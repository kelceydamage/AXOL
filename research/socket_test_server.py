#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

import SocketServer
import subprocess
from datetime import datetime

class LocalTasks(object):
	methods = {
			'cpu': ['cat', '/proc/loadavg'],
			'memory': ['cat', '/proc/meminfo'],
			'disk': ['df', '-h'],
			'payfirma_logs': [
				'tail -n 100 /var/log/apache2/payfirma-error.log | grep "%s" | grep -i error' \
				% str(datetime.utcnow())[8:15]
				]
			}

	@classmethod
	def run_task(cls, method):
		if method in cls.methods:
			if method == 'payfirma_logs':
				proc = subprocess.Popen(
					cls.methods[method][0],
					stdout=subprocess.PIPE,
					stdin=subprocess.PIPE,
					shell=True
					)
				response = proc.stdout.read()
				print response
				return response
			else:
				proc = subprocess.Popen(
					cls.methods[method],
					stdout=subprocess.PIPE,
					stdin=subprocess.PIPE
					)
				response = proc.stdout.read()
				return response
		else:
			return 'Invalid Method'

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

class TCPHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		self.data = self.request.recv(1024).strip()
		print '{} requested: {}'.format(self.client_address[0], self.data)
		if self.client_address[0] == 'ip':
			response = LocalTasks.run_task(self.data)
			self.request.sendall(response)
		else:
			self.request.sendall('Connection Refused')

if __name__ == '__main__':
	HOST, PORT = '172.31.9.218', 9999
	server = SimpleServer((HOST, PORT), TCPHandler)
	server.serve_forever()
