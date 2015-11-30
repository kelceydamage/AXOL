#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
from axol_common.classes.common_logger import CommonLogger
from classes.axol_resource import AxolResource
from aapi.aapi import app as app
from flask import jsonify, Flask
from task_engine.TaskEngine import DW
from lmdb import *
from ast import literal_eval
import time

class ResourceDashboard(AxolResource):
	"""docstring for ResourceDashboard
	Must implement:

	"""

	def __init__(self):
		super(ResourceDashboard, self).__init__()
		pass

	@staticmethod
	@app.route('/api/readonly/dashboard/', methods=['GET'])
	def request_dashboard_api():
		sources = [
			'cpu',
			'memory',
			'disk',
			'mysql',
			'mean',
			'deviation_pos',
			'deviation_neg'
			]
		t = time.time()
		response = DW.cache_key_get('roledefs')
		warnings = DW.cache_key_get('ro_warnings')
		server_dict = ResourceDashboard().create_server_list(
			literal_eval(response),
			'production_servers'
			)
		response_dict = {
			'response': {
				'value': {}
				},
			'warnings': {}
			}
		response_dict['warnings'] = literal_eval(warnings)
		error_dict = {}
		for server in server_dict:
			response_dict['response']['value'][server] = {}
			for source in sources:
				key = 'ro_%s_%s' % (source, server)
				try:
					response = DW.cache_key_get(key)
					response_dict['response']['value'][server][source] = literal_eval(response)
				except Exception, e:
					error_dict[key] = str(e)
		if error_dict != {}:
			CommonLogger.log(error_dict, 'dashboard', 'request_dashboard_api')
		t2 = time.time()
		t3 = t2 - t
		response_dict['response']['time'] = round(t3, 4)
		print 'complete'
		try:
			return jsonify(response_dict)
		except Exception, e:
			CommonLogger.log(str(e), 'dashboard', 'request_dashboard_api')
			print e




