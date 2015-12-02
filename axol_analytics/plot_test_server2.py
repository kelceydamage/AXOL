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
# The bokeh-server must be running to see this example

from bokeh.plotting import *
from bokeh.charts import *
from bokeh.models import GlyphRenderer
from bokeh.models import Range1d
from bokeh.models import HoverTool
import bokeh.embed as embed
import time
import sys
sys.path.append("/opt/AXOL_Management/AXOL")
from axol_common.classes.common_math import CommonMath
import socket
import json
from sys import getsizeof
import struct
import datetime
from numpy import pi, cos, sin, linspace, roll
import numpy as np

profiler = {}
profiler['start'] = time.time()

def receive_all(socket, n):
	data = ''
	while len(data) < n:
		packet = socket.recv(n - len(data))
		if not packet:
			return None
		data += packet
	return data

def receive_message(socket):
	raw_message_length = receive_all(socket, 4)
	if not raw_message_length:
		return None
	message_length = struct.unpack('>I', raw_message_length)[0]
	return receive_all(socket, message_length)

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
	request = receive_message(tls_sock)
	response = json.loads(request.decode('base64','strict'))
	return response

def format_data(start_time):
	command = "select deviation_mean, deviation_negative, deviation_positive, deviation_variance, \
	time_string from axol_metrics.clusters where source='cpu' and name='api' and insert_time > %s;" % start_time
	response = query([command])
	deviation_pos_list = []
	deviation_neg_list = []
	variance_list = []
	mean_list = []
	time_list = []
	time_list_2 = []
	int_list = []
	deviation_amount = []
	n = 0
	for group in response['response']:
		deviation_pos_list.append(group['deviation_positive'])
		deviation_neg_list.append(group['deviation_negative'])
		#variance_list.append(group['deviation_variance']/100)
		variance_list.append(
			((group['deviation_positive'] - group['deviation_mean']) / group['deviation_mean'])
			)
		mean_list.append(round(group['deviation_mean'], 2))
		time_list.append(
			time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(group['time_string'])))
			)
		time_list_2.append(datetime.datetime.fromtimestamp(float(group['time_string']) - 28800))
		n += 1
		int_list.append(n)
		deviation_amount.append(
			round(
				(group['deviation_mean'] / group['deviation_positive']), 2
				) * 20
			)
	return deviation_amount, mean_list, int_list, time_list, time_list_2, variance_list, deviation_neg_list, deviation_pos_list

def fudge_data(time_list_2):
	deviation_pos_list = []
	deviation_neg_list = []
	variance_list = []
	mean_list = []
	time_list = []
	int_list = []
	deviation_amount = []
	n = 0
	init_data_list = [
		1675,
		3223,
		2017,
		1501,
		2067,
		2500,
		1000,
		2972,
		1975,
		2104,
		2100,
		2973,
		1980
		]
	deviation = CommonMath.map_deviation(init_data_list)

	deviation_amount = [0 for i in range(len(init_data_list))]
	mean_list = init_data_list
	int_list = range(len(init_data_list))
	time_list = time_list_2[:len(init_data_list)]
	time_list_2 = time_list_2[:len(init_data_list)]
	variance_list = [0 for i in range(len(init_data_list))]
	deviation_neg_list = [0 for i in range(len(init_data_list))]
	deviation_pos_list = [0 for i in range(len(init_data_list))]

	return deviation_amount, mean_list, int_list, time_list, time_list_2, variance_list, deviation_neg_list, deviation_pos_list


def calculate_max_hits(mean_list, time_list_2):
	_max = max(mean_list)
	max_hits = []
	max_points = []
	mean_index = []
	n = 0
	for m in mean_list:
		if m > (_max * 0.90):
			print n
			max_hits.append(m)
			print 'MH: %s' % max_hits
			max_points.append(time_list_2[n])
			print 'MP: %s' % max_points
		n += 1
	return max_hits, max_points

def exponential_moving_average(mean_list, ra, n):
	r = []
	for i in range(ra):
	        r.append(i)
	p = ''
	a = (2 / (float(n) + 1))
	s1 = sum(mean_list[:n])
	EMAp = float(s1) / n
	EMA_list = []
	for p in mean_list[-ra:]:
		EMA = (p * a) + (EMAp * (1 - a))
		EMAp = EMA
		EMA_list.append(round(EMA, 2))
	return EMA_list

