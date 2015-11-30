#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
import elasticsearch
import time
import random
from datetime import datetime
from base32encode import base10_to_base_x, format_record_id
from transaction import body, merchant_id_randomizer

import os, re, sys, subprocess

import sys, os
from multiprocessing import Pool, Process, Queue, freeze_support, cpu_count

# Processing Class
#-----------------------------------------------------------------------#

class Processing(object):
	"""docstring for NewProcess"""
	def __init__(self):
		super(Processing, self).__init__()
		pass

	def create_queue(self):
		queue = Queue()
		return queue

	def generate_pool(self, processes):
		pool = Pool(processes=4)
		return pool

	def new_process_pool(self, pool, func, data):
		result = pool.apply_async(func, args=data)
		return result

	def new_process(self, func, data):
		process = Process(target=func, args=data)
		process.start()
		return process

	def new_process_map(self, pool, func, data, data2='', data3=''):
		result = pool.map(func, [data])
		return result

node = 'Elasticsearch:80'

es = elasticsearch.Elasticsearch(node)

dt = datetime.utcnow()
date = int(dt.strftime('%d%m%Y'))
time = int(dt.strftime('%H%M%S'))
ms = str(dt.strftime('%f'))[:4]

def set_temp_files():
	m = [
		1092,
		9281,
		3,
		32,
		526,
		876,
		82,
		93586,
		2568285,
		2658
		]
	for i in m:
		f = open(str(i), 'w')
		f.write('0')
		f.close()

def index_record(body, node):
	es = elasticsearch.Elasticsearch(node)

	def counter(m):
		f = open(str(m), 'r')
		c = f.read()
		#print c
		f.close()
		c = int(c) + 1
		print c
		f = open(str(m), 'w')
		f.write(str(c))
		f.close 
		#c1 = 0
		c2 = 0
		c3 = 0
		c4 = 0
		return c

	def index(es, converted_id, m, body):
		x = random.uniform(40.00, 60000.99)
		x1 = random.uniform(20.00, x)
		x2 = random.uniform(10.00, x1)
		body['Amount'] = round(random.uniform(2.00, x2), 2)

		es.index(
			index='test',
			doc_type=m,
			id=converted_id,
			body=body
			)
		#return response

	m = merchant_id_randomizer()

	converted_id = format_record_id(
		base10_to_base_x(date, 32),
		base10_to_base_x(time, 32),
		base10_to_base_x(int(ms), 32),
		base10_to_base_x(m, 32),
		base10_to_base_x(counter(m), 32)
		)

	result = index(
		es,
		converted_id,
		m,
		body
		)
	#print result
	#return result

'''
t = 0
while t < 10:
	index_record(
		es, 
		body
		)
	t += 1
'''


'''
# 1000 / 58 TPS
index_record(
	es, 
	body
	)
'''

def _child_process(proc, func, data):
	process_list = []
	for z1 in range(200):
		p = proc.new_process(
			func,
			data
			)

		process_list.append(p)

	for process in process_list:
		process.join()

if __name__ == '__main__':
	freeze_support()

	
	p = Processing()
	pool = p.generate_pool(20)
	for x in range(40):
		response = p.new_process_pool(
			pool,
			index_record,
			(body, node)
			)
	
	pool.close()
	pool.join()
	
	'''
	w1 = 0
	proc = Processing()
	q = proc.create_queue()
	
	
	while w1 < 1:
		for z1 in range(40):
			p = proc.new_process(
				index_record,
				(body, node)
				)
		p.join()
		w1 += 1
	'''
	'''
	while w1 < 1:
		p1 = proc.new_process(
			_child_process, [
				proc,
				index_record,
				(body, node)
				]
			)

		#try:
			#queue_response = q.get(timeout=0.1)
			#response[queue_response[0]] = queue_response[1]
		#except Exception, e:
		#	print e

		
		w1 += 1
	p1.join()
	'''

	'''
	print cpu_count()
	while True:
		if response.ready() == True:
			print response.ready()
			#pool.close()
			#pool.join()
			break
	'''
	#print response.get()

	# 1000 / 20.9 = 47 TPS
	# 3000 / 59.2 = 50.67 TPS
'''
set_temp_files()
'''