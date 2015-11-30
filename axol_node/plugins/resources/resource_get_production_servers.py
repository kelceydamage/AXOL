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
from aapi.aapi import app as app
from flask import jsonify
from flask import request

class ResourceGetProductionServers(AxolResource):
	"""docstring for ResourceGetProductionServers
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
		super(ResourceGetProductionServers, self).__init__()
		self.source = 'get_production_servers'
		self.local = True

	def _show_help(self):
		return {
			'Help': {
				'api': '/api/get_production_servers',
				'method': 'POST',
				'required data': {
					'network': '<internal, external>'
					},
				'version': api
				}
			}

	@staticmethod
	@app.route('/api/get_production_servers', methods=['POST', 'GET'])
	def api_get_production_servers():
		if request.method == 'GET':
			return jsonify(ResourceGetProductionServers()._show_help())
		try:
			data = CommonResource.handle_request(request, ResourceGetProductionServers.required_post)
		except Exception, e:
			CommonLogger.log(e, 'get_production_servers', 'api_get_production_servers')
			return jsonify({'response': {'error': str(e)}})
		try:
			roledefs = generate_base_roles(data.network)
			server_dict = ResourceGetProductionServers.create_server_list(roledefs, 'production_servers')
		except Exception, e:
			CommonLogger.log(e, 'get_production_servers', 'api_get_production_servers')
			return jsonify({'response': {'error': str(e)}})
		return jsonify({'response': {'production_servers': server_dict}})