def calculate_cross(e1, e2, time_list_2, mean_list):
	status = ''
	cross_x = []
	cross_y = []
	cross_name = []
	n = 0
	last_n1 = 0
	last_n2 = 0
	name = ''
	trend = []
	trend_time = []
	trend_height = []
	t_next = []
	last_name = ''
	success = []
	e1.reverse()
	e2.reverse()
	time_list_2.reverse()
	for n1, n2, t1 in zip(e1, e2, time_list_2):
		print '--------------------------------'
		if n1 > last_n1:
			x = 100 - round(100 * (last_n1 / n1),  1)
			print 'CURRENT X: %s' % x
			if (last_n1 / n1) < 1.01:
				trend.append('>%s%%' % x)
				trend_time.append(t1)
				trend_height.append(n1)
			cross_x.append(t1)
			cross_y.append(max(mean_list) * 1.4)
			name = 'up'
		else:
			x = 100 - round(100 * (n1 / last_n1), 1)
			print 'CURRENT X: %s' % x
			if (n1 /last_n1) < 1.01:
				trend.append('>%s%%' % x)
				trend_time.append(t1)
				trend_height.append(n1)
			cross_x.append(t1)
			cross_y.append(max(mean_list) * 1.4)
			name = 'down'
		if n1 > n2:
			if status == 'dead':
				name = 'golden'
			status = 'golden'
		else:
			if status == 'golden':
				name = 'dead'
			status = 'dead'
		print 'X: %s, NAME: %s' % (x, name)
		if x > 3 and (name == 'up' or name == 'golden'):
			print 'chose up'
			if x > 11:
				print 'u11: %s' % name
				name_2 = 'up'
				t_next.append('%s+++' % name_2)
			elif x > 8:
				print 'u8: %s' % name
				name_2 = 'up'
				t_next.append('%s++' % name_2)
			elif x > 5:
				print 'u5: %s' % name
				name_2 = 'up'
				t_next.append('%s+' % name_2)
			else:
				print 'u3: %s' % name
				name_2 = 'up'
				t_next.append('%s' % name_2)
		elif x > 3 and (name == 'down' or name == 'dead'):
			print 'chose down'
			if x > 11:
				print 'd11: %s' % name
				name_2 = 'down'
				t_next.append('%s+++' % name_2)
			elif x > 8:
				print 'd8: %s' % name
				name_2 = 'down'
				t_next.append('%s++' % name_2)
			elif x > 5:
				print 'd5: %s' % name
				name_2 = 'down'
				t_next.append('%s+' % name_2)
			else:
				print 'd3: %s' % name
				name_2 = 'down'
				t_next.append('%s' % name_2)
		elif name == 'golden':
			print 'chose golden'
			name_2 = 'uncertain'
			t_next.append('uncertain')
		elif name == 'dead':
			print 'chose dead'
			name_2 = 'uncertain'
			t_next.append('uncertain')
		elif x > 1.5 and (name == 'up' or name == 'down'):
			print 'chose x > 1.5 < 3'
			name_2 = name
			t_next.append('%s-' % name_2)
		elif x > 0.5 and (name == 'up' or name == 'down'):
			print 'chose x > 1.5 < 3'
			name_2 = name
			t_next.append('%s--' % name_2)
		elif x > 0.1 and (name == 'up' or name == 'down'):
			print 'chose x > 1.5 < 3'
			name_2 = name
			t_next.append('%s---' % name_2)
		else:
			print 'chose [u]'
			name_2 = '[u]'
			t_next.append(name_2)
		print 'End routine'
		print 'X: %s, NAME: %s, Prediction: %s' % (x, name, t_next[n])
		cross_name.append(name)
		if name == 'golden':
			name = 'up'
		if name == 'dead':
			name = 'down'
		if name in last_name:
			success.append(5)
		else:
			success.append(0)
		last_name = name_2
		last_n1 = n1
		last_n2 = n2
		n += 1

	#       t_next.reverse()
	e2.reverse()
	e1.reverse()
	time_list_2.reverse()
	return cross_x, cross_y, cross_name, trend, trend_time, trend_height, t_next, success

