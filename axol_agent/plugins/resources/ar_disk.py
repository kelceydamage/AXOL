#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

class ARDisk(object):
	function = ['df', '-h']

	def __init__(self, data):
		self.data = data

	def format(self):
		# Must retuirn a valid dict for json formatting
		self.data = self.data.split('\n')
		self.data.pop(0)
		self.data.pop(-1)
		response = {}
		n = 0
		for line in self.data:
			device, size, used, available, percent, mountpoint = line.split()
			if mountpoint == '/':
				mountpoint = '.root'
			if device == 'udev':
				device = '/udev'
			else:
				mountpoint = mountpoint.replace('/', '.')
			name = 'disk_%s' % n
			response[name] = {
				'mount_point': mountpoint[1:],
				'device': device,
				'size': size,
				'used': used,
				'free_space': available,
				'percent_used': str(percent.strip('%'))
				}
			n += 1

		return response
