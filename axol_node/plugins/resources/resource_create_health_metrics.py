#! /usr/bin/env python
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
from axol_common.classes.common_timer import CommonTimer
from axol_common.classes.common_logger import CommonLogger
from axol_common.classes.common_resource import CommonResource
from axol_common.classes.common_math import CommonMath
from axol_common.classes.common_data_object import GenericDataObject
from classes.axol_resource import AxolResource
from axol_config import api
from aapi.aapi import app as app
from flask import jsonify
from flask import request
from ast import literal_eval
from task_engine.TaskEngine import DW
from math import *
from sys import getsizeof
import time

class ResourceCreateHealthMetrics(AxolResource):
	"""docstring for ResourceGetProcessorUsage
	Must implement:
		_show_help()
		self.source = {keyword}
		self.local = Bool
		self.store = Bool
		self.profiler = Bool
		api_<name of your api>()
		calculate_new_fields()
		write_to_database()
	Optional:
		if self.store = True, write_to_database() function must be implemented
	"""
	required_post = {
		'role': (True, u's'),
		'profile': (False, u's')
		}

	def __init__(self):
		super(ResourceCreateHealthMetrics, self).__init__()
		self.source = 'health'
		self.local = True
		self.store = True
		self.profiler = True
		self.sources = [
			'cpu',
			'memory',
			'disk',
			'mean',
			'deviation_pos',
			'deviation_neg'
			]
		self.thresholds = (0)

	def _show_help(self):
		return {
			'help': {
				'api': '/api/create_health_metrics',
				'method': 'POST',
				'required_data': {
					'role': '<some role>',
					},
				'version': api
				}
			}

	@staticmethod
	@app.route('/api/create_health_metrics', methods=['GET', 'POST'])
	def api_create_health_metrics():
		if request.method == 'GET':
			return jsonify(ResourceCreateHealthMetrics()._show_help())
		try:
			data = CommonResource.handle_request(
				request=request,
				params=ResourceCreateHealthMetrics.required_post
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='create_health_metrics',
				method='api_create_health_metrics-1'
				)
			return jsonify(report)
		try:
			response = ResourceCreateHealthMetrics().create_async_job(
				data=data
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='create_health_metrics',
				method='api_create_health_metrics-2'
				)
			return jsonify(report)
		try:
			ResourceCreateHealthMetrics().populate_cache(
				response=response['response']
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='create_health_metrics',
				method='api_create_health_metrics-3'
				)
			return jsonify(report)
		return jsonify(response)

	def populate_cache(self, response):
		server_dict = {}
		print response
		print '##################'
		response['api'] = api
		response['api']['api_name'] = 'health'
		for item in response['value']:
			print '1111'
			print response['value'][item]
			response['value'][item] = response['value'][item]
			for item_2 in response['value'][item]:
				if item_2 != 'name' and item_2 != 'warnings':
					print '2222'
					print response['value'][item][item_2]
					response['value'][item][item_2] = response['value'][item][item_2]
					key = 'ro_%s_%s' % (item_2, item)
					print '-------------------'
					print key
					DW.cache_key_set(key, response['value'][item][item_2])

	def run_task(self, task):
		print 'RUN TASK 1 ##############'
		print task
		for server in task.value:
			for _type in self.sources:
				key = '%s_%s' % (_type, str(server))
				try:
					cache_data = DW.cache_key_get(key)
					if type(eval(str(cache_data))) is dict:
						try:
							task.value[server][_type] = GenericDataObject(eval(str(cache_data)))
							if task.value[server][_type].warnings[server] != None:
								print 'RED FLAG: %s %s' % (server, _type)
								print task.value[server][_type].warnings
							else:
								task.value[server][_type].health_indicator = CommonMath.adaptive_filtration(
									task.value[server][_type].normalized_indicator,
									task.value[server][_type].multiplier,
									task.value[server][_type].threshold_red,
									task.value[server][_type].scale
									)
						except Exception, e:
							print 'ERROR 1: %s' % e
				except Exception, e:
					CommonLogger.log(e, 'create_health_metrics', 'run_task-<%s-%s>' % (server, _type))
					print 'ERROR 2: %s' % e
					return jsonify({'response': {'error': str(e)}})
		new_obj = GenericDataObject(task.value[server])
		new_obj.name = server
		task.value[server] = new_obj
		try:
			for server in task.value:
				task.value[server] = self.validate_thresholds(task.value[server])
		except Exception, e:
			print 'ERROR 3: %s' % e
		print 'RUN TASK 2 ##############'
		print task
		return task

	def validate_thresholds(self, data_object):
		def test_against_thresholds(sub_object):
			if type(sub_object) is GenericDataObject:
				sub_object.warnings = {}
				if hasattr(sub_object, 'normalized_indicator'):
					percent = sub_object.normalized_indicator * 100
				else:
					percent = 100
				if hasattr(sub_object, 'error') and getattr(sub_object, 'error') != None:
					print '%s <sub_obj error>: %s' % (sub_object.name, sub_object.error)
					sub_object.warnings['status'] = 3
					sub_object.warnings[sub_object.name] = {}
					sub_object.warnings[sub_object.name]['error'] = sub_object.error
					print 'Return Cond: Has Error'
					return sub_object
				elif hasattr(sub_object, 'health_indicator') and sub_object.health_indicator < 0:
					sub_object.warnings['status'] = 2
					sub_object.error = "%s on %s's health currently at %s {%s percent}" % (
						sub_object.source,
						sub_object.name,
						sub_object.health_indicator,
						percent
						)
					sub_object.error2 = "%s, health=%s" % (
						sub_object.name,
						sub_object.health_indicator
						)
					sub_object.warnings[sub_object.name] = {}
					sub_object.warnings[sub_object.name]['error'] = (
						sub_object.error,
						sub_object.error2
						)
					sub_object.error_count = 1
					print 'Return Cond: Threshold Exceeded'
					return sub_object
				else:
					sub_object.warnings['status'] = 0
					sub_object.warnings[sub_object.name] = {}
					sub_object.warnings[sub_object.name]['error'] = None
					print 'Return Cond: healthy'
					return sub_object
		for _type in self.sources:
			if hasattr(data_object, _type):
				print 'RUN: VT: %s' % _type
				sub_object = getattr(data_object, _type)
				sub_object = test_against_thresholds(sub_object)
				setattr(data_object, _type, sub_object)
		return data_object

	def calculate_new_fields(self, response_object):
		return response_object

	def post_processing(self, axol_task_value):
		return axol_task_value

	def write_to_database(self, axol_task_value):
		pass