def get_accuracy(success, t_next, mean_list):
	c1 = 0
	c2 = 0
	for z, z1 in zip(success, t_next):
		if z != 0:
			c1 += 1
		if z1 == '[u]' or z1 == 'uncertain':
			c2 += 1
	print '-----------------------'
	print c1
	print c2
	global_percentage = ['Prediction ACC: %s%%' % round((float(c1) / float(len(mean_list) - c2)) * 100, 2)]
	stats = ['Tried: %s/%s, Succeeded: %s, Refused: %s' % (len(mean_list) - c2, len(mean_list), c1, c2)]
	print stats
	return stats, global_percentage

# TUNING
#-----------------------------------------------------------------------#
# Plot Range

# Short EMA in ticks(15s intervals)
n2 = 60
# Long EMA in ticks(15s intervals)
n1 = 120
# Sample size from Elasticsearch
sample = 480
#-----------------------------------------------------------------------#

colors = [
	"#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce",
	"#ddb7b1", "#cc7878", "#933b41", "#550b1d"
]

profiler['setup'] = (time.time() - profiler['start'])
profiler['temp'] = time.time()

start_time = int((time.time() - 21600) * 1000)
deviation_amount, mean_list, int_list, time_list, time_list_2, variance_list, deviation_neg_list, deviation_pos_list = format_data(start_time)
profiler['format_data'] = (time.time() - profiler['temp'])
profiler['temp'] = time.time()
max_hits, max_points = calculate_max_hits(mean_list, time_list_2)
ra = len(mean_list)
profiler['max_hits'] = (time.time() - profiler['temp'])
profiler['temp'] = time.time()
#deviation_amount, mean_list, int_list, time_list, time_list_2, variance_list, deviation_neg_list, deviation_pos_list = fudge_data(time_list_2)
#n = 5
n = 100
EMA_list = exponential_moving_average(mean_list, ra, n)

profiler['ema_s'] = (time.time() - profiler['temp'])
profiler['temp'] = time.time()
#n = 10
n = 300
EMA_list_2 = exponential_moving_average(mean_list, ra, n)

profiler['ema_l'] = (time.time() - profiler['temp'])
profiler['temp'] = time.time()

cross_x, cross_y, cross_name, trend, trend_time, trend_height, t_next, success = calculate_cross(EMA_list, EMA_list_2, time_list_2, mean_list)

profiler['calculate_cross'] = (time.time() - profiler['temp'])
profiler['temp'] = time.time()

stats, global_percentage = get_accuracy(success, t_next, mean_list)
profiler['get_accuracy'] = (time.time() - profiler['temp'])
profiler['temp'] = time.time()

output_server("animated_2")
p = figure(
	name='API Cluster', y_range=Range1d(start=0, end=max(mean_list) * 1.7),
	plot_width=1100, plot_height=400, background_fill="#E8DDCB", x_axis_type="datetime",
	title='API Cluster'
	)
#---------------------------------------------------------------------------------------
p.line(
	x=time_list_2, y=deviation_pos_list, line_width=30, line_color='orange', line_alpha=0.2, name='line_3'#, legend='Positive Deviation'
	)
p.line(
	x=time_list_2, y=deviation_neg_list, line_width=30, line_color='orange', line_alpha=0.2, name='line_4'#, legend='Negative Deviation'
	)

p.rect(
	x=time_list_2, y=max(mean_list) * 1.15, width=30000, height=variance_list, name='rect_1', alpha=0.5#, legend='Variance'
	)
p.line(
	x=time_list_2, y=mean_list, line_width=10, line_color='orange', line_alpha=0.5, name='line_1'
	)

p.line(
	x=time_list_2, y=mean_list, line_width=3, line_color='black', line_alpha=0.6, name='line_2'#, legend='Mean Averages'
	)
p.circle(
	x=time_list_2, y=mean_list, size=deviation_amount, color='blue', alpha=0.15, name='circle_3'#, legend='Rate Of Deviation'
	)


