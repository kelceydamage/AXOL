#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
from axol_common.classes.common_logger import CommonLogger
from axol_common.classes.common_data_object import GenericDataObject
from axol_common.classes.common_resource import CommonResource
from axol_common.distributed.axol_roledefs import generate_base_roles
from classes.axol_resource import AxolResource
from axol_config import api
from task_engine.TaskEngine import DW
from aapi.aapi import app as app
from flask import jsonify
from flask import request
from ast import literal_eval

class ResourceRestoreAlertServers(AxolResource):
	"""docstring for ResourceRestoreAlertServers
	Must implement:
		_show_help
		self.methods = {<method_type>: function}
		self.source = {keyword}
		request_{keyword}_api
		calculate_new_fields
	"""
	required_post = {
		'network': (True, u's'),
		'profile': (False, u's')
		}

	def __init__(self):
		super(ResourceRestoreAlertServers, self).__init__()
		self.source = 'restore_alert_servers'
		self.local = True

	def _show_help(self):
		return {
			'Help': {
				'api': '/api/restore_alert_servers',
				'method': 'POST',
				'required data': {
					'network': '<internal, external>'
					},
				'version': api
				}
			}

	@staticmethod
	@app.route('/api/restore_alert_servers', methods=['POST', 'GET'])
	def api_restore_alert_servers():
		if request.method == 'GET':
			return jsonify(ResourceRestoreAlertServers()._show_help())
		try:
			data = CommonResource.handle_request(request, ResourceRestoreAlertServers.required_post)
		except Exception, e:
			CommonLogger.log(e, 'restore_alert_servers', 'api_restore_alert_servers')
			return jsonify({'response': {'error': str(e)}})
		try:
			roledefs = generate_base_roles(data.network)
			DW.cache_key_set('roledefs', roledefs)
			roledefs = literal_eval(DW.cache_key_get('roledefs'))
			server_dict = ResourceRestoreAlertServers.create_server_list(roledefs, 'production_servers')
		except Exception, e:
			CommonLogger.log(e, 'restore_alert_servers', 'api_restore_alert_servers')
			return jsonify({'response': {'error': str(e)}})
		return jsonify({'response': {'alert_servers': server_dict}})
