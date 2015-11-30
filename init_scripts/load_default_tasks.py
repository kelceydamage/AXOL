#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

import urllib2
import time

# Main script
#-----------------------------------------------------------------------#

# research
axol_scheduler = 'ip-address'

def register_scheduler_task(axol_scheduler, api_name, func, method, time, role):
	response = urllib2.urlopen(
		'http://%s/api/scheduler/schedule/%s/%s/%s/%s/%s' % (
			axol_scheduler,
			api_name,
			func,
			method,
			time,
			role
			)
		)
	print 'http://%s/api/scheduler/schedule/%s/%s/%s/%s/%s' % (
			axol_scheduler,
			api_name,
			func,
			method,
			time,
			role
			)
	return response.read()

# Default tasks to load
#-----------------------------------------------------------------------#

#roles = 'hq_api_servers'
roles = 'production_servers'

'''
register_scheduler_task(
	axol_scheduler,
	'network',
	'heartbeat',
	'usage',
	15,
	'production_servers'
	)

time.sleep(4)
'''
register_scheduler_task(
	axol_scheduler,
	'system',
	'memory',
	'stats',
	15,
	roles
	)

print 'sleep 5'
time.sleep(5)

register_scheduler_task(
	axol_scheduler,
	'system',
	'cpu',
	'usage',
	15,
	roles
	)

print 'sleep 5'
time.sleep(5)

roles = 'mysql_servers'

register_scheduler_task(
	axol_scheduler,
	'plugins',
	'mysql',
	'performance',
	15,
	roles
	)

roles = 'production_servers'

register_scheduler_task(
	axol_scheduler,
	'system',
	'disk',
	'usage',
	15,
	roles
	)

roles = 'hq_api_servers'

time.sleep(3)
'''
register_scheduler_task(
	axol_scheduler,
	'hq',
	'logs',
	'error',
	15,
	roles
	)
'''

# ----------------------------''
'''
roles = 'axol'


register_scheduler_task(
	axol_scheduler,
	'network',
	'heartbeat',
	'usage',
	15,
	roles
	)

time.sleep(3)

register_scheduler_task(
	axol_scheduler,
	'system',
	'memory',
	'stats',
	15,
	roles
	)
'''
print 'sleep 5'
time.sleep(3)
'''
roles = 'axol'

register_scheduler_task(
	axol_scheduler,
	'system',
	'cpu',
	'usage',
	15,
	roles
	)

print 'sleep 5'
time.sleep(3)

register_scheduler_task(
	axol_scheduler,
	'system',
	'disk',
	'usage',
	15,
	roles
	)
'''
roles = 'production_servers'
register_scheduler_task(
	axol_scheduler,
	'system',
	'health',
	'stats',
	15,
	roles
	)
'''
roles = 'axol'
time.sleep(3)
register_scheduler_task(
	axol_scheduler,
	'system',
	'health',
	'stats',
	15,
	roles
	)
'''


