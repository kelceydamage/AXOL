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

# Test events || client.test() supports: enable_response=True if you want
# to see the raw api output
#-----------------------------------------------------------------------#
print '----Event Tests------------------'
CT = CommonTimer()

client = AxolApiClient('10.100.10.130')

api = 'create_event_notice'
data = {
	'alert_type': [],
	'source': 'api_test',
	'group': 'none',
	'data': {'test_field': 'test_string'},
	}
CT.start()
client.test(api, data)
CT.log('create_event_notice')
for item in CT.get_log():
	print item
