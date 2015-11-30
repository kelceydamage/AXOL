#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

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



