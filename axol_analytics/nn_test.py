#! /usr/bin/env python
#-----------------------------------------#
# Copyright [2015] [Kelcey Jamison-Damage]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Imports
#-----------------------------------------------------------------------#
import time
import sys
import socket
import json
import struct
from sys import getsizeof
import datetime
from bokeh.plotting import *
#from bokeh.models import GlyphRenderer
#from __future__ import print_function

from bokeh.models import GlyphRenderer
import bokeh.embed as embed

output_server("log_lines")

# TUNING
#-----------------------------------------------------------------------#
# Plot Range
ra = 480
# Short EMA in ticks(15s intervals)
n2 = 4
# Long EMA in ticks(15s intervals)
n1 = 240
# Sample size from Elasticsearch
sample = 480
q = 'hello'
t = '%s' % q
#-----------------------------------------------------------------------#

def query(query_list):
	def __connect(request):
		client_socket = socket.socket(
			socket.AF_INET,
			socket.SOCK_STREAM
			)
		tls_sock = client_socket
		tls_sock.settimeout(1)
		error = 'undefined'
		try:
			tls_sock.connect(('127.0.0.1',9999))
			error = None
		except Exception, e:
			error = str(e)
			print 'CASSANDRA ERROR {__connect|send}: %s' % (error)
		try:
			request = str(json.dumps(request)).encode('base64','strict')
			print 'SEND SIZE: %s' % getsizeof(request)
			request = struct.pack('>I', len(request)) + request
			tls_sock.sendall(request)
			error = None
		except Exception, e:
			error = str(e)
			print 'CASSANDRA {__connect|connect}: %s' % (error)
		return tls_sock, error

	request = {}
	request['commands'] = query_list
	request['method'] = 'cassandra'
	tls_sock, error = __connect(request)

	return json.loads(tls_sock.recv(10244))

'''
r = []
for i in range(ra):
	r.append(i)

n3 = ra - n2
p = ''
a = (2 / (float(n1) + 1))
s1 = sum(data_obj['live_elasticsearch_1'][:n1])
EMAp = float(s1) / n1
EMA_list = []
for p in data_obj['live_elasticsearch_1'][-ra:]:
	#EMA = p + sum(data_obj['live_elasticsearch_1'][240:])
	EMA = (p * a) + (EMAp * (1 - a))
	EMAp = EMA
	EMA_list.append(EMA)

p = ''
a = (2 / (float(n2) + 1))
s2 = sum(data_obj['live_elasticsearch_1'][-n2:])
print s2
EMAp2 = float(s2) / n2
EMA_list_2 = []
for p in data_obj['live_elasticsearch_1'][-ra:]:
	EMA = (p * a) + (EMAp2 * (1 - a))

	print '---------------------------------------------'
	print '(p * a) + (EMAp2 * (1 - a)) = (%s) + (%s * (%s))' % ((p*a), EMAp2, (1-a))
	print 'EMAp2: %s' % EMAp2
	print 'P: %s' % p
	print 'a: %s' % a
	print 'EMA: %s' % EMA

	EMAp2 = EMA
	EMA_list_2.append(EMA)
'''


# prepare some data
#x0 = EMA_list
#x1 = data_obj['live_elasticsearch_1'][-ra:]
#x2 = EMA_list_2
#data_obj_2 = {
#	'Recorded Usage': x1,
#	'Long EMA(%smin)' % ((n1 * 15) / 60) : x0,
#	'Short EMA(%smin)' % ((n2 * 15) / 60): x2
#	}

#d1 = max(data_obj_2['Short EMA(%smin)' % ((n2 * 15) / 60)])
#d2 = min(data_obj_2['Short EMA(%smin)' % ((n2 * 15) / 60)])
#a1 = abs(int(d1)-int(d2))
#y_r = max(data_obj_2['Recorded Usage']) + 5
x = 1
y = 1
p = figure()
p.line(x, y)

push()

tag = embed.autoload_server(p, cursession())
html = """
<html>
  <head></head>
  <body>
    %s
  </body>
</html>
"""
with open("animated_embed.html", "w+") as f:
    f.write(html)

renderer = p.select(dict(type=GlyphRenderer))
ds = renderer[0].data_source

t = 0
while True:

	command = "select deviation_mean, deviation_negative, deviation_positive, deviation_variance, \
	time_string from axol_metrics.clusters where source='memory' and name='api' limit 10"
	response = query([command])
	deviation_pos_list = []
	deviation_neg_list = []
	variance_list = []
	mean_list = []
	time_list = []
	int_list = []
	n = 0
	for group in response['response']:
		deviation_pos_list.append(group['deviation_positive'])
		deviation_neg_list.append(group['deviation_negative'])
		variance_list.append(group['deviation_variance'])
		mean_list.append(group['deviation_mean'])
		time_list.append(datetime.datetime.fromtimestamp(float(group['time_string'])))
		n += 1
		int_list.append(n)

	ds.data['x'] = time_list
	ds.data['y'] = mean_list
	cursession().store_objects(ds)
	time.sleep(1)
	print 'Interval: %s' % t
	t += 1




	'''
	p1.circle(r, x1, line_color='black', line_width=1, fill_alpha=0.5, radius=1, fill_color='black', line_alpha=0.5, legend='Recorded Usage')
	p1.circle(r, x2, line_color='red', line_width=1, fill_alpha=0.5, radius=1, fill_color='red', line_alpha=0.5, legend='Short EMA(%smin)' % ((n2 * 15) / 60))
	p1.rect([(len(r) / 2)], d1, height=2, width=len(r), fill_color="blue", fill_alpha=0.2, line_color=None, legend='Max Trend')
	p1.rect([(len(r) / 2)], d2, height=2, width=len(r), fill_color="red", fill_alpha=0.2, line_color=None, legend='Min Trend')
	p1.rect([(len(r) / 2)], (d2 + (a1 / 2)), height=a1, width=len(r), fill_color="yellow", fill_alpha=0.1, line_color=None, legend='Normal Amplitude(%s)' % a1)
	p1.circle(r, x0, line_color='green', line_width=1, fill_alpha=0.5, radius=1, fill_color='green', line_alpha=0.5, legend='Long EMA(%smin)' % ((n1 * 15) / 60))
	'''
	'''
	# create a new figure
	p2 = figure(
	    tools="pan,box_zoom,reset,previewsave",
	    y_range=[0, y_r], title="CPU: Elasticsearch 1 - %s Samples" % sample,
	    x_axis_label='Ticks(15s) - %smin' % ((ra * 15) / 60), y_axis_label='Percent Usage'
	)

	# create plots!
	p2.line(r, x1, line_color='black', line_width=1, legend='Recorded Usage', line_alpha=0.7)
	p2.line(r, x2, line_color='red', line_width=4, legend='Short EMA(%smin)' % ((n2 * 15) / 60), line_alpha=0.5)
	p2.rect([(len(r) / 2)], d1, height=2, width=len(r), fill_color="blue", fill_alpha=0.2, line_color=None, legend='Max Trend')
	p2.rect([(len(r) / 2)], d2, height=2, width=len(r), fill_color="red", fill_alpha=0.2, line_color=None, legend='Min Trend')
	p2.rect([(len(r) / 2)], (d2 + (a1 / 2)), height=a1, width=len(r), fill_color="yellow", fill_alpha=0.1, line_color=None, legend='Normal Amplitude(%s)' % a1)
	p2.line(r, x0, line_color='green', line_width=4, legend='Long EMA(%smin)' % ((n1 * 15) / 60), line_alpha=0.9)
	'''
	# output to static HTML file

