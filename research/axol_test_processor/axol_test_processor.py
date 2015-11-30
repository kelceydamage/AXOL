#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

import SocketServer
import subprocess
import socket
import ssl
import json
import os
from plugins.plugin_registration import ar_methods

class LocalTasks(object):
	methods = ar_methods

	@classmethod
	def run_task(cls, data):

		return cls.methods['transaction'](data).validate()

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	daemon_threads = True
	allow_reuse_address = True

	def server_bind(self):
		SocketServer.TCPServer.server_bind(self)
		self.socket = ssl.wrap_socket(
			self.socket,
			server_side=True,
			certfile="/opt/AXOL_Management/AXOL/axol_agent/ssl/server_crt.pem",
			keyfile='/opt/AXOL_Management/AXOL/axol_agent/ssl/server_key.pem',
			do_handshake_on_connect=False,
			ssl_version=ssl.PROTOCOL_TLSv1
			)

	def get_request(self):
		(socket, addr) = SocketServer.TCPServer.get_request(self)
		socket.do_handshake()

		return (socket, addr)

class TCPHandler(SocketServer.BaseRequestHandler):
	white_list = [
		'127.0.0.1',
		'172.31.77.176',
		'10.1.1.1',
		'172.31.255.12'
		]
	api_version = {
		'version_name': 'Poplar',
		'version_number': '1.0.0b'
		}

	def handle(self):
		self.data = self.request.recv(1024).strip()
		if self.client_address[0] in self.white_list:
			response = LocalTasks.run_task(self.data)
			response['api'] = self.api_version
			response['api']['api_name'] = self.data
			self.request.sendall(json.dumps(response))
		else:
			self.request.sendall(json.dumps({'error': 'Connection Refused'}))

def write_pid_file():
		pid = str(os.getpid())
		f = open('/var/run/axol_agent.pid', 'w')
		f.write(pid)
		f.close()

if __name__ == '__main__':
		write_pid_file()
		HOST = socket.gethostbyname(socket.gethostname())
		PORT = 443
		server = SimpleServer(('', PORT), TCPHandler)
		server.serve_forever()
