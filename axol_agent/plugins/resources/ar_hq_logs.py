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
from datetime import datetime

class ARHQLogs(object):
	function = [
		'sudo tail -n 200 /home/sites/api/logs/error.log | grep "%s" | grep -i mandrill' \
		% str(datetime.now())[8:15]
		]

	def __init__(self, data):
		self.data = data

	def format(self):	# Must retuirn a valid dict for json formatting
		if 'mandrill' not in self.data:
			response = {}
			response['error_count'] = 0

			return response

		response = {}
		self.data = self.data.split('\n')
		self.data.pop()
		line = self.data[-1].split(' ERROR - ')
		response['log_time'] = line[0]
		user = line[1].split(':')
		response['user'] = user[0]
		data = user[1:]
		print data
		response['error_type'] = data[3]
		response['trace'] = '%s %s' % (data[3], data[4])
		response['error_count'] = 1

		return response

print str(datetime.now())[8:15]