p.line(
	x=time_list_2, y=EMA_list_2, line_width=5, line_color='grey', line_alpha=0.8, name='line_6'#, legend='EMA Long'
	)
p.line(
	x=time_list_2, y=EMA_list, line_width=10, line_color='white', line_alpha=0.9, name='line_5'#, legend='EMA Short'
	)
#---------------------------------------------------------------------------------------

p.circle(
	x=max_points, y=max_hits, size=35, name='circle_1', color='red', alpha=0.5, #legend='Top Ten Percent',
	line_alpha=0.3, line_color='white', line_width=4
	)

p.circle(
	x=max_points, y=max_hits, size=5, color='orange', name='circle_2'
	)
p.circle(
	x=time_list_2, y=EMA_list, size=3, color='grey', name='circle_4', line_color='blue', line_alpha=0.4
	)
p.circle(
	x=trend_time, y=max(mean_list) * 1.4, size=success, color='green', name='circle_5', line_alpha=0.6
	)


p.text(
	text=EMA_list, x=time_list_2, y=0, angle=1.58, name='text_1', text_font_size='10pt'
	)
p.text(
	text=max_hits, x=max_points, y=max_hits, angle=0.9, name='text_2'
	)
p.text(
	text=cross_name, x=cross_x, y=max(mean_list) * 1.4, angle=0.9, name='text_3', text_font_size='10pt'
	)
p.text(
	text=trend, x=trend_time, y=trend_height, angle=1.58, name='text_4', text_font_size='8pt'
	)
p.text(
	text=t_next, x=trend_time, y=max(mean_list) * 1.15, angle=1.58, name='text_5', text_font_size='8pt'
	)
p.text(
	text=global_percentage, x=[time_list_2[400]], y=max(mean_list) * 0.95, angle=0, name='text_6', text_font_size='20pt'
	)
p.text(
	text=stats, x=[time_list_2[400]], y=max(mean_list) * 0.90, angle=0, name='text_7', text_font_size='10pt'
	)
profiler['draw_chart'] = (time.time() - profiler['temp'])
profiler['temp'] = time.time()
push()
profiler['push'] = (time.time() - profiler['temp'])
profiler['temp'] = time.time()
tag = embed.autoload_server(p, cursession())
html = """
<html>
	<head></head>
	<body>
		%s
	</body>
</html>
"""
html = html % (tag)
with open("animated_embed.html", "w+") as f:
	f.write(html)
profiler['write_embed'] = (time.time() - profiler['temp'])
profiler['temp'] = time.time()
print("""
To view this example, run
	python -m SimpleHTTPServer (or http.server on python 3)
in this directory, then navigate to
""")


renderer = p.select(dict(type=GlyphRenderer))
for glyph in renderer:
	if glyph.name == 'line_1':
		line_1 = glyph.data_source
	elif glyph.name == 'line_2':
		line_2 = glyph.data_source
	elif glyph.name == 'line_3':
		line_3 = glyph.data_source
	elif glyph.name == 'line_4':
		line_4 = glyph.data_source
	elif glyph.name == 'line_5':
		line_5 = glyph.data_source
	elif glyph.name == 'line_6':
		line_6 = glyph.data_source
	elif glyph.name == 'circle_1':
		circle_1 = glyph.data_source
	elif glyph.name == 'circle_2':
		circle_2 = glyph.data_source
	elif glyph.name == 'circle_3':
		circle_3 = glyph.data_source
	elif glyph.name == 'circle_4':
		circle_4 = glyph.data_source
	elif glyph.name == 'circle_5':
		circle_5 = glyph.data_source
	elif glyph.name == 'text_1':
		text_1 = glyph.data_source
	elif glyph.name == 'text_2':
		text_2 = glyph.data_source
	elif glyph.name == 'text_3':
		text_3 = glyph.data_source
	elif glyph.name == 'rect_1':
		rect_1 = glyph.data_source
	elif glyph.name == 'text_4':
		text_4 = glyph.data_source
	elif glyph.name == 'text_5':
		text_5 = glyph.data_source
	elif glyph.name == 'text_6':
		text_6 = glyph.data_source
	elif glyph.name == 'text_7':
		text_7 = glyph.data_source

