#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013
#+

import os, subprocess
from paramiko import SSHClient

#folder_to_be_archived = '/home/mysql_backup_v2.py'

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
		pass

	def install_axol_scheduler(self, infile):

		print 'CREATING DIRECTORIES ###############'
		self._ssh('sudo mkdir /opt/AXOL_Management')
		print 'INSTALLING PACKAGES ################'
		self._ssh('sudo apt-get install python-pip -y')
		self._ssh('sudo aptitude install libapache2-mod-wsgi')

		print 'INSTALLING PYTHON PACKAGES #########'
		self._ssh('sudo pip install boto fabric flask')
		print 'COMPLETING INSTALLATION ############'
		self._ssh('sudo apt-get update')

		self.deploy(infile)

		print 'INSTALLING CONFIG FILES ############'
		self._ssh('service apaceh2 stop')
		self._ssh('sudo rm -f /etc/apache2/sites-available/default')
		self._ssh('sudo cp /opt/AXOL_Management/AXOL/axol_scheduler/server_config/default /etc/apache2/sites-available/default')
		self._ssh('service apache2 start')

	def deploy(self, infile):
		command = 'tar.exe -zcvf pfmon.tar %s' % infile
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
		self._ssh(
			'sudo cp /home/%s/pfmon.tar /opt/AXOL_Management/pfmon.tar; \
			cd /opt/AXOL_Management/; \
			sudo tar -zxvf /opt/AXOL_Management/pfmon.tar; \
			sudo rm -f /pfmon.tar;' % self.remote_user
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

#remote_server = '54.201.119.11'
remote_server = '54.186.222.10'
#remote_server = '54.200.105.146'
#remote_server = '54.200.171.130'
remote_user = 'pfmon-deploy'
remote_password = 'SWS#@fwk&*'
folder_to_be_archived = 'AXOL/axol_node'

DT = DeployTool(
	remote_user,
	remote_password,
	remote_server
	)

#DT.install_axol_scheduler()

output = DT.deploy(folder_to_be_archived)

remote_server = '50.112.162.211'
folder_to_be_archived = 'AXOL/axol_scheduler'

DT = DeployTool(
	remote_user,
	remote_password,
	remote_server
	)

DT.deploy(folder_to_be_archived)
'''
output = DT.deploy(folder_to_be_archived)
'''

#print output
