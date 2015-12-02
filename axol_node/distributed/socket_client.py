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

from axol_common.classes.common_data_object import GenericDataObject
from axol_common.classes.common_logger import CommonLogger
import socket
import time
import sys
import ssl
import json
from classes.processing import Processing
from multiprocessing import current_process
from re import search
from sys import getsizeof

class AgentClient(object):
	def __init__(self, roledefs):
		self.roledefs = roledefs

	def agent_query(self, task):
		client_setup_time = time.time()
		current_process().daemon = False
		role = task.role
		processing_object = Processing()
		self.q = processing_object.create_queue()
		response = {}
		task.client_setup_time = time.time() - client_setup_time
		process_spawner_time = time.time()
		p = processing_object.new_process(
			self._child_process,
			[role, processing_object, task]
			)
		response = []
		task.process_spawner_time = time.time() - process_spawner_time
		queue_reduction_time = time.time()
		name_time_list = []
		gdo_time_list = []
		new_fields_time_list = []
		socket_client_init_list = []
		socket_client_connect_list = []
		socket_client_send_list = []
		socket_client_recv_list = []
		for host in self.roledefs[role]:
			queue_response = self.q.get(timeout=4)
			task.value[queue_response.name] = queue_response
			name_time_list.append(queue_response.times['match_name_time'])
			gdo_time_list.append(queue_response.times['gdo_time'])
			new_fields_time_list.append(queue_response.times['calculate_new_fields_time'])
			socket_client_init_list.append(queue_response.times['socket_client_init_time'])
			socket_client_connect_list.append(queue_response.times['socket_client_connect_time'])
			socket_client_send_list.append(queue_response.times['socket_client_send_time'])
			socket_client_recv_list.append(queue_response.times['socket_client_recv_time'])
		task.queue_reduction_time = time.time() - queue_reduction_time
		process_join_time = time.time()
		p.join()
		task.process_join_time = time.time() - process_join_time
		task.match_name_time = sum(name_time_list) / len(name_time_list)
		task.gdo_time = sum(gdo_time_list) / len(gdo_time_list)
		task.calculate_new_fields_time = sum(new_fields_time_list) / len(new_fields_time_list)
		task.socket_client_init_time = sum(socket_client_init_list) / len(socket_client_init_list)
		task.socket_client_connect_time = sum(socket_client_connect_list) / len(socket_client_connect_list)
		task.socket_client_send_time = sum(socket_client_send_list) / len(socket_client_send_list)
		task.socket_client_recv_time = sum(socket_client_recv_list) / len(socket_client_recv_list)
		print 'CLIENT TASK SIZE: %s' % getsizeof(task.value)
		return task

	def _match_name(self, host):
		for name in self.roledefs:
			if search(r'live', name) or search(r'dev', name):
				if host in self.roledefs[name]['external'] \
				or host in self.roledefs[name]['internal']:
					name = name.strip('_L')
					return name

	def process_gdo(self, task, server, host, times):
		gdo_time = time.time()
		match_name_time = time.time()
		name = self._match_name(host)
		times['match_name_time'] = time.time() - match_name_time
		GDO = GenericDataObject(server)
		GDO.host = host
		GDO.name = name
		GDO.source = task.source
		GDO.warnings = {}
		if hasattr(task.resource, 'calculate_new_fields'):
			calculate_new_fields_time = time.time()
			GDO = task.resource.calculate_new_fields(GDO)
			times['calculate_new_fields_time'] = time.time() - calculate_new_fields_time
		times['gdo_time'] = time.time() - gdo_time
		GDO.times = times
		return GDO

	def _child_process(self, role, processing_object, task):
		process_list = []

		def __connect(self, host, task):
			times = {}
			socket_client_init_time = time.time()
			client_socket = socket.socket(
				socket.AF_INET,
				socket.SOCK_STREAM
				)
			tls_sock = ssl.wrap_socket(
				client_socket,
				cert_reqs=ssl.CERT_NONE,
				do_handshake_on_connect=False,
				ssl_version=ssl.PROTOCOL_TLSv1
				)
			tls_sock.settimeout(1)
			error = 'undefined'
			times['socket_client_init_time'] = time.time() - socket_client_init_time
			socket_client_connect_time = time.time()
			try:
				tls_sock.connect((host,9999))
				error = None
			except Exception, e:
				error = str(e)
			times['socket_client_connect_time'] = time.time() - socket_client_connect_time
			socket_client_send_time = time.time()
			try:
				tls_sock.send(task.source)
			except Exception, e:
				if error != None:
					error = '%s, %s' % (error, str(e))
				else:
					error = str(e)
			times['socket_client_send_time'] = time.time() - socket_client_send_time

			return tls_sock, error, times

		def __spawn(self, host, task):
			tls_sock, error, times = __connect(
				self,
				host,
				task
				)
			socket_client_recv_time = time.time()
			if error == None:
				try:
					server = json.loads(tls_sock.recv(10244))
					if 'error' in server:
						error = server['error']
				except Exception, e:
					server = {'error': str(e)}
			else:
				server = {'error': error}
			if 'error' not in server:
				server['error'] = None
			times['socket_client_recv_time'] = time.time() - socket_client_recv_time
			GDO = self.process_gdo(
				task,
				server,
				host,
				times
				)
			GDO.warnings[GDO.name] = error
			if GDO.warnings[GDO.name] != None:
				print '<GDO Warnings>: %s' % GDO.warnings[GDO.name]
			try:
				if not hasattr(GDO, 'name'):
					print 'AGENT ERROR {__spawn|q.put}: %s' % host
					print 'AGENT ERROR {__spawn|q.put}: %s' % dir(GDO)
					raise
				self.q.put(GDO)
			except Exception, e:
				error = str(e)

		def __kill_proc(process_list):
			for process in process_list:
				process.join()

		per_server_process_spawning_time = time.time()
		for host in self.roledefs[role]:
			p = processing_object.new_process(
				__spawn,
				[self, host, task]
				)

			process_list.append(p)
		print '----------------'
		print 'per_server_process_spawning_time'
		print round((time.time() - per_server_process_spawning_time) * 1000, 1)
		spawned_process_join_time = time.time()
		__kill_proc(process_list)
		print 'spawned_process_join_time'
		print round((time.time() - spawned_process_join_time) * 1000, 1)
