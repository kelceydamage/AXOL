#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
from axol_api_client import AxolApiClient
import sys
sys.path.append("/opt/AXOL_Management/AXOL")
sys.path.append("C:\Users\kelcey.damage.CORP\Documents\GitHub\AXOL")
from axol_common.classes.common_timer import CommonTimer

# Test administration || client.test() supports: enable_response=True if
# you want to see the raw api output
#-----------------------------------------------------------------------#
print '----Admin Tests------------------'
CT = CommonTimer()

client = AxolApiClient('10.100.10.34', )

api = 'get_all_roles'
data = {
	'network': 'external'
	}
CT.start()
client.test(api, data)

api = 'get_alert_servers'
data = {}
CT.log('get_all_roles')
client.test(api, data)

api = 'remove_alert_server'
data = {
	'server_name': 'live_axol_auto_scheduler_v1.0.0'
	}
CT.log('get_alert_server')
client.test(api, data)

api = 'restore_alert_servers'
data = {
	'network': 'external'
	}
CT.log('remove_alert_server')
client.test(api, data)

api = 'get_production_servers'
data = {
	'network': 'external'
	}
CT.log('restore_alert_servers')
client.test(api, data)
CT.log('get_production_servers')
for item in CT.get_log():
	print item