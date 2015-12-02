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
import sys
sys.path.append("/opt/AXOL_Management/AXOL/axol_common")
from common_client import CommonClient
from config.common_config import axol_node
import urllib2
import json
import subprocess
import time

# Core Application Class
#-----------------------------------------------------------------------#

class CommonLogger(object):
	"""docstring for Logger"""
	host = subprocess.Popen(
		['hostname', '-I'],
		stdout=subprocess.PIPE,
		stdin=subprocess.PIPE,
		shell=False
		)

	def __init__(self):
		pass

	@staticmethod
	def log(error, source, method):
		data = {
			'alert_type': ['email'],
			'source': 'axol_events',
			'group': 'default',
			'data': {'error': str(error), 'source': source, 'method': method}
			}
		try:
			sent_log = CommonClient.call_api(
				'create_event_notice',
				data,
				axol_node
				)
			print 'LOGGER: %s' % sent_log
			return sent_log
		except Exception, e:
			sent_log = {'response': {'logger_error': e}}
			print 'LOGGER ERROR: %s' % e
			return sent_log

	@staticmethod
	def size():
		pass

	@staticmethod
	def time_stamp(timer):
		return time.time() - timer

	@staticmethod
	def time_start():
		return time.time()

