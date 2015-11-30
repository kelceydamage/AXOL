#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
from axol_common.classes.common_timer import CommonTimer
from axol_common.classes.common_logger import CommonLogger
from axol_common.classes.common_resource import CommonResource
from axol_common.classes.common_data_object import GenericDataObject
from axol_common.database.cassandra_wrapper import insert
from classes.axol_resource import AxolResource
from task_engine.TaskEngine import DW
from axol_config import api
from aapi.aapi import app as app
from flask import jsonify, Flask
from flask import request
from ast import literal_eval

class ResourceSendWarningsAlerts(AxolResource):
	"""docstring for ResourceSendWarningsAlerts
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
		'profile': (False, U's'),
		'role': (False, U's')
		}

	def __init__(self):
		super(ResourceSendWarningsAlerts, self).__init__()
		self.source = 'alerts'
		self.local = True
		self.store = True
		self.profiler = True
		self.sources = [
			'cpu',
			'memory',
			'disk',
			]

	def _show_help(self):
		return {
			'help': {
				'usage': '/api/send_warnings_alerts',
				'method': 'POST',
				'required_data': {
					'role': '<some role>'
					},
				'version': api
				}
			}

	@staticmethod
	@app.route('/api/send_warnings_alerts', methods=['GET', 'POST'])
	def api_send_warnings_alerts():
		if request.method == 'GET':
			return jsonify(ResourceSendWarningsAlerts()._show_help())
		try:
			data = CommonResource.handle_request(
				request=request,
				params=ResourceSendWarningsAlerts.required_post
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='create_event_notice',
				method='api_create_event_notice-1'
				)
			return jsonify(report)
		try:
			response = ResourceSendWarningsAlerts().create_async_job(
				data=data
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='create_event_notice',
				method='api_create_event_notice-2'
				)
			return jsonify(report)
		return jsonify(response)

	def run_task(self, AxolTask):
		AxolTask.name = 'alerts'
		AxolTask.api = api
		AxolTask.api['api_name'] = 'send_warnings_alerts'
		AxolTask.value = {}
		warnings = {}
		for source in self.sources:
			warnings[source] = []
			key = '%s_warnings' % source
			print key
			try:
				value = literal_eval(DW.cache_key_get(key))
			except Exception, e:
				print 'ERROR RT: %s' % e
			for server in value:
				if type(value[server]) is dict:
					if server in AxolTask.value:
						AxolTask.value[server][source] = value[server]['error']
					else:
						AxolTask.value[server] = {source: value[server]['error']}
		ResourceSendWarningsAlerts().notification_threshold(
			AxolTask=AxolTask
			)
		return AxolTask

	def calculate_new_fields(self, response_object):
		return response_object

	def post_processing(self, axol_task_value):
		return axol_task_value

	def write_to_database(self, axol_task_value):
		pass
