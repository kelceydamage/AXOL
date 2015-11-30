#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

import sys, os, time
import time
from random import randint
from multiprocessing import Process, Pool, Queue

# Processing Class
#-----------------------------------------------------------------------#


class Processing(object):
	"""docstring for Processing"""
	def __init__(self):
		super(Processing, self).__init__()
		pass

# Processing wrapper methods
#-----------------------------------------------------------------------#

	def create_queue(self):
		queue = Queue()
		return queue

	def generate_pool(self, processes=4):
		pool = Pool(processes)
		return pool

	def new_process_pool(self, pool, func, data):
		result = pool.apply_async(func, data)
		return result

	def new_process(self, func, data):
		process = Process(target=func, args=data)
		process.start()
		return process

	def new_process_map(self, pool, func, data, data2='', data3=''):
		result = pool.map(func, [data])
		return result

