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

import signal
import SocketServer
import subprocess
import socket
import ssl
import json
import os
import re
import sys
from plugins.plugin_registration import ar_methods
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from sys import getsizeof
import struct

class LocalTasks(object):
	methods = ar_methods

	@classmethod
	def run_task(cls, request):
		def gather_data(cls, request, method):
			response = cls.methods[method](request).submit(session)
			output = cls.methods[method](response).format(response)
			return output

		method = request['method']
		if method not in cls.methods:
			return 'Invalid Method'
		else:
			return gather_data(cls, request, method)

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	daemon_threads = True
	allow_reuse_address = True

	def server_bind(self):
		SocketServer.TCPServer.server_bind(self)

	def get_request(self):
		(socket, addr) = SocketServer.TCPServer.get_request(self)
		return (socket, addr)

class TCPHandler(SocketServer.BaseRequestHandler):
	white_list = [
		'127.0.0.1',
		'172.31.77.176',
		'10.1.1.1',
		'172.31.193.179',
		'172.31.'
		]
	api_version = {
		'version_name': 'Wonderboom',
		'version_number': '1.2.0'
		}

	def receive_all(self, socket, n):
		data = ''
		while len(data) < n:
			packet = socket.recv(n - len(data))
			if not packet:
				return None
			data += packet
		return data

	def receive_message(self, socket):
		raw_message_length = self.receive_all(socket, 4)
		if not raw_message_length:
			return None
		message_length = struct.unpack('>I', raw_message_length)[0]
		return self.receive_all(socket, message_length)

	def handle(self):
		self.data = self.receive_message(self.request)
		print 'RECV SIZE: %s' % getsizeof(self.data)
		for entry in self.white_list:
			if re.search(entry, self.client_address[0]):
				match_token = True
				break
		else:
			match_token = False
		if match_token == True:
			response = LocalTasks.run_task(json.loads(self.data.decode('base64','strict')))
			#response['api'] = self.api_version
			#response['api']['api_name'] = self.data
			request = str(json.dumps(response)).encode('base64','strict')
			request = struct.pack('>I', len(request)) + request
			self.request.sendall(request)
		else:
			request = str(json.dumps({'error': 'Connection Refused'})).encode('base64','strict')
			request = struct.pack('>I', len(request)) + request
			self.request.sendall(request)

def write_pid_file():
	pid = str(os.getpid())
	f = open('/var/run/cassandra_agent.pid', 'w')
	f.write(pid)
	f.close()

def exit_gracefully(signal, frame):
	sys.exit(0)

if __name__ == '__main__':
	write_pid_file()
	signal.signal(signal.SIGINT, exit_gracefully)
	cluster = Cluster(['172.31.255.12', '172.31.255.25', '172.31.255.36', '172.31.255.41'])
	session = cluster.connect('axol_metrics')
	session.row_factory = dict_factory
	session.default_timeout = 30
	HOST = socket.gethostbyname(socket.gethostname())
	PORT = 9999
	server = SimpleServer(('127.0.0.1', PORT), TCPHandler)
	server.serve_forever()
