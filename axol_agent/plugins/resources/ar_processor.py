#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

class ARProcessor(object):
	function = ['a=`cat /proc/loadavg`; a="$a `nproc`"; echo $a']

	def __init__(self, data):
		self.data = data

	def format(self):
		# Must retuirn a valid dict for json formatting
		self.data = self.data.split()
		response = {
			'one_minute': self.data[0],
			'five_minute': self.data[1],
			'fifteen_minute': self.data[2],
			'scheduled_to_run': self.data[3],
			'total_processes': int(self.data[4]),
			'number_of_processing_units': int(self.data[5])
			}

		return response
