#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

from axol_common.distributed.axol_roledefs import roledefs
from axol_common.database.database_wrapper import DatabaseWrapper
from axol_common.classes.common_logger import CommonLogger
from axol_common.classes.common_data_object import GenericDataObject
from re import search
from celery import Celery
from celery.signals import worker_process_init, worker_init
from AxolTask import AxolTask
from axol_config import backend
from axol_config import broker
from axol_config import cache
from axol_config import node
from axol_config import log_params
from elasticsearch import Elasticsearch
import json
from lmdb import *
import os
import subprocess
from sys import getsizeof
from ast import literal_eval
from cassandra.cluster import Cluster
import time

# TaskEngine Class
#-----------------------------------------------------------------------#
class TaskEngine(object):
	"""docstring for TaskEngine"""
	def __init__(self):
		super(TaskEngine, self).__init__()
		self.AxolTask = AxolTask()
		self.error_types = [
			'None',
			'null',
			'Timed out',
			'Low level',
			'Name look'
			]

	def set_engine(self, engine):
		self.engine = engine
		self.engine.conf.update(
			CELERY_TASK_RESULT_EXPIRES = 30,
			)

# Per task methods
#-----------------------------------------------------------------------#
	def run_task(self, new_data_object):
		try:
			roledefs = literal_eval(DW.cache_key_get('roledefs'))
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='task_engine',
				method='cache_key_get'
				)
			return report
		print '### build task'
		try:
			self._build_task(
				roledefs=roledefs,
				data=new_data_object
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='task_engine',
				method='build_task'
				)
			return report
		post_process_time = time.time()
		print '### process task'
		if self.AxolTask.resource.local == False:
			try:
				self._process_task_response()
			except Exception, e:
				report = CommonLogger.log(
					error=e,
					source='task_engine',
					method='process_task_response'
					)
				return report
		print '### health'
		if self.AxolTask.source == 'health':
			try:
				self.AxolTask.resource.notification_threshold(
					AxolTask=self.AxolTask
					)
			except Exception, e:
				report = CommonLogger.log(
					error=e,
					source='task_engine',
					method='notification_threshold'
					)
				return report
		print '### post process'
		try:
			self.AxolTask.post_process()
		except Exception, e:
				report = CommonLogger.log(
					error=e,
					source='task_engine',
					method='post_processing'
					)
				return report
		self.AxolTask.post_process_time = time.time() - post_process_time
		print '### database write'
		database_write_time = time.time()
		try:
			self.AxolTask.write_data()
		except Exception, e:
 			report = CommonLogger.log(
 				error=e,
 				source='task_engine',
 				method='write_data'
 				)
 			return report
		self.AxolTask.database_write_time = time.time() - database_write_time
		return self.AxolTask

	def _build_task(self, roledefs, data):
		print 'TASK ENGINE 1 ##############'
		print data.print_attributes_with_values()
		self.AxolTask.source = data.source
		self.AxolTask.role = data.role
		self.AxolTask.resource = data.resource
		self.AxolTask.data = data.data
		task_payload_execution_time = time.time()
		if self.AxolTask.resource.local == True:
			self.AxolTask.execute_local(
				roledefs=roledefs
				)
		else:
			self.AxolTask.execute(
				roledefs=roledefs
				)
		self.AxolTask.task_payload_execution_time = time.time() - task_payload_execution_time
		print '## completed build'

	def store_to_cache(self, server):
		key = '%s_%s' % (self.AxolTask.source, str(server))
		value = str(self.AxolTask.value[server]).encode()
		DW.cache_key_set(key, value)

	def _process_task_response(self):
		default = {
			'warn_threshold': 0,
			'silence_threshold': 0
			}

		def check_for_error(data, error_range_x, error_range_y):
			for error in self.error_types[error_range_x:error_range_y]:
				if error in str(data):
					return True

		if self.AxolTask.value != '':
			for server in self.AxolTask.value:
				if hasattr(self.AxolTask.value[server], 'source'):
					self.AxolTask.value[server] = self.AxolTask.value[server].return_attribute_dict()
					self.AxolTask.warnings[server] = self.AxolTask.value[server]['warnings'][server]
					if self.AxolTask.warnings[server] == None:
						self.AxolTask.warnings['status'] = 0
					elif self.AxolTask.warnings[server] != None:
						self.AxolTask.warnings[server] = {'error': self.AxolTask.warnings[server]}
						self.AxolTask.warnings_count = 1
						self.AxolTask.warnings['status'] = 2
					self.store_to_cache(server)
				else:
					self.AxolTask.warnings[server] = []
					server_data = self.AxolTask.value[server].return_attribute_dict()
					for _type in server_data:
						if hasattr(server_data[_type], 'warnings'):
							if server_data[_type].warnings[server]['error'] != None:
								server_data[_type].warnings[server]['condition'] = _type
								self.AxolTask.warnings[server].append(server_data[_type].warnings[server])
								self.AxolTask.warnings['status'] = 3
					if self.AxolTask.warnings[server] == []:
						key = str('notification_%s' % server)
						DW.cache_key_set(key, default)
					self.AxolTask.warnings_count = 1
		else:
			self.AxolTask.value[server]['error'] = 'an error occured'
			self.AxolTask.warnings_count = 1
			self.AxolTask.warnings['status'] = 4
		key = '%s_warnings' % self.AxolTask.source
		value = self.AxolTask.warnings
		DW.cache_key_set(key, value)

# Celery app config
#-----------------------------------------------------------------------#
print 'STARTING CELERY'
print backend
print broker

celery = Celery('AXOL', backend=backend, broker=broker)
celery.config_from_object({
	'CELERYD_POOL_RESTARTS': False,
	'CELERY_TASK_RESULT_EXPIRES': 15,
	'CELERYD_TASK_TIME_LIMIT': 15,
	'BROKER_POOL_LIMIT': 0,
	'BROKER_CONNECTION_TIMEOUT': 1,
	})

# Cache instantiation
#-----------------------------------------------------------------------#
#DW = DatabaseWrapper('elasticache')
DW = DatabaseWrapper(cache)
print 'INIT CACHE: %s' % DW.service

# Store roledefs
#-----------------------------------------------------------------------#
DW.cache_key_set('roledefs', roledefs)

# Task Engine instantiation
#-----------------------------------------------------------------------#
TE = TaskEngine()
TE.set_engine(celery)

# Elasticsearch configuration
#-----------------------------------------------------------------------#
print 'CONFIGURING ELASTICSEARCH'
ES = Elasticsearch(node)

# Logger obj creation
#-----------------------------------------------------------------------#
LOG = GenericDataObject(log_params)
