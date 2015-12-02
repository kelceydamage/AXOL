#! /usr/bin/env python
# coding: utf-8
#-----------------------------------------#
# Copyright [2015] [Kelcey Jamison-Damage]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Imports
#-----------------------------------------------------------------------#
from axol_common.classes.common_logger import CommonLogger
from axol_common.classes.common_data_object import GenericDataObject
from axol_common.classes.common_resource import CommonResource
from classes.axol_resource import AxolResource
from axol_config import api
from aapi.aapi import app as app
from flask import jsonify
from flask import request
from sys import getsizeof

class ResourceGetMysqlUsage(AxolResource):
	"""docstring for ResourceGetMysqlUsage
	Must implement:
		_show_help
		self.methods = {<method_type>: function}
		self.source = {keyword}
		request_{keyword}_api
		calculate_new_fields
	"""
	required_post = {
		'role': (True, u's'),
		'profile': (False, u's')
		}

	def __init__(self):
		super(ResourceGetMysqlUsage, self).__init__()
		self.source = 'mysql'
		self.local = False

	def _show_help(self):
		return {
			'help': {
				'usage': '/api/get_mysql_usage',
				'method': 'POST',
				'required_data': {
					'role': '<some role>',
					'alert_type': ['email', 'text']
					},
				'version': api
				}
			}

	@staticmethod
	@app.route('/api/get_mysql_usage', methods=['GET', 'POST'])
	def api_get_mysql_usage():
		if request.method == 'GET':
			return jsonify(ResourceGetMysqlUsage()._show_help())
		try:
			data = CommonResource.handle_request(request, ResourceGetMysqlUsage.required_post)
		except Exception, e:
			CommonLogger.log(e, 'get_mysql_usage', 'api_get_mysql_usage')
			return jsonify({'response': {'error': str(e)}})
		try:
			response = ResourceGetMysqlUsage().create_async_job(data)
		except Exception, e:
			CommonLogger.log(e, 'get_mysql_usage', 'api_get_mysql_usage')
			return jsonify({'response': {'error': str(e)}})
		return jsonify(response)

	def calculate_new_fields(self, response_object):
		def calculate_key_read_efficiency(response_object):
			# Key Reads: The number of physical reads of a key block from disk.
			# Key Read Request: The number of requests to read a key block from the cache.
			# Key Read Efficiency: The ratio of the number of physical reads of a key
			# block from the cache to the number of requests to read a key block from
			# the cache in percentage. The MySQL performance is good if the value of Key
			# Read Efficiency is 90 percent and above. Increasing the size of the cache
			# improves the value of Key Read Efficiency and hence an improved the
			# performance.
			response_object.efficiency_key_read = (
				float(response_object.key_reads) / float(response_object.key_read_requests)
				)
			response_object.efficiency_key_read_miss_rate = int((
				float(response_object.key_read_requests) / float(response_object.key_reads)
				))
			return response_object

		def calculate_key_write_efficiency(response_object):
			# Key Writes: The number of physical writes of a key block to disk.
			# Key Write Request: The number of requests to write a key block to the cache.
			# Key Write Efficiency: The ratio of the number of physical writes of a key
			# block to the cache to the number of requests to write a key block to the cache
			# in percentage. For a good performance of the MySQL server, the value of Key
			# Write Efficiency must be 90 percent and above. If it is found less, then you
			# can increase the size of the cache to improve the performance.
			response_object.efficiency_key_write = (
				float(response_object.key_writes) / float(response_object.key_write_requests)
				) * 100
			response_object.efficiency_key_write_miss_rate = round((
				float(response_object.key_write_requests) / float(response_object.key_writes)
				), 2)
			return response_object

		def calculate_key_buffer_used(response_object):
			# SELECT SUM(INDEX_LENGTH)/(1024*1024) 'Index Size' FROM
			# information_schema.TABLES where ENGINE='MyISAM' AND TABLE_SCHEMA
			# NOT IN('mysql','information_schema');
			# if result is (<=100 ) then your all indexes are cached into key_buffer
			# if result is (>100) then your all indexes are not cached into key_buffer
			# you may gain performance boost by increasing key_buffer_size.
			pass

		def calculate_qcache_hit_rate(response_object):
			# Hit rate = Qcache_hits / (Qcache_hits + Com_select) * 100
			a = response_object.qcache_hits
			b = response_object.com_select
			response_object.efficiency_qcache_hit_rate = round((
				(float(a) / (float(a) + float(b))) * 100
				), 2)
			return response_object

		def calculate_query_insert_rate(response_object):
			# Insert rate = Qcache_inserts / (Qcache_hits + Com_select) * 100
			a = response_object.qcache_hits
			b = response_object.com_select
			c = response_object.qcache_inserts
			response_object.efficiency_qcache_insert_rate = round((
				(float(c) / (float(a) + float(b))) * 100
				), 2)
			return response_object

		def calculate_query_prune_rate(response_object):
			# Prune rate = (Qcache_lowmem_prunes / Qcache_inserts) * 100
			a = response_object.qcache_inserts
			b = response_object.qcache_lowmem_prunes
			response_object.efficiency_qcache_prune_rate = round((
				((float(b) / float(a))) * 100
				), 2)
			return response_object

		def calculate_qcache_fragmentation(response_object):
			# Over time Query Cache might get fragmented, which reduces performance.
			# This can be seen as large value of Qcache_free_blocks relatively to
			# Qcache_free_memory. FLUSH QUERY CACHE command can be used for query
			# cache defragmentation but it may block query cache for rather long time
			#for large query caches, which might be unsuitable for online applications.
			a = response_object.qcache_free_blocks
			b = response_object.qcache_free_memory
			response_object.efficiency_qcache_fragmentation_ratio = (
				b / (a * 1024)
				)
			return response_object

		def calculate_pruning_ratio(response_object):
			# Queries are constantly being invalidated from query cache by table updates,
			# this means number of queries in cache and memory used can not grow forever
			# even if your have very large amount of different queries being run. Of
			# course in some cases you have tables which are never modified which would
			# flood query cahe but it unusual. So you might want to set query cache to
			# certain value and watch Qcache_free_memory and Qcache_lowmem_prunes – If
			# you’re not getting much of lowmem_prunes and free_memory stays high you
			# can reduce query_cache appropriately. Otherwise you might wish to increase
			# it and see if efficiency increases
			pass

		def calculate_qcache_efficiency(response_object):
			# There are few ways you can look at query_cache efficiency. First looking
			# at number of your selects – Com_select and see how many of them are cached.
			# Query Cache efficiency would be Qcache_hits/(Com_select+Qcache_hits). As
			# you can see we have to add Qcache_hits to Com_select to get total number
			# of queries as if query cache hit happens Com_select is not incremented.
			# But if you have just 20% Cache hit rate does it mean it is not worth it ?
			# Not really it depends on which queries are cached, as well as overhead query
			# cache provides. One portion of query cache overhead is of course inserts so
			# you can see how much of inserted queries are used: Qcache_hits/Qcache_inserts
			# Other portion of overhead comes from modification statements which you can
			# calculate by (Com_insert+Com_delete+Com_update+Com_replace)/Qcache_hits
			pass

		def calculate_qcache_hit_efficiency(response_object):
			# query cache hit rate percentage ((Qcache_hits / (Qcache_hits + Qcache_inserts
			# + Qcache_not_cached))*100) should be as close to 100% as possible.
			pass

		def calculate_current_usage(response_object):
			n = 1
			n = int(n) + 0
			response_object.current_usage = n
			return response_object

		def calculate_usage_for_health(response_object):
			response_object.normalized_indicator = 1
			response_object.multiplier = 1
			response_object.threshold_red = 100
			response_object.scale = 0
			return response_object
		if response_object.error == None:
			response_object = calculate_current_usage(response_object)
			response_object = calculate_usage_for_health(response_object)
			response_object = calculate_key_read_efficiency(response_object)
			response_object = calculate_key_write_efficiency(response_object)
			response_object = calculate_qcache_fragmentation(response_object)
			response_object = calculate_query_prune_rate(response_object)
			response_object = calculate_qcache_hit_rate(response_object)
			response_object = calculate_query_insert_rate(response_object)
			return response_object
		else:
			print '#### %s %s' % (response_object.name, response_object.error)
		return response_object

