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

class ARGetRecentTransactions(object):
	password = 'PASSWORD'
	command = 'show global status'
	function = ['mysql -u user --password="%s" -e "%s" ' % (password, command)]

	def __init__(self, data):
		self.data = data

	def format(self):
		# Must retuirn a valid dict for json formatting
		if self.data == '':
			response = {
				'error': 'unable to connect to the MySQL service'
				}

			return response

		self.data = self.data.split('\n')
		self.data.pop(0)
		self.data.pop(-1)
		response = {}
		for line in self.data:
			name, value = line.split('\t')
			try:
				response[name.lower()] = int(value)
			except Exception, e:
				response[name.lower()] = value

		return response



