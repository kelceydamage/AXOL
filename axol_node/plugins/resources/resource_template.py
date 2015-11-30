#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
from axol_common.classes.common_logger import CommonLogger
from axol_common.classes.common_data_object import GenericDataObject
from axol_common.classes.common_resource import CommonResource
from classes.axol_resource import AxolResource
from axol_config import api
from aapi.aapi import app as app
from flask import jsonify

# Plugin class
#-----------------------------------------------------------------------#
class ResourceTemplate(AxolResource):
	"""docstring for ResourceTemplate
	Must implement:
		_show_help
		self.local = <boolean> for using the agents or not
		self.source = <keyword>
		request_<keyword>_api
	"""
	required_post = {
		'profile': (False, u's')
		}

	def __init__(self):
		super(ResourceTemplate, self).__init__()
		self.source = 'cpu'

		# set to False if you want to use an Agent plugin and role based execution
		self.local = True

	def _show_help(self):
		# example help returned on 'GET' request
		return {
			'Help': {
				'api': '/api/get_null',
				'method': 'POST',
				'required data': {
					'network': '<internal, external>'
					},
				'version': api
				}
			}

	# This is a copy and paste method for establishing an API endpoint
	# Expects 'role'
	@staticmethod
	@app.route('/api/get_null', methods=['GET', 'POST'])
	def request_cpu_api():
		# Return help for 'GET' requests
		if request.method == 'GET':
			return jsonify(ResourceGetProductionServers()._show_help())

		# data is an object with all your first level POST fields as attributes
		data = CommonResource.handle_request(request, ResourceGetProductionServers.required_post)

		try:

# Add your request handling code here
#-----------------------------------------------------------------------#

			# use this if you have an agent plugin and want to execute async tasks
			response = ResourceTemplate().create_async_job(data)

# Built-in error handling
#-----------------------------------------------------------------------#
		except Exception, e:
			CommonLogger.log(e, self.source, 'request_cpu_api')
			return jsonify({'response': {'error': str(e)}})

# Send response to browser
#-----------------------------------------------------------------------#
		return jsonify({'response': response})

	# this is the entry point for any custom code if using  async tasks
	def calculate_new_fields(self, response_object):
		return response_object



