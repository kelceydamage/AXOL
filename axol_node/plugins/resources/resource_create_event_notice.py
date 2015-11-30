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
from axol_config import api
from aapi.aapi import app as app
from flask import jsonify, Flask
from flask import request

class ResourceCreateEventNotice(AxolResource):
	"""docstring for ResourceCreateEventNotice
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
		'alert_type': (True, []),
		'source': (True, U's'),
		'group': (True, U's'),
		'data': (True, {}),
		'profile': (False, U's')
		}

	def __init__(self):
		super(ResourceCreateEventNotice, self).__init__()
		self.source = 'events'
		self.local = True
		self.store = True
		self.profiler = True

	def _show_help(self):
		return {
			'help': {
				'usage': '/api/create_event_notice',
				'method': 'POST',
				'required_data': {
					'alert_type': '<list of prefered types>',
					'source': '<type of event>',
					'group': '<group name>',
					'data': '<some json>',
					},
				'version': api
				}
			}

	@staticmethod
	@app.route('/api/create_event_notice', methods=['GET', 'POST'])
	def api_create_event_notice():
		if request.method == 'GET':
			return jsonify(ResourceCreateEventNotice()._show_help())
		try:
			data = CommonResource.handle_request(
				request=request,
				params=ResourceCreateEventNotice.required_post
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='create_event_notice',
				method='api_create_event_notice-1'
				)
			return jsonify(report)
		try:
			response = ResourceCreateEventNotice().create_async_job(
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
		AxolTask.name = 'event_notice'
		AxolTask.api = api
		AxolTask.api['api_name'] = 'create_event_notice'
		if AxolTask.data['alert_type'] != []:
			try:
				ResourceCreateEventNotice().send_notice(
					name=AxolTask.name,
					data=AxolTask.data,
					group=AxolTask.data['group'],
					alert_type=AxolTask.data['alert_type']
					)
			except Exception, e:
				status = 'incomplete'
				CommonLogger.log(e, 'create_event_notice', 'api_create_event_notice')
		AxolTask.value = {
			AxolTask.name: {
				'name': AxolTask.name,
				'source': AxolTask.data['source'],
				'email_group': AxolTask.data['group'],
				'alert_type': AxolTask.data['alert_type'],
				'event': AxolTask.data['data'],
				'api': AxolTask.api
				}
			}
		return AxolTask

	def calculate_new_fields(self, response_object):
		return response_object

	def post_processing(self, axol_task_value):
		return axol_task_value

	def write_to_database(self, axol_task_value):
		self.query([
			insert(
				data_object=axol_task_value,
				table_space='axol_metrics.event_notices'
				)]
			)
