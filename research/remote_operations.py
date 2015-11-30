#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

import sys
from fabric.api import *
from datetime import datetime

sys.path.append("/opt/AXOL_Management/AXOL")

from auto_roledefs import *

# Environment Configuration
#-----------------------------------------------------------------------#

def init():
	env.roledefs = generate_base_roles()

env.user = 'payfirma-monitor'
env.password = 'password'
env.parallel = True
env.warn_only = True
env.connection_attempts = 1
env.timeout = 1
env.skip_bad_hosts = True
env.disable_known_hosts = True
env.pool_size = 16

# Fabric Jobs
#-----------------------------------------------------------------------#

def fabric_update_roledefs(args=[]):
	env.roledefs = []
	env.roledefs = generate_base_roles()

	return env

def get_is_alive(args=[]):
	pass

def get_heartbeat():
	output = run('echo "I am alive"', pty=False)

	return output

def get_processor_load(args=[]):
	output = sudo('cat /proc/loadavg', pty=False)

	return output

def get_memory_stats(args=[]):
	output = sudo('cat /proc/meminfo', pty=False)

	return output

def get_memory_usage(args=[]):
	output = sudo('free', pty=False)

	return output

def get_disk_usage(args=[]):
	output = sudo('df -hP', pty=False)

	return output

def get_time(args=[]):
	output = sudo('date', pty=False)

	return output

def get_service_status(args=[]):
	output = sudo('service %s status' % args[0], pty=False)

	return output

def get_fatal_errors(args=[]):
	time = str(datetime.utcnow())

	output = sudo('cat %s | grep "%s" | grep -i "fatal"' % (
			'/var/log/apache2/payfirma-error.log',
			time[8:15]),
		pty=True
		)

	if output == None or output == 'Null':
		output = ''

	return output

def get_error_errors(args=[]):
	time = str(datetime.utcnow())

	output = sudo('cat %s | grep "%s" | grep -i "error"' % (
			'/var/log/apache2/payfirma-error.log',
			time[8:15]),
		pty=False
		)

	if output == None or output == 'Null':
		output = ''

		return output

	else:
		output_2 = []
		for line in output.split('/\n'):
			output_2.append(line)

		return output_2

def deploy_agent(args=[]):
	output = sudo(
		'echo %s > /home/payfirma-monitor/axol_agent; \
		chmod 777 axol_agent.py' % args[0]
		)

init()
