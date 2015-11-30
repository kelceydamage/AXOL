#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

class ARHeartbeat(object):
	function = ['echo', 'i am alive']

	def __init__(self, data):
		self.data = data

	def format(self):
		# Must retuirn a valid dict for json formatting
		response = {
			'status': self.data.strip('\n')
			}

		return response

