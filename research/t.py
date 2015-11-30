#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013
import boto.ec2
import re

# Filter IP addresses into a role collection
def generate_role(_list, _filter, application_flag):
        for role in roledefs:
                if re.search(r'%s.*' % _filter, role) \
                and not re.search(r'.*all.*', role) \
                or re.search(r'.*servers.*', role):
                        try:
                                _list.append(
                                        roledefs[role][application_flag]
                                        )
                        except Exception, e:
                                pass

        return _list

# Application flag can be either internal or external
#application_flag = 'external'
application_flag = 'internal'

ec2 = boto.ec2.connect_to_region(
	"us-west-2",
	aws_access_key_id="access key",
	aws_secret_access_key="secret key",
	)

x = ec2.get_all_instances()
roledefs = {}

t = []
for item in x:
	t.append(item.instances[0])

for item in t:
	if str(item._state) == 'running(16)':# and re.search(r'staging', item.tags['Name']):
		roledefs[item.tags['Name']] = {}
		roledefs[item.tags['Name']]['internal'] = item.private_ip_address
		roledefs[item.tags['Name']]['external'] = item.ip_address

for item in roledefs:
	print item
	print roledefs[item]

print roledefs

