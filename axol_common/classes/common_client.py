#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
import urllib2
import sys
import json

# Main class || Client for accessing AXOL API
#-----------------------------------------------------------------------#
class CommonClient(object):
	"""docstring for CommonClient"""
	def __init__(self, host):
		super(CommonClient, self).__init__()
		pass

	@staticmethod
	def call_api(api_name, data, host):
		url = 'http://%s/api/%s' % (host, api_name)
		data = json.dumps(data)
		request = urllib2.Request(url, data)
		request.add_header('Content-Type', 'application/json')
		response = urllib2.urlopen(request)
		response_dict = json.loads(response.read())
		return response_dict
