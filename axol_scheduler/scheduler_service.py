#! /usr/bin/env python
#-----------------------------------------#
# Copyright [2015] [Kelcey Jamison-Damage]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Imports
#-----------------------------------------------------------------------#

from __future__ import with_statement
from flask import jsonify
from flask import request
from flask import Flask
import time
import datetime
from client.wrapper import call_function_api
from scheduler import *
from axol_config import axol_node

# Application Instantiation
#-----------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object(__name__)
scheduler = Scheduler()

# Utility functions
#-----------------------------------------------------------------------#

def filter_task_response(response):
	receipt_list = {}
	for receipt in response['value']:
		receipt_list[receipt] = response['value'][receipt]
	response['value'] = {}
	for receipt in receipt_list:
		task = receipt_list[receipt]
		response['value'][receipt] = {}
		response['value'][receipt]['task_name'] = task.name
		response['value'][receipt]['Scheduled_Time'] = task.scheduled_time
		response['value'][receipt]['Start_Time'] = task.start_time
		response['value'][receipt]['Interval'] = task.time_interval
		response['value'][receipt]['Halt_Flag'] = task.halt_flag.is_set()
		response['value'][receipt]['Receipt'] = receipt
		response['value'][receipt]['Tasks'] = str(task.func)
		task = ''
	print response
	#response['value']['tasks'] = str(receipt_list)
	return response

# Base API
#-----------------------------------------------------------------------#

@app.route('/api/version', methods=['GET'])
def request_version():
	response = {'value': {}}
	response['value']['name'] = 'AXOL Scheduler Node'
	response['value']['version'] = 'v1.1.1'
	return response

# Scheduler API
#-----------------------------------------------------------------------#

@app.route('/api/get_scheduled_tasks', methods=['POST'])
def request_list_scheduler_tasks():
	response = {'value': {}}
	response['value'] = scheduler.list()
	response = filter_task_response(response)
	return jsonify(response)

@app.route('/api/scheduler/start', methods=['GET'])
def request_start_scheduler():
	response = {'value': {}}
	response['value'] = scheduler.run()
	return jsonify(response)

@app.route('/api/scheduler/halt', methods=['GET'])
def request_halt_scheduler():
	response = {'value': {}}
	response['value'] = scheduler.halt()
	return jsonify(response)

@app.route('/api/remove_scheduled_task', methods=['POST'])
def request_unschedule():
	if 'task_name' not in request.json:
		return jsonify({'error': 'missind required field: task_name'})
	task_name = str(request.json["task_name"])
	response = {'value': {}}
	receipts = scheduler.list()
	if len(receipts) > 0:
		for receipt in receipts:
			print receipts
			print receipt
			if receipts[receipt].name == task_name:
				print 'Found: %s' % receipt
				scheduler.drop(receipt)
				response['value'] = scheduler.list()
				response['notice'] = (
					'Succeeded in removing task: Task with name '
					'%s has been removed from the scheduler' % task_name
					)
				response = filter_task_response(response)
				print jsonify(response)
				return jsonify(response)
			else:
				response['value'] = scheduler.list()
				response['notice'] = (
					'Failed to remove task: Task with name '
					'%s could not be found' % task_name
					)
				response = filter_task_response(response)
				print jsonify(response)
				return jsonify(response)
	else:
		response['value'] = scheduler.list()
		response['notice'] = (
			'Failed to remove task: There are no more '
			'tasks to be removed'
			)
		response = filter_task_response(response)
		print jsonify(response)
		return jsonify(response)

@app.route('/api/create_scheduled_task', methods=['POST'])
def request_schedule_task():
	response = {'value': {}}
	if not request.json:
		abort(400)
	data = request.json
	time_int = int(data['time'])
	try:
		scheduler.schedule(
			str(data['task_name']),
			datetime.datetime.now(),
			every_x_secs(time_int),
			time_int,
			call_function_api,
			axol_node,
			str(data['api_name']),
			'method',
			str(data['role'])
			)
	except Exception, e:
		print '<error>: %s' % e
	response['value'] = 'Task has been scheduled, %s' % data['task_name']
	print jsonify({'response': response})
	return jsonify({'response': response})

# Application Start
#-----------------------------------------------------------------------#

scheduler.schedule(
	'init_task',
	datetime.datetime.now(),
	every_x_secs(3600),
	3600,
	call_function_api,
	axol_node,
	'admin',
	'usage',
	'local_debug'
	)
scheduler.start()
scheduler.halt()

if __name__ == '__main__':

	app.debug = True
	app.run(host='0.0.0.0')

