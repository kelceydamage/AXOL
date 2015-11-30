#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

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
