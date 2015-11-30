#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
from axol_api_client import AxolApiClient

# Test events || client.test() supports: enable_response=True if you want
# to see the raw api output
#-----------------------------------------------------------------------#
print '----Event Tests------------------'

client = AxolApiClient('10.100.10.34')

api = 'create_event_notice'

alert_types = [
	{'alert_type': ['email']},
	{'alert_type': ['text']},
	{'alert_type': []},
	{'alert_type': ['some_other_value']},
	{'alert_type': 'string_not_in_list'},
	{'alert_type': ''}
	]
sources = [
	{'source': 'api_test'},
	{'source': 'api_test'},
	{'source': 'api_test'}
	#{'source': ['wrong_1', 'wrong_2']},
	#{'source': ''}
	]
groups = [
	{'group': 'none'},
	{'group': ['value_in_list']},
	{'group': ['wrong_1', 'wrong_2']},
	{'group': 'test'},
	{'group': ''}
	]
tdata = [
	{'data': ['list']},
	{'data': ['wrong_1', 'wrong_2']},
	{'data': 'string_value'},
	{'data': {'dict_key_1': 'value_1'}},
	{'data': {'dict_key_1': ''}},
	{'data': ''}
	]
matrix = {
	'alert_types': alert_types,
	'sources': sources,
	'groups': groups,
	'tdata': tdata
	}

#for t1 in matrix['alert_types']:
def matrix_test(matrix, api, client):
	i = 0
	failures = []
	for t2 in matrix['tdata']:
		for t3 in matrix['groups']:
			for t4 in matrix['sources']:
				data = {'alert_type': [], 'data':t2['data'], 'group':t3['group'], 'source':t4['source']}
				status, error = client.test(api, data)
				if status != 'Passed':
					failures.append((i, status, error))
				i = i + 1
	return (failures, i)
i2 = 0
for n in range(1):
	failures, i = matrix_test(matrix, api, client)
	i2 = i2 + i

print 'Tests ran: %s' % i2
print '-----------------------------------'
for item in failures:
	print item
print len(failures)