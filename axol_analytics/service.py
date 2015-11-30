#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
from elasticsearch import Elasticsearch
import datetime
import urllib
import urllib2
import numpy as np
#import pandas as pd
from bokeh.plotting import line, show
import json

# Elasticsearch configuration
#-----------------------------------------------------------------------#
print 'CONFIGURING ELASTICSEARCH'
#node = 'internal-Elasticsearch-Internal-LB-729281810.us-west-2.elb.amazonaws.com:80'
node = 'Elasticsearch-Cluster:80'
ES = Elasticsearch(node)

root_url = 'http://Elasticsearch'
date_now = datetime.date.today()
data = {
	'size': 1000,
	'query': {
		'filtered': 
			'query': {
				'range': {
					'timestamp': {
						'gte': '2014-12-09T0:05:00.000000',
						'lte': 'now'
						}
					}
				},
			'filter': {
				'bool': {
					'must_not': {
						'term': {'name': 'live_axol_auto_scheduler_v1.0.0'}
						}
					}
				}
			}
		}
	}
data_obj = {'live_elasticsearch_1':[], 'live_elasticsearch_2':[], 'live_elasticsearch_3':[]}
api = '/_all/cpu/_search'
data = json.dumps(data)
print data
request = urllib2.Request('%s%s' % (root_url, api), data)
print request.get_full_url()
print dir(request)
print request.get_data()
response = urllib2.urlopen(request)
hits = json.loads(response.read())
print '--------------------------------------------------'
for records in hits['hits']['hits']:
	for record in records:
		if record == '_source':

			if records[record]['name'] == 'live_elasticsearch_1':
				data_obj['live_elasticsearch_1'].append(records[record]['current_usage'])
			elif records[record]['name'] == 'live_elasticsearch_2':
				data_obj['live_elasticsearch_2'].append(records[record]['current_usage'])
			elif records[record]['name'] == 'live_elasticsearch_3':
				data_obj['live_elasticsearch_3'].append(records[record]['current_usage'])
#print data_obj
l = len(data_obj['live_elasticsearch_1'])
r = []
for i in range(50):
	r.append(i)

#print r
'''
from bokeh.plotting import figure, output_file, show

# prepare some data
x0 = data_obj
'''
'''
y1 = [x**2 for x in x0]
y2 = [10**x for x in x0]
y3 = [10**(x**2) for x in x0]
'''
'''
# output to static HTML file
output_file("log_lines.html")

# create a new figure
p = figure(
    tools="pan,box_zoom,reset,previewsave",
    y_range=[1, 100], title="CPU Usage",
    x_axis_label='Ticks', y_axis_label='Percent Usage'
)

# create plots!
z1 = range(30,40,10)
colors = ['green', 'red', 'orange']
for z, i in zip(data_obj, colors):
	p.line(r, data_obj[z], line_color=i, line_width=2, legend=z)
	p.circle(r, data_obj[z])
	p.circle(r, 60)
p.rect([40], 40, height=10, width=10, fill_color="blue", fill_alpha=0.6, line_color=None)
#p.line(r, x0, legend="CPU USE")
'''
'''
p.circle(x0, x0, legend="y=x")
p.line(x0, y1, legend="y=x**2")
p.circle(x0, y1, fill_color=None, line_color="green", legend="y=x**2")
p.line(x0, y2, line_color="red", line_width=2, legend="y=10^x")
p.line(x0, y3, line_color="orange", line_width=2, legend="y=10^(x^2)")
'''
#show()




