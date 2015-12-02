#! /usr/bin/env python
#-----------------------------------------#
#Copyright [2015] [Kelcey Jamison-Damage]

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

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

class ResourceCreateLogEntry(AxolResource):
	"""docstring for ResourceCreateLogEntry
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
		'log': (True, True),
		'profile': (False, U's')
		}

	def __init__(self):
		super(ResourceCreateLogEntry, self).__init__()
		self.source = 'log_entry'
		self.local = True
		self.store = False
		self.profiler = True

	def _show_help(self):
		return {
			'help': {
				'usage': '/api/create_log_entry',
				'method': 'POST',
				'required_data': {
					'alert_type': '<list of prefered types>',
					'source': '<type of event>',
					'group': '<group name>',
					'data': '<some json>',
					'log': 'True or False'
					},
				'version': api
				}
			}

	@staticmethod
	@app.route('/api/create_log_entry', methods=['GET', 'POST'])
	def api_create_log_entry():
		if request.method == 'GET':
			return jsonify(ResourceCreateLogEntry()._show_help())
		try:
			data = CommonResource.handle_request(
				request=request,
				params=ResourceCreateLogEntry.required_post
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='create_log_entry',
				method='api_create_log_entry-1'
				)
			return jsonify(report)
		try:
			response = ResourceCreateLogEntry().create_async_job(
				data=data
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='create_log_entry',
				method='api_create_log_entry-2'
				)
			return jsonify(report)
		return jsonify(response)

	def run_task(self, AxolTask):
		AxolTask.name = 'log_entry'
		AxolTask.api = api
		AxolTask.api['api_name'] = 'create_log_entry'
		self.store = AxolTask.data['log']
		if AxolTask.data['alert_type'] != []:
			try:
				ResourceCreateLogEntry().send_notice(
					name=AxolTask.name,
					data=AxolTask.data,
					group=AxolTask.data['group'],
					alert_type=AxolTask.data['alert_type']
					)
			except Exception, e:
				print 'ERROR: RCL notice: %s' % e
				status = 'incomplete'
				CommonLogger.log(e, 'create_log_entry', 'api_create_log_entry')
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
		AxolTask.value[AxolTask.name]['event']['name'] = AxolTask.name
		AxolTask.value[AxolTask.name]['event']['alert_type'] = AxolTask.data['alert_type']
		AxolTask.value[AxolTask.name]['event']['email_group'] = AxolTask.data['group']
		AxolTask.value[AxolTask.name]['event']['source'] = AxolTask.data['source']
		return AxolTask

	def calculate_new_fields(self, response_object):
		return response_object

	def post_processing(self, axol_task_value):
		axol_task_value['log_entry'] = axol_task_value['log_entry']['event']
		return axol_task_value

	def write_to_database(self, axol_task_value):
		if self.store == True:
			self.query([
				insert(
					data_object=axol_task_value,
					table_space='axol_logs.%s' % axol_task_value['log_entry']['source']
					)]
				)

