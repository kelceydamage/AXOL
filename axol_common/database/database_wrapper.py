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

# Import main
#-----------------------------------------------------------------------#

# EC2
from boto import ec2

# Dynamodb
from boto import dynamodb
from boto.dynamodb import *

# Elasticache
from boto import elasticache
from boto.elasticache import layer1
from redis import *

# LMDB
from lmdb import *

# Database class
#-----------------------------------------------------------------------#

class DatabaseWrapper(object):
	"""When instantiating this class, a valid service name must be passed to the constructor"""
	def __init__(self, service):
		super(DatabaseWrapper, self).__init__()
		self.region = "us-west-2"
		self.service = service
		if self.service == 'elasticache':
			self._init_elasticache()
		elif self.service == 'dynamodb':
			self._init_dynamodb()
		elif self.service == 'lmdb':
			self._init_lmdb()

# LMDB interface
#-----------------------------------------------------------------------#
	def _init_lmdb(self):
		print 'init db'
		lmdb = Environment(
			path='/opt/AXOL_Management/AXOL/axol_node/database',
			map_size=256000000,
			subdir=True,
			map_async=True,
			writemap=True,
			max_readers=24,
			max_dbs=0,
			max_spare_txns=24,
			lock=True
			)
		self.LMDB = lmdb
		self.cache_endpoint = '/opt'
		print 'complete'

# DynamoDB discovery interface
#-----------------------------------------------------------------------#
	def _init_dynamodb(self):
		self._connect_to_dynamodb()
		self.table = self.database.get_table('axol_notifications')
		self.cache_endpoint = self.table

	def _connect_to_dynamodb(self):
		self.database = dynamodb.connect_to_region(
			self.region,
			aws_access_key_id="AKIAJQF4ELAIIMGJABZA",
			aws_secret_access_key="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"
			)

# Elasticache discovery interface
#-----------------------------------------------------------------------#
	def _init_elasticache(self):
		self._connect_to_elasticache()
		self._get_cache_parameters()
		self._describe_replication_groups()
		endpoint = self._get_cache_endpoint()
		self.redis = StrictRedis(
			host=endpoint[0],
			port=endpoint[1]
			)

	def _connect_to_elasticache(self):
		self.cache = elasticache.connect_to_region(
			self.region,
			aws_access_key_id="AKIAJQF4ELAIIMGJABZA",
			aws_secret_access_key="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"
			)

	def _get_cache_parameters(self):
		response = self.cache.describe_cache_clusters()
		self.cache_parameters = response['DescribeCacheClustersResponse']['DescribeCacheClustersResult']['CacheClusters'][0]

	def _describe_replication_groups(self):
		replication_group = self.cache.describe_replication_groups(self.cache_parameters['ReplicationGroupId'])
		self.replication_group = replication_group['DescribeReplicationGroupsResponse']['DescribeReplicationGroupsResult']['ReplicationGroups'][0]
		self.cache_endpoint = self.replication_group['NodeGroups'][0]['PrimaryEndpoint']['Address']
		self.cache_port = self.replication_group['NodeGroups'][0]['PrimaryEndpoint']['Port']

	def _get_cache_endpoint(self):
		return (self.cache_endpoint, self.cache_port)

# Cache interface
#-----------------------------------------------------------------------#

	def cache_key_set(self, name, value):
		if self.service == 'elasticache':
			self.redis.set(
				name=name,
				value=value
				)
		elif self.service == 'lmdb':
			with Environment.begin(self.LMDB, write=True) as txn:
				txn.put(
					str(name),
					str(value),
					overwrite=True
					)
		elif self.service == 'dynamodb':
			item = self.table.new_item(
				hash_key=str(name),
				range_key='axol_cache',
				attrs={'item': str(value)}
				)
			item.put()
		else:
			return 'invalid method for service'

	# name_list must have key_name as first element in list
	def cache_key_zset(self, name_list):
		if self.service == 'elasticache':
			return self.redis.zadd(name_list)
		else:
			return 'invalid method for service'

	def cache_key_get(self, name):
		if self.service == 'elasticache':
			return self.redis.get(name)
		elif self.service == 'lmdb':
			with Environment.begin(self.LMDB, write=True) as txn:
				return txn.get(name)
		elif self.service == 'dynamodb':
			return self.table.get_item(
				hash_key=str(name),
				range_key='axol_cache'
				)['item']
		else:
			return 'invalid method for service'

	def cache_key_delete(self, name):
		if self.service == 'elasticache':
			return self.redis.delete(name)
		else:
			return 'invalid method for service'

	def cache_key_exists(self, name):
		if self.service == 'elasticache':
			return self.redis.exists(name)
		else:
			return 'invalid method for service'

# Database interface
#-----------------------------------------------------------------------#

	def database_table_list(self):
		return self.database.list_tables()

	def database_table_get(self, table_name):
		return self.database.get_table(table_name)

	def database_table_describe(self, table_name):
		return self.database.describe_table(table_name)

	def database_table_set(self, table_name, key_name, source, value):
		table = self.database.get_table(table_name)
		item = table.new_item(hash_key=key_name, range_key=source, attrs=value)
		item.put()

	def database_table_get(self, table_name, key_name, source):
		table = self.database.get_table(table_name)
		item = table.get_item(hash_key=key_name, range_key=source)
		return item

# Example Usage
#-----------------------------------------------------------------------#
'''
print '#-----------------------------------------------------------------------#'
DW = DatabaseWrapper('lmdb')
print '\nSERVICE: %s' % DW.service
print 'Cache Endpoint: %s' % DW.cache_endpoint
print '\nCalling: DatabaseWrapper.cache_key_set("test", "true")'
print '### Set key: "test", value: "true"'
DW.cache_key_set('test', 'true')
print '\nCalling: DatabaseWrapper.cache_key_get("test")'
print '### Get key response: %s\n' % DW.cache_key_get('test')
print '#-----------------------------------------------------------------------#'
DW = DatabaseWrapper('elasticache')
print '\nSERVICE: %s' % DW.service
print 'Cache Endpoint: %s' % DW.cache_endpoint
print '\nCalling: DatabaseWrapper.cache_key_set("test", "true")'
print '### Set key: "test", value: "true"'
DW.cache_key_set('test', 'true')
print '\nCalling: DatabaseWrapper.cache_key_get("test")'
print '### Get key response: %s\n' % DW.cache_key_get('test')
print '#-----------------------------------------------------------------------#'
DW = DatabaseWrapper('dynamodb')
print '\nSERVICE: %s' % DW.service
print 'Cache Endpoint: %s' % DW.cache_endpoint
print '\nCalling: DatabaseWrapper.cache_key_set("test", "true")'
print '### Set key: "test", value: "true"'
DW.cache_key_set('test', 'true')
print '\nCalling: DatabaseWrapper.cache_key_get("test")'
print '### Get key response: %s\n' % DW.cache_key_get('test')
print '#-----------------------------------------------------------------------#'
'''







