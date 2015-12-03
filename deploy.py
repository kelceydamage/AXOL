#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013
#+

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

	def install_axol_node(self):
		print 'Configure base #####################'
		self._ssh(
			'sudo yum -y install gcc centos-release-SCL; \
			sudo yum -y install python27 perl dos2unix; \
			sudo echo "yum -y install python-setuptools"|scl enable python27 -; \
			sudo echo "easy_install pip"| scl enable python27 -; \
			sudo source /opt/rh/python27/enable; \
			sudo pip install celery lmdb fabric boto awscli redis elasticsearch cassandra-driver'
			)

	def configure_axol_node(self):
		print 'Configure axol #####################'
		self._ssh(
			'cd /opt/AXOL_Management/axol_node/server_config; \
			sudo cp default /etc/httpd/conf.d/; \
			sudo cp celeryd.sh /etc/init.d/celeryd'
			)

	def deploy(self, infile):
		command = 'tar -zcvf pfmon.tar %s' % infile
		subprocess.Popen(
			command,
			shell=True
			)

		print 'SFTP To Remote #####################'
		self._sftp(
			'pfmon.tar',
			'/home/%s/pfmon.tar' % self.remote_user
			)

		print 'SSH To Remote ######################'
		o, e = self._ssh(
			'sudo mkdir /opt/AXOL_Management; \
			sudo cp /home/%s/pfmon.tar /opt/AXOL_Management/pfmon.tar; \
			cd /opt/AXOL_Management/; \
			sudo tar -zxvf /opt/AXOL_Management/pfmon.tar; \
			sudo rm -f /pfmon.tar; \
			sudo find ./ -type f -exec dos2unix {} \;' % self.remote_user
			)
		print e


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

remote_server = '<remote-ip>'
remote_user = 'deploy-user'
remote_password = 'deploy-pass'
folder_to_be_archived = 'axol_node'

DT = DeployTool(
	remote_user,
	remote_password,
	remote_server
	)

DT.install_axol_node()
DT.deploy('axol_node')
DT.deploy('axol_common')
DT.configure_axol_node()

