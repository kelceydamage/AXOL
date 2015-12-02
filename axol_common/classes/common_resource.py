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

from common_data_object import GenericDataObject
from common_logger import CommonLogger
import time
from flask import jsonify

class CommonResource(object):

	def __init__(self):
		super(AxolResource, self).__init__()
		pass

	@staticmethod
	def handle_request(request, params):
		request_dict = dict(request.json)
		len_r = len(request_dict)
 		len_p = len(params)
 		if len_r > len_p:
			raise Exception('Too many fields in POST request, got: %s, max: %s' % (len_r, len_p))
		for key in params:
			if params[key][0] == True and key not in request_dict:
				raise Exception('Missing field: %s' % key)
			elif key in request_dict and type(params[key][1]) != type(request_dict[key]):
				raise Exception('field: %s is of the wrong type, expect: %s, got: %s' % (
					key, type(params[key][1]),
					type(request_dict[key]))
					)
		for key in request_dict:
			if key not in params:
				raise Exception('Invalid field: %s' % key)
		if 'role' not in request_dict:
			request_dict['role'] = 'local_debug'
		data = GenericDataObject(request_dict)
		return data

	@staticmethod
	def try_catch(func, args):
		try:
			return func(args)
		except Exception, e:
			CommonLogger.log(e, str(func), 'tc')

	def list_all_attributes(self):
		for value in (value for value in dir(self) if '__' not in value):
			print value

	def generate_id(self, time):
		time = time[0:10] + '.' + time[11:26]
		return time
