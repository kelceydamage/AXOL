#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
from axol_api_client import AxolApiClient
import sys
sys.path.append("/opt/AXOL_Management/AXOL")
sys.path.append("C:\Users\kelcey.damage.CORP\Documents\GitHub\AXOL")
sys.path.append("D:\GitHub\Payfirma\AXOL")
from axol_common.classes.common_timer import CommonTimer

# Test metrics || client.test() supports: enable_response=True if you want
# to see the raw api output
#-----------------------------------------------------------------------#
print '----Test metrics-----------------'
CT = CommonTimer()


client = AxolApiClient('10.100.10.130')

api = 'get_processor_usage'
data = {
	'role': 'production_servers'
	}
CT.start()
client.test(api, data)

api = 'get_memory_usage'
data = {
	'role': 'production_servers'
	}
CT.log('get_processor_usage')
client.test(api, data)

api = 'get_disk_usage'
data = {
	'role': 'production_servers'
	}
CT.log('get_memory_usage')
client.test(api, data)

api = 'get_mysql_usage'
data = {
	'role': 'mysql_servers'
	}
CT.log('get_disk_usage')
client.test(api, data)

api = 'create_health_metrics'
data = {
	'role': 'production_servers'
	}
CT.log('get_mysql_usage')
client.test(api, data)
CT.log('create_health_metrics')
for item in CT.get_log():
	print item
