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
class AxolApiClient(object):
	"""docstring for AxolApiClient"""
	def __init__(self, host):
		super(AxolApiClient, self).__init__()
		self.host = host

	def call_function_api(self, api_name, data, enable_response):
		error = None
		url = 'http://%s/api/%s' % (self.host, api_name)
		data = json.dumps(data)
		request = urllib2.Request(url, data)
		request.add_header('Content-Type', 'application/json')
		response = urllib2.urlopen(request)
		response_dict = response.read()
		if enable_response == True:
			print response_dict
		try:
			error = json.loads(response_dict)['response']['error']
			return 'Failed', error
		except Exception, e:
			return 'Passed', error

	def test(self, api, data, enable_response=False):
		print 'Calling: %s' % api
		try:
			status, error = self.call_function_api(api, data, enable_response)
		except Exception, e:
			status = 'Failed'
			print '%s: %s' % (api, e)
		print 'errors: %s' % error
		print 'Completed: %s\n' % status
		return status, error
