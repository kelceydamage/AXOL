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

class ARService(object):
	function = ['service', '--status-all']

	def __init__(self, data):
		self.data = data

	def format(self):
		# Must retuirn a valid dict for json formatting
		self.data = self.data.split('\n')
		self.data.pop(-1)
		response = {}
		for line in self.data:
			line = line.split('  ')
			if re.search(r'\+', line[0]):
				response[line[1]] = 'running'
			else:
				response[line[1]] = 'stopped'

		return response

