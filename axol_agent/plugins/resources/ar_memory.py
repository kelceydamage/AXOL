#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

class ARMemory(object):
	function = ['cat', '/proc/meminfo']

	def __init__(self, data):
		self.data = data

	def format(self):
		# Must retuirn a valid dict for json formatting
		self.data = self.data.split('\n')
		self.data.pop(-1)
		response = {}
		for value in self.data:
			value = value.replace('(', '_').replace(')', '')
			value_list = value.strip(' ').split(':')
			response[value_list[0].lower()] = int(value_list[1].strip(' ').strip(' kB'))
		response['memused'] = response['active']

		return response
