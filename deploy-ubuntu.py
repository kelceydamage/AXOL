#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013
#+

import os, subprocess
from paramiko import SSHClient, AutoAddPolicy
import time
import sys
sys.path.append("/Volumes/git/axol")
from axol_common.distributed import axol_roledefs

#folder_to_be_archived = '/home/mysql_backup_v2.py'

roledefs = axol_roledefs.generate_base_roles('external')

class DeployTool(object):
	"""docstring for ClassName"""
	def __init__(self, remote_user, remote_password, remote_server):
		self.remote_user = remote_user
		self.remote_password = remote_password
		self.remote_server = remote_server
		self.client = SSHClient()
		self.client.set_missing_host_key_policy(AutoAddPolicy())
		self.client.load_system_host_keys()
		self.client.connect(
			hostname=self.remote_server,
			username=self.remote_user,
			password=self.remote_password
			)

	def restart_node(self):
		print 'RESTARTING AXOL ################'
		self._ssh('sudo /opt/AXOL_Management/AXOL/axol_node/axol_start')

	def install_analytics_node(self, infile):
		self.create_directories()
		print 'INSTALLING PACKAGES ################'
		self._ssh('sudo apt-get install python-dev python-pip python-numpy \
			python-scipy python-matplotlib ipython ipython-notebook python-pandas \
			python-sympy python-nose -y')
		self._ssh('sudo pip install scikit-learn')
		self._ssh('sudo pip install bokeh')
		self.deploy(infile)

	def update_analytics_node(self, infile):
		self.deploy(infile)

	def update_axol_node(self, infile):
		self.deploy(infile)
		self.install_config_files()

	def install_axol_node(self, infile):
		self.create_directories()
		self.install_packages()
		#self.setup_rabbitmq()
		self.install_python_packages()
		self.update_apt()
		self.create_user()
		self.deploy(infile)
		self.install_config_files()

	def create_directories(self):
		print 'CREATING DIRECTORIES ###############'
		try:
			self._ssh('sudo touch /home/test')
			self._ssh('sudo mkdir /opt/AXOL_Management')
			self._ssh('sudo mkdir /opt/AXOL_Management/AXOL')
		except Exception, e:
			print e

	def install_packages(self):
		print 'INSTALLING PACKAGES ################'
		try:
			self._ssh('sudo apt-get update')
			self._ssh('echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list')
			self._ssh('sudo apt-get install apache2 -y')
			self._ssh('sudo apt-get install dos2unix -y')
			self._ssh('sudo apt-get install apt-show-versions -y')
			self._ssh('sudo apt-get install htop -y')
			self._ssh('sudo a2enmod ssl')
			self._ssh('sudo aptitude install libapache2-mod-wsgi -y')
			self._ssh('sudo apt-get install python-dev -y')
		except Exception, e:
			print e
		print 'INSTALLING PACKAGES RMQ #############'
		try:
			self._ssh('sudo aptitude install rabbitmq-server -y')
		except Exception, e:
			print e

	def setup_rabbitmq(self):
		print 'CONFIGURING RABBITMQ ###############'
		try:
			self._ssh('sudo apt-get update')
			self._ssh('echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list')
			self._ssh('sudo aptitude install rabbitmq-server -y')
			self._ssh('touch /var/lib/rabbitmq/.erlang.cookie')
			self._ssh('chown rabbitmq:rabbitmq /var/lib/rabbitmq/.erlang.cookie')
			self._ssh('sudo echo "XUNTWTQPUMITKLDZYPAY" > /var/lib/rabbitmq/.erlang.cookie')
			self._ssh('service rabbitmq-server start')
			self._ssh('sudo rabbitmqctl add_user celery jgh8&hbJVk56')
			self._ssh('sudo rabbitmqctl add_vhost celery')
			self._ssh('sudo rabbitmqctl set_permissions -p celery celery ".*" ".*" ".*"')
		except Exception, e:
			print e

	def install_python_packages(self):
		print 'INSTALLING PYTHON PACKAGES #########'
		try:
			#self._ssh('sudo apt-get install python-pip -y')
			self._ssh('sudo pip install elasticsearch')
			self._ssh('sudo pip install celery==3.1.16')
			self._ssh('sudo pip install lmdb')
			self._ssh('pip install cassandra-driver')
			#self._ssh('sudo pip install librabbitmq')
			#self._ssh('sudo pip install requests')
			#self._ssh('sudo pip install redis')
		except Exception, e:
			print e

	def update_apt(self):
		print 'COMPLETING PACKAGE INSTALLATION ####'
		self._ssh('sudo apt-get update')

	def create_user(self):
		print 'CREATING USERS #####################'
		self._ssh('sudo useradd axol -G www-data')

	def install_config_files(self):
		print 'INSTALLING CONFIG FILES ############'
		try:
			self._ssh('service apache2 stop')
			self._ssh('sudo rm -f /etc/apache2/sites-available/000-default.conf')
			self._ssh('sudo rm -f /etc/apache2/sites-enabled/000-default.conf')
			self._ssh('sudo rm -f /etc/apache2/sites-enabled/000-default')
			time.sleep(1)
			self._ssh('sudo cp /opt/AXOL_Management/AXOL/axol_node/server_config/default /etc/apache2/sites-available/default')
			self._ssh('sudo ln -s /etc/apache2/sites-available/default /etc/apache2/sites-enabled/000-default.conf')
			self._ssh('sudo cp /opt/AXOL_Management/AXOL/axol_node/server_config/celeryd.sh /etc/init.d/celeryd')
			print 'INSTALLING /ETC/DEFAULT'
			self._ssh('sudo cp /opt/AXOL_Management/AXOL/axol_node/server_config/etc_default/celeryd.sh /etc/default/celeryd')
			#self._ssh('sudo dos2unix /etc/default/celeryd')
			self._ssh('sudo chown axol:axol /var/log/celery; sudo chown axol:axol /var/run/celery')
			self._ssh('sudo ln -s /opt/AXOL_Management/AXOL/axol_node/axol_start.sh /home/axol_start')
			#self._ssh('sudo chmod 777 /opt/AXOL_Management/AXOL/axol_node/tmp/*')
		except Exception, e:
			print e

	def install_axol_scheduler(self, infile):
		print 'CREATING DIRECTORIES ###############'
		self.create_directories()

		print 'INSTALLING PACKAGES ################'
		self._ssh('sudo apt-get update')
		self._ssh('sudo apt-get install python-dev -y')
		self._ssh('sudo apt-get install python-pip -y')
		self._ssh('sudo apt-get install apache2 -y')
		self._ssh('sudo a2enmod ssl')
		self._ssh('sudo aptitude install libapache2-mod-wsgi -y')

		print 'INSTALLING PYTHON PACKAGES #########'
		self._ssh('sudo pip install boto fabric flask flower')
		print 'COMPLETING INSTALLATION ############'
		self._ssh('sudo apt-get update')

		self.deploy(infile)
		self.install_axol_scheduler_config()

	def install_axol_scheduler_config(self):
		print 'INSTALLING CONFIG FILES ############'
		self._ssh('service apache2 stop')
		self._ssh('sudo rm -f /etc/apache2/sites-available/000-default.conf')
		self._ssh('sudo rm -f /etc/apache2/sites-enabled/000-default.conf')
		self._ssh('sudo cp /opt/AXOL_Management/AXOL/axol_scheduler/server_config/default /etc/apache2/sites-available/default')
		self._ssh('sudo ln -s /etc/apache2/sites-available/default /etc/apache2/sites-enabled/000-default.conf')
		self._ssh('service apache2 start')

	def deploy(self, infile):
		command = 'tar -zcvf pfmon.tar %s' % infile
		subprocess.Popen(
			command,
			shell=True
			)
		print 'Starting Deploy ####################'

		time.sleep(2)

		print 'SFTP To Remote #####################'
		self._sftp(
			'pfmon.tar',
			'/home/%s/pfmon.tar' % self.remote_user
			)

		print 'SSH To Remote ######################'
		print 'Copy TAR ###########################'
		self._ssh('sudo cp /home/%s/pfmon.tar /opt/AXOL_Management/AXOL/pfmon.tar' % self.remote_user)
		self._ssh('cd /opt/AXOL_Management/AXOL/; sudo tar -zxvf pfmon.tar')
		self._ssh('sudo rm -f /opt/AXOL_Management/AXOL/pfmon.tar')
		print 'Completed Deploy ###################'

	def build_agent_package(self, infile):
		print 'Building Archive ###################'
		command = 'tar -zcvf agent.tar %s' % infile
		subprocess.Popen(
			command,
			shell=True
			)

		time.sleep(0.5)

	def deploy_agent(self, infile, name):
		print 'SFTP To Remote #####################'
		self._sftp(
			'agent.tar',
			'/home/%s/agent.tar' % self.remote_user
			)
