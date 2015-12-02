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
import urllib2
import sys
import json

# Main class || Client for accessing AXOL API
#-----------------------------------------------------------------------#
class CommonClient(object):
	"""docstring for CommonClient"""
	def __init__(self, host):
		super(CommonClient, self).__init__()
		pass

	@staticmethod
	def call_api(api_name, data, host):
		url = 'http://%s/api/%s' % (host, api_name)
		data = json.dumps(data)
		request = urllib2.Request(url, data)
		request.add_header('Content-Type', 'application/json')
		response = urllib2.urlopen(request)
		response_dict = json.loads(response.read())
		return response_dict
