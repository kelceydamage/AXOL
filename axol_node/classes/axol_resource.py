#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
from celery.contrib.methods import task_method
from task_engine.TaskEngine import TE
from task_engine.TaskEngine import TaskEngine
from task_engine.TaskEngine import ES
from task_engine.TaskEngine import DW
from task_engine.TaskEngine import LOG
from axol_common.classes.common_data_object import GenericDataObject
from axol_common.classes.common_resource import CommonResource
from axol_common.classes.common_logger import CommonLogger
from distributed.socket_client import AgentClient
from datetime import datetime
from datetime import timedelta
from classes.Messaging import Messaging
from ast import literal_eval
from math import *
from sys import getsizeof
import time
import sys
import socket
import json
import struct

class AxolResource(object):
	"""ResourceType Object is a static object containing global methods for all
	resource classes"""

	def __init__(self):
		super(AxolResource, self).__init__()
		pass

	@staticmethod
	def create_server_list(roledefs, role_name):
		server_dict = {}
		for server in roledefs[role_name]:
			name = AgentClient(roledefs)._match_name(server)
			server_dict[name] = server
		return server_dict

	def create_async_job(self, data):
		create_async_time = time.time()
		AxolTask, t = self.process_queue(
			self.async_job.delay(data)
			)
		if type(AxolTask) is dict:
			return AxolTask
		else:
			if AxolTask.source == 'health':
				return AxolTask.format_response()
			else:
				AxolTask.value = eval(str(AxolTask.value).decode())
				AxolTask.time = t
				AxolTask.create_async_time = time.time() - create_async_time
				return AxolTask.format_response()

	@TE.engine.task(filter=task_method, name='AxolResource.async_job')
	def async_job(self, data):
		async_job_time = time.time()
		try:
			new_data_object = GenericDataObject(data.return_attribute_dict())
			new_data_object.data = data.return_attribute_dict()
			data = ''
			new_data_object.source = self.source
			new_data_object.resource = self
			AxolTask = TaskEngine().run_task(new_data_object)
		except Exception, e:
			CommonLogger.log(e, 'axol_resource', 'async_job')
		if type(AxolTask) == dict:
			return AxolTask
		elif AxolTask.source == 'health':
			AxolTask.async_job_time = time.time() - async_job_time
			return AxolTask
		else:
			AxolTask.value = str(AxolTask.value).encode()
			AxolTask.async_job_time = time.time() - async_job_time
			return AxolTask

	@TE.engine.task(filter=task_method, name='AxolResource.notification')
	def notification(self, name, data):
		Messaging().notification(name, data)

	@TE.engine.task(filter=task_method, name='AxolResource.notification_type_2')
	def notification_type_2(self, name, data, group, alert_type):
		Messaging().notification_type_2(name, data, group, alert_type)

	@TE.engine.task(filter=task_method, name='AxolResource.database_query')
	def database_query(self, response):
		self.query(response)

	def send_notice(self, name, data, group=None, alert_type=None):
		self.notification_type_2.delay(name, data, group, alert_type)

	def query_async(self, response):
		self.database_query.delay(response)

	'''
	def send_event(self, e, resource, method):
		LOG.error = str(e)
		LOG.resource = resource
		LOG.method = method
		self.log(LOG)
	'''

	def generate_id(self, time):
		time = time[0:10] + '.' + time[11:26]
		return time

	def query(self, query_list):
		def __connect(request):
			client_socket = socket.socket(
				socket.AF_INET,
				socket.SOCK_STREAM
				)
			tls_sock = client_socket
			tls_sock.settimeout(1)
			error = 'undefined'
			try:
				tls_sock.connect(('127.0.0.1',9999))
				error = None
			except Exception, e:
				error = str(e)
				print 'CASSANDRA ERROR {__connect|send}: %s' % error
			try:
				request = str(json.dumps(request)).encode('base64','strict')
				print 'SEND SIZE: %s' % getsizeof(request)
				request = struct.pack('>I', len(request)) + request
				tls_sock.sendall(request)
				error = None
			except Exception, e:
				error = str(e)
				print 'CASSANDRA {__connect|connect}: %s' % (error)
			return tls_sock, error

		request = {}
		request['commands'] = query_list
		request['method'] = 'cassandra'
		tls_sock, error = __connect(request)

	def threshold_validation(self, response_object):
		data = {'error': 'Current health: %s, below threshold: %s on %s' % (
			response_object.health_indicator,
			response_object.threshold_red,
			response_object.name
			)}
		if response_object.health_indicator < 0:
			try:
				self.send_notice(
					name='threshold_validation',
					data=data,
					group='default',
					alert_type=['email']
					)
			except Exception, e:
				status = 'incomplete'
				CommonLogger.log(e, 'threshold_validation', 'threshold_validation')
			response_object.warnings[response_object.name] = data['error']
		return response_object

	def notification_threshold(self, AxolTask):
		def process_notification(name, AxolTask, key):
			notification_status = DW.cache_key_get(key)
			print '<Notification Status>: %s' % notification_status
			if notification_status == None:
				default = {
					'warn_threshold': 0,
					'silence_threshold': 0
					}
				DW.cache_key_set(key, default)
				notification_status = DW.cache_key_get(key)
			ns = literal_eval(notification_status)
			ns['warn_threshold'] += 1
			if (7 >= ns['warn_threshold'] > 4 and ns['silence_threshold'] == 0):
				self.send_notice(
					name=AxolTask.name,
					data=AxolTask.value,
					group='default',
					alert_type=['email', 'text']
					)
				DW.cache_key_set(key, ns)
				return 1
			elif (ns['warn_threshold'] > 4 and ns['silence_threshold'] <= 12):
				ns['silence_threshold'] += 1
				DW.cache_key_set(key, ns)
				return 1
			elif ns['silence_threshold'] > 12:
				ns['warn_threshold'] = 5
				ns['silence_threshold'] = 0
				DW.cache_key_set(key, ns)
				return 1
			DW.cache_key_set(key, ns)
			return 1

		key = 'notification_threshold'
		if len(AxolTask.value) > 0:
			for server in AxolTask.value:
				if server != 'status':
					if AxolTask.value[server] != []:
						print '<Task Warnings>: %s' % AxolTask.value[server]
						try:
							process_notification(server, AxolTask, key)
						except Exception, e:
							CommonLogger.log(e, 'axol_resource', 'process_notification')
		else:
			default = {
				'warn_threshold': 0,
				'silence_threshold': 0
				}
			DW.cache_key_set(key, default)
		return 1

	def process_queue(self, result):
		t = 0
		while True:
			if result.ready() == True:
				g = result.get()
				return g, t
				break
			else:
				t = t + 0.001
				time.sleep(0.001)
				if t >= 10:
					tmp = {
						'Response': {
							'failed_request': True
							}
						}
					return tmp, t
					break

	def calculate_new_fields(self, response_object):
		return response_object

	def post_processing(self, axol_task_value):
		return axol_task_value

	def write_to_database(self, axol_task_value):
		pass
