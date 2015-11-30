#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2014

# Imports
#-----------------------------------------------------------------------#
import os, subprocess
from paramiko import SSHClient

class DeployTool(object):
	"""docstring for ClassName"""
	def __init__(self, remote_user, remote_password, remote_server):
		self.remote_user = remote_user
		self.remote_password = remote_password
		self.remote_server = remote_server
		self.client = SSHClient()
		self.client.load_system_host_keys()
		self.client.connect(
			hostname=self.remote_server,
			username=self.remote_user,
			password=self.remote_password
			)

	def _ssh(self, command):
		stdin, stdout, stderr = self.client.exec_command(command)
		ssh_output = stdout.read()
		ssh_error = stderr.read()

		return (ssh_output, ssh_error)

	def _sftp(self, infile, outfile):
		sftp = self.client.open_sftp()
		sftp.put(
			infile,
			outfile
			)

	def deploy(self):
		print '### Downloading Configurator ###'
		self._ssh('wget -P /opt/ http://10.100.10.146/config/configurator.sh')
		self._ssh('chmod 777 /opt/configurator.sh')
		print '### Running Configurator ###'
		self._ssh('/opt/configurator.sh')

remote_user = 'root'
remote_password = prompt('Enter Password')

for server in ['']:
	print '### Deploying: %s ###' % server
	DT = DeployTool(
		remote_user,
		remote_password,
		server
		)

	DT.deploy()