#sudo rm -f agent.tar; \
		print 'Create Base Folder #################'
		self._ssh('sudo mkdir -p /opt/AXOL_Management/AXOL')
		print 'Copy Archive To Base Folder ########'
		self._ssh('sudo cp /home/%s/agent.tar /opt/AXOL_Management/AXOL/agent.tar' % self.remote_user)
		print 'Unpack Archive #####################'
		self._ssh('cd /opt/AXOL_Management/AXOL; sudo tar -zxvf agent.tar')
		print 'Deploy Init Script #################'
		self._ssh('sudo cp /opt/AXOL_Management/AXOL/%s/%s_init.sh /etc/init.d/%s' % (name,name,name))
		print 'Set Agent Permissions ##############'
		self._ssh('sudo chmod 755 /etc/init.d/%s' % name)
		print 'Rename Executable ##################'
		self._ssh('sudo mv /opt/AXOL_Management/AXOL/%s/%s.py /opt/AXOL_Management/AXOL/%s/%s' % (name,name,name,name))
		print 'Updating RC ########################'
		self._ssh('sudo update-rc.d %s defaults' % name)
		self._ssh('sudo ln -s /etc/init.d/%s /sbin/%s' % (name,name))
		print 'Agent Installed ####################'

	def restart_agent(self, name):
		try:
			self._ssh('sudo service %s stop' % name)
			time.sleep(1)
			self._ssh('sudo service %s start' % name)
			print 'Agent Rebooted #####################'
		except Exception, e:
			print e


	def deploy_research(self, infile):
		print 'Building Archive ###################'
		command = 'tar -zcvf research.tar %s' % infile
		subprocess.Popen(
			command,
			shell=True
			)

		time.sleep(0.5)

		print 'SFTP To Remote #####################'
		self._sftp(
			'research.tar',
			'/home/%s/research.tar' % self.remote_user
			)
		#sudo rm -f agent.tar; \
		print 'Create Base Folder #################'
		self._ssh('sudo mkdir /opt/AXOL_Management')
		self._ssh('sudo mkdir /opt/AXOL_Management/AXOL')
		print 'Copy Archive To Base Folder ########'
		self._ssh('sudo cp /home/%s/research.tar /opt/AXOL_Management/AXOL/research.tar' % self.remote_user)
		print 'Unpack Archive #####################'
		self._ssh('cd /opt/AXOL_Management/AXOL; sudo tar -zxvf research.tar')
		print 'Setting Permissions ################'
		self._ssh('sudo chmod 777 /opt/AXOL_Management/AXOL/research/agent\ research\ code/socket_test_client.py')
		print 'Remove Archive #####################'
		self._ssh('sudo rm -f /opt/AXOL_Management/AXOL/research.tar')

	def test_deploy(self, infile):
		print 'SFTP To Remote #####################'
		self._sftp(
			'pfmon.tar',
			'/home/%s/pfmon.tar' % self.remote_user
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

remote_server = '<remote-ip>'
remote_user = 'deploy-user'
remote_password = 'deploy-pass'

DT = DeployTool(
	remote_user,
	remote_password,
	remote_server
	)


folder_to_be_archived = 'axol_node'
servers = ['<remote-ip>']
for server in servers:
	print 'Deploying Node To: %s' % server
	DT = DeployTool(
		remote_user,
		remote_password,
		server
		)

	#DT.install_axol_node(folder_to_be_archived)
	DT.update_axol_node(folder_to_be_archived)
	DT.deploy('axol_common')
	DT.restart_node()
	#DT.install_config_files()
	#DT.setup_rabbitmq()

print 'FINISHED NODE DEPLOY'

#data['response']['value'][item][item_2]
#output = DT.deploy(folder_to_be_archived)
#output = DT.test_deploy(folder_to_be_archived)

# analytics
remote_server = '<remote-ip>'

folder_to_be_archived = 'axol_analytics'

DT = DeployTool(
	remote_user,
	remote_password,
	remote_server
	)

#DT.install_analytics_node(folder_to_be_archived)
DT.update_analytics_node(folder_to_be_archived)
DT.deploy('axol_common')

'''

# research
remote_server = '<remote-ip>'

folder_to_be_archived = 'axol_scheduler'

DT = DeployTool(
	remote_user,
	remote_password,
	remote_server
	)

#DT.install_axol_scheduler(folder_to_be_archived)
DT.deploy('axol_common')
DT.deploy(folder_to_be_archived)
'''
'''
remote_server = '<remote-ip>'
folder_to_be_archived = 'axol_api_tests'

DT = DeployTool(
	remote_user,
	remote_password,
	remote_server
	)

#DT.install_axol_scheduler(folder_to_be_archived)
DT.deploy('axol_common')
DT.deploy(folder_to_be_archived)
'''
'''
#DT.install_axol_scheduler_config()
#output = DT.deploy(folder_to_be_archived)
print 'FINISHED SCHEDULER DEPLOY'
'''
'''
remote_servers = [
	'<remote-ip>',
	'<remote-ip>'
	]

'''

folder_to_be_archived = 'axol_agent'
DT.build_agent_package(folder_to_be_archived)
servers = ['<remote-ip>']
print 'Starting'
for server in servers:
	print 'Deploying Agent To: %s' % server
	DT = DeployTool(
		remote_user,
		remote_password,
		server
		)

	#DT.deploy_agent(folder_to_be_archived,'axol_test_processor')
	DT.deploy_agent(folder_to_be_archived, 'axol_agent')
	DT.deploy('axol_common')
	#DT.restart_agent('axol_agent')


'''
folder_to_be_archived = 'cassandra_agent'
DT.build_agent_package(folder_to_be_archived)
servers = ['<remote-ip>']
for server in servers:
	print 'Deploying Agent To: %s' % server
	DT = DeployTool(
		remote_user,
		remote_password,
		server
		)

	#DT.deploy_agent(folder_to_be_archived,'axol_test_processor')
	DT.deploy_agent(folder_to_be_archived, 'cassandra_agent')
	#DT.restart_agent('axol_agent')
#print output
'''

'''
#remote_server = '<remote-ip>'
folder_to_be_archived = 'research'

DT = DeployTool(
	remote_user,
	remote_password,
	remote_server
	)
'''
#DT.deploy_research(folder_to_be_archived)


