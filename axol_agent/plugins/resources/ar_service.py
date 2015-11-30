#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

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

