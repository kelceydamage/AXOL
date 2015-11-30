#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

import urllib2
import sys
sys.path.append("..")
from axol_config import axol_node
import json

def call_function_api(axol_node, api_name, role):
	print 'http://%s/api/%s' % (axol_node, api_name)
	url = 'https://%s/api/%s' % (axol_node, api_name)
	data = json.dumps({"role": "%s" % role})
	request = urllib2.Request(url, data)
	request.add_header('Content-Type', 'application/json')
	response = urllib2.urlopen(request)
	return response.read()

