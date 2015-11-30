#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

class ARTransactionMimic(object):
	def __init__(self, data):
		self.data = data

	def validate(self):
		response = {
			'value': self.data
			}

		print response

		return response
