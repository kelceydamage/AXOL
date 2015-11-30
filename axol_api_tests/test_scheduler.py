#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
from axol_api_client import AxolApiClient

# Test scheduler || client.test() supports: enable_response=True if you want
# to see the raw api output
#-----------------------------------------------------------------------#
print '----Test scheduler---------------'

client = AxolApiClient('10.100.10.59')

api = 'create_scheduled_task'
data = {
	"time": 300,
	"task_name": 'integration_test',
	"api_name": 'get_null',
	"role": 'production_servers'
	}

client.test(api, data, enable_response=True)

api = 'get_scheduled_tasks'
data = {}

client.test(api, data, enable_response=True)


api = 'remove_scheduled_task'
data = {
	"task_name": "integration_test'",
	}

client.test(api, data, enable_response=True)
