#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

import socket
import time
import sys
sys.path.append("/opt/AXOL_Management/AXOL/axol_node")
from processing import Processing
import ssl
import re
import os
import pickle
from multiprocessing import current_process
import base64
from auto_roledefs import *
import json

host = 'ip'
client_socket = socket.socket(
	socket.AF_INET,
	socket.SOCK_STREAM
	)
tls_sock = ssl.wrap_socket(
	client_socket,
	cert_reqs=ssl.CERT_NONE,
	do_handshake_on_connect=False,
	ssl_version=ssl.PROTOCOL_TLSv1
	)
tls_sock.settimeout(1)
error = 'undefined'
try:
	tls_sock.connect((host,9999))
	try:
		tls_sock.send('hello')
		error = None
	except Exception, e:
		error = str(e)
		print 'AGENT ERROR {__connect|send}: %s' % error
except Exception, e:
	error = str(e)
	print 'AGENT ERROR {__connect|connect}: %s %s' % (host, error)
