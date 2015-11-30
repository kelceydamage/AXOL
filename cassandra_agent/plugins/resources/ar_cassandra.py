#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

import time
import sys
import collections

class ARCassandra(object):
	def __init__(self, data):
		self.data = data

	def submit(self, session):
		for command in self.data['commands']:
			try:
				result = session.execute(command)
			except Exception, e:
				print 'ERROR: %s' % e
		return result

	def format(self, result):
		return {'response': result}
