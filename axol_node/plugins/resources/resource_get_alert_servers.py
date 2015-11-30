#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
from axol_common.classes.common_data_object import GenericDataObject
from axol_common.classes.common_resource import CommonResource
from axol_common.classes.common_logger import CommonLogger
from classes.axol_resource import AxolResource
from axol_config import api
from aapi.aapi import app as app
from flask import jsonify
from flask import request
from task_engine.TaskEngine import DW
from ast import literal_eval

class ResourceGetAlertServers(AxolResource):
	"""docstring for ResourceGetAlertServers
	Must implement:
		_show_help
		self.methods = {<method_type>: function}
		self.source = {keyword}
		request_{keyword}_api
		calculate_new_fields
	"""
	required_post = {
		'profile': (False, u's')
		}

	def __init__(self):
		super(ResourceGetAlertServers, self).__init__()
		self.source = 'get_alert_servers'
		self.local = True

	def _show_help(self):
		return {
			'Help': {
				'api': '/api/get_alert_servers',
				'method': 'POST',
				'required data': 'None',
				'version': api
				}
			}

	@staticmethod
	@app.route('/api/get_alert_servers', methods=['POST', 'GET'])
	def api_get_alert_servers():
		if request.method == 'GET':
			return jsonify(ResourceGetAlertServers()._show_help())
		try:
			data = CommonResource.handle_request(request, ResourceGetAlertServers.required_post)
		except Exception, e:
			CommonLogger.log(e, 'get_alert_servers', 'api_get_alert_servers')
			return jsonify({'response': {'error': str(e)}})
		try:
			roledefs = literal_eval(DW.cache_key_get('roledefs'))
			server_dict = ResourceGetAlertServers.create_server_list(roledefs, 'production_servers')
		except Exception, e:
			CommonLogger.log(e, 'get_alert_servers', 'api_get_alert_servers')
			return jsonify({'response': {'error': str(e)}})
		return jsonify({'response': {'alert_servers': server_dict}})
