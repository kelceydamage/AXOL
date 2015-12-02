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




