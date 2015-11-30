#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
from distributed import socket_client
from sys import getsizeof
import time

# Class
#-----------------------------------------------------------------------#

class AxolTask(object):
	"""This is that standard task object that is used by Axol for every task"""
	def __init__(self):
		super(AxolTask, self).__init__()
		self.response = ''
		self.time = ''
		self.value = {}
		self.source = ''
		self.warnings = {'status': 0}
		self.warnings_counter = 0
		self.trigger = 0
		self.role = ''
		self.func = ''
		self.args = []
		self.resource = None

	def execute(self, roledefs):
		self = socket_client.AgentClient(roledefs).agent_query(self)
		self.execute_profile = {
			'client_setup': round(self.client_setup_time * 1000, 1),
			'process_spawner': round(self.process_spawner_time * 1000, 1),
			'queue_reduction': round(self.queue_reduction_time * 1000, 1),
			'queue_reduction_internals': {
				'look_up_server_name': round(self.match_name_time * 1000, 1),
				'calculate_new_fields': round(self.calculate_new_fields_time * 1000, 1),
				'gdo_creation_overhead': round((self.gdo_time - (
					self.calculate_new_fields_time + self.match_name_time
					)) * 1000, 1),
				'network_client_overhead': round((self.queue_reduction_time - sum([
					self.match_name_time,
					self.calculate_new_fields_time,
					self.gdo_time,
					self.socket_client_init_time,
					self.socket_client_connect_time,
					self.socket_client_send_time,
					self.socket_client_recv_time
					])) * 1000, 1),
				'socket_client_init': round(self.socket_client_init_time * 1000, 1),
				'socket_client_connect': round(self.socket_client_connect_time * 1000, 1),
				'socket_client_send': round(self.socket_client_send_time * 1000, 1),
				'socket_client_recv': round(self.socket_client_recv_time * 1000, 1)
				},
			'process_join': round(self.process_join_time * 1000, 1)
			}

	def execute_local(self, roledefs):
		self.value = {}
		for server in roledefs[self.role]:
			self.value[socket_client.AgentClient(roledefs)._match_name(server)] = {}
		print '### starting RT'
		self = self.resource.run_task(self)
		self.execute_profile = {}

	def write_data(self):
		self.resource.write_to_database(self.value)

	def post_process(self):
		self.value = self.resource.post_processing(self.value)

	def profiler(self):
		if self.resource.profiler == True:
			profiler_time = time.time()
			profiler = {'axol_node': {}, 'api_node': {}}
			profiler['axol_node'] = {
				'task_payload_execution': round(self.task_payload_execution_time * 1000, 1),
				'task_payload_execution_internals': self.execute_profile,
				'database_write':  round((self.database_write_time * 1000), 1),
				'post_process':  round((self.post_process_time * 1000), 1),
				'task_engine_overhead':  round(((self.async_job_time - sum([
					self.task_payload_execution_time,
					self.database_write_time,
					self.post_process_time
					])) * 1000), 1),
				'queue_time':  round((self.time * 1000), 1),
				'async_job_overhead':  round(((self.create_async_time - sum([
					self.time,
					self.async_job_time
					])) * 1000), 1),
				'total_time':  round((self.create_async_time * 1000), 1)
				}
			temp_list = []
			for key in self.execute_profile:
				if type(self.execute_profile[key]) != dict:
					temp_list.append(self.execute_profile[key])
			profiler['axol_node']['task_payload_execution_internals']['execution_overhead'] = round(
				(self.task_payload_execution_time * 1000) - sum(temp_list), 1
				)
			profiler['profiler_time'] = round((time.time() - profiler_time) * 1000, 1)
			return profiler
		else:
			return False

	def format_response(self):
		self.response = {
			'response': {
				'value': self.value,
				'profiler': self.profiler()
				},
			'source': self.source,
			'warnings': self.warnings
			}
		return self.response
