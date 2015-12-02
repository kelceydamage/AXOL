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
sys.path.append("..")
from axol_config import axol_node
import json

def call_function_api(axol_node, api_name, role):
	print 'http://%s/api/%s' % (axol_node, api_name)
	url = 'https://%s/api/%s' % (axol_node, api_name)
	data = json.dumps({"role": "%s" % role})
	request = urllib2.Request(url, data)
	request.add_header('Content-Type', 'application/json')
	response = urllib2.urlopen(request)
	return response.read()

