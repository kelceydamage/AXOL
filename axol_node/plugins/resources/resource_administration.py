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
from axol_common.classes.common_data_object import GenericDataObject
from axol_common.classes.common_resource import CommonResource
from axol_common.distributed.axol_roledefs import generate_base_roles
from classes.axol_resource import AxolResource
from axol_config import api
from task_engine.TaskEngine import DW
from aapi.aapi import app as app
from flask import jsonify, Flask
from flask import request
from ast import literal_eval

class ResourceAdmin(AxolResource):
	"""docstring for ResourceProcessor
	Must implement:
		_show_help
		self.source = {keyword}
		request_{keyword}_api
		calculate_new_fields
	"""

	def __init__(self):
		super(ResourceAdmin, self).__init__()
		self.source = 'version'
		self.local = True

	def _show_help(self):
		return {
			'Help': {
				'roles administration':{
					'api': '/api/system/admin/roles',
					'available_methods': {
						'POST':{
							'required data': [
								'network=<internal, external>',
								'action=<remove, list, list_ec2, restore>',
								'server_name=<name of server>'
								]
							}
						}
					}
				}
			}

	@staticmethod
	@app.route('/api/manage_alerts', methods=['POST', 'GET'])
	def request_admin_api():
		print request.method
		if request.method == 'GET':
			return jsonify(ResourceAdmin()._show_help())
		else:
			print request.json
			if not 'server_name' in request.json \
			or not 'action' in request.json \
			or not 'network' in request.json:
				return jsonify({'error': 'missing required data'})
			response_object = GenericDataObject(request.json)
			roledefs = literal_eval(DW.cache_key_get('roledefs'))
			if response_object.action == 'remove':
				changed_roles = {}
				try:
					for name in roledefs:
						if response_object.server_name in name:
							host = roledefs[name][response_object.network]
					for name in roledefs:
						if host in roledefs[name]:
							roledefs[name].remove(host)
							changed_roles[name] = roledefs[name]
					DW.cache_key_set('roledefs', roledefs)
				except Exception, e:
					return jsonify({'error':e})
				return jsonify({
					'host':host,
					'changed_roles': changed_roles
					})
			elif response_object.action == 'list':
				return jsonify(roledefs)
			elif response_object.action == 'restore':
				roledefs = generate_base_roles()
				DW.cache_key_set('roledefs', roledefs)
				return jsonify(roledefs)
			elif response_object.action == 'list_ec2':
				roledefs = generate_base_roles()
				return jsonify(roledefs)
