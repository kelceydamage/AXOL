#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

import time

class Entry(object):
	def __init__(self, args):
		super(Entry, self).__init__()
		self.index = args[0]
		self.timestamp = args[1]
		self.time_since_last = args[2] 
		self.time_overall = args[3]

	def get_entry(self):
		return self.__dict__

class CommonTimer(object):
	def __init__(self):
		super(CommonTimer, self).__init__()
		self.time_log = []

	def start(self):
		data = (
			'start',
			time.time(),
			0,
			0
			)
		self.time_log.append(Entry(data).get_entry())

	def log(self, name):
		timestamp = time.time()
		tl = timestamp - self.time_log[-1]['timestamp']
		to = timestamp - self.time_log[0]['timestamp']
		data = (
			name,
			timestamp,
			str(tl),
			str(to)
			)
		self.time_log.append(Entry(data).get_entry())

	def get_log(self):
		exec_time_log = self.time_log
		self.time_log = []
		return exec_time_log

timer = CommonTimer()