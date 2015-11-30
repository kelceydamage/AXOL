#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

class ARJavaLogs(object):
	function = ['curl -u log-admin:PASSWORD@1 http://127.0.0.1:8081/metrics']

	def __init__(self, data):
		self.data = data

	def format(self):
		# Must retuirn a valid dict for json formatting
		response = self.data

		return response