profiler['organize_glyphs'] = (time.time() - profiler['temp'])
print profiler

while True:
	profiler = {}
	profiler['start'] = time.time()
	start_time = int((time.time() - 21600) * 1000)
	deviation_amount, mean_list, int_list, time_list, time_list_2, variance_list, deviation_neg_list, deviation_pos_list = format_data(start_time)
	profiler['format_data'] = round(time.time() - profiler['start'], 6)
	profiler['temp'] = time.time()
	#deviation_amount, mean_list, int_list, time_list, time_list_2, variance_list, deviation_neg_list, deviation_pos_list = fudge_data(time_list_2)
	max_hits, max_points = calculate_max_hits(mean_list, time_list_2)
	profiler['max_hits'] = round(time.time() - profiler['temp'], 6)
	profiler['temp'] = time.time()
	#n = 5
	n = 100
	EMA_list = exponential_moving_average(mean_list, ra, n)
	profiler['ema_s'] = round(time.time() - profiler['temp'], 6)
	profiler['temp'] = time.time()
	#n = 10
	n = 300
	EMA_list_2 = exponential_moving_average(mean_list, ra, n)
	profiler['ema_l'] = round(time.time() - profiler['temp'], 6)
	profiler['temp'] = time.time()

	cross_x, cross_y, cross_name, trend, trend_time, trend_height, t_next, success = calculate_cross(EMA_list, EMA_list_2, time_list_2, mean_list)
	profiler['calculate_cross'] = round(time.time() - profiler['temp'], 6)
	profiler['temp'] = time.time()

	stats, global_percentage = get_accuracy(success, t_next, mean_list)
	print stats
	profiler['get_accuracy'] = round(time.time() - profiler['temp'], 6)
	profiler['temp'] = time.time()

	line_2.data['x'] = time_list_2
	line_2.data['y'] = mean_list
	line_1.data['line_width'] = deviation_amount
	line_3.data['x'] = time_list_2
	line_3.data['y'] = deviation_pos_list
	line_4.data['x'] = time_list_2
	line_4.data['y'] = deviation_neg_list
	line_5.data['x'] = time_list_2
	line_5.data['y'] = EMA_list
	line_6.data['x'] = time_list_2
	line_6.data['y'] = EMA_list_2
	circle_1.data['x'] = max_points
	circle_1.data['y'] = max_hits
	circle_2.data['x'] = max_points
	circle_2.data['y'] = max_hits
	circle_3.data['x'] = time_list_2
	circle_3.data['y'] = mean_list
	circle_3.data['size'] = deviation_amount
	circle_4.data['x'] = time_list_2
	circle_4.data['y'] = EMA_list
	circle_5.data['x'] = trend_time
	circle_5.data['size'] = success
	text_1.data['text'] = EMA_list
	text_1.data['x'] = time_list_2
	text_2.data['text'] = max_hits
	text_2.data['x'] = max_points
	text_2.data['y'] = max_hits
	text_3.data['text'] = cross_name
	text_3.data['x'] = cross_x
	text_3.data['y'] = cross_y
	rect_1.data['x'] = time_list_2
	rect_1.data['height'] = variance_list
	text_4.data['x'] = trend_time
	text_4.data['y'] = trend_height
	text_4.data['text'] = trend
	text_5.data['x'] = trend_time
	text_5.data['text'] = t_next
	text_6.data['x'] = [time_list_2[400]]
	text_6.data['text'] = global_percentage
	text_7.data['x'] = [time_list_2[400]]
	print stats
	text_7.data['text'] = stats
	print stats
	line_1.data['x'] = time_list_2
	line_1.data['y'] = mean_list

	profiler['update_data'] = round(time.time() - profiler['temp'], 6)
	profiler['temp'] = time.time()

	cursession().store_objects(line_2, line_3, line_4,
		line_5, line_6, circle_1, circle_2, circle_3, text_1,
		text_2, text_3, rect_1, circle_4, circle_5, text_4, text_5,
		text_6, text_7, line_1
		)

	profiler['update_session'] = round(time.time() - profiler['temp'], 6)
	print profiler
	time.sleep(5)
