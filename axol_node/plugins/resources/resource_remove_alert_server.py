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
from axol_common.classes.common_logger import CommonLogger
from axol_common.classes.common_data_object import GenericDataObject
from axol_common.classes.common_resource import CommonResource
from classes.axol_resource import AxolResource
from axol_config import api
from aapi.aapi import app as app
from flask import jsonify
from flask import request
from task_engine.TaskEngine import DW
from ast import literal_eval

class ResourceRemoveAlertServer(AxolResource):
	"""docstring for ResourceRemoveAlertServer
	Must implement:
		_show_help
		self.methods = {<method_type>: function}
		self.source = {keyword}
		request_{keyword}_api
		calculate_new_fields
	"""
	required_post = {
		'server_name': (True, u's'),
		'profile': (False, u's')
		}

	def __init__(self):
		super(ResourceRemoveAlertServer, self).__init__()
		self.source = 'remove_alert_servers'
		self.local = True

	def _show_help(self):
		return {
			'Help': {
				'api': '/api/remove_alert_servers',
				'method': 'POST',
				'required data':  {
					'server_name': '<name of the server to remove>'
					},
				'version': api
				}
			}

	@staticmethod
	@app.route('/api/remove_alert_server', methods=['POST', 'GET'])
	def api_remove_alert_server():
		role = 'production_servers'
		if request.method == 'GET':
			return jsonify(ResourceRemoveAlertServer()._show_help())
		try:
			data = CommonResource.handle_request(request, ResourceRemoveAlertServer.required_post)
		except Exception, e:
			CommonLogger.log(e, 'remove_alert_server', 'api_remove_alert_server')
			return jsonify({'response': {'error': str(e)}})
		try:
			roledefs = literal_eval(DW.cache_key_get('roledefs'))
			server_dict = ResourceRemoveAlertServer.create_server_list(roledefs, role)
			if server_dict[data.server_name] in roledefs[role]:
				roledefs[role].remove(server_dict[data.server_name])
				DW.cache_key_set('roledefs', roledefs)
			if data.server_name in server_dict.keys():
				del server_dict[data.server_name]
		except Exception, e:
			CommonLogger.log(e, 'remove_alert_server', 'api_remove_alert_server')
			return jsonify({'response': {'error': str(e)}})
		return jsonify({'response': {'removed': data.server_name, 'alert_servers': server_dict}})
