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

import smtplib, re, os
import datetime

class Messaging(object):
	"""docstring for Messaging"""
	def __init__(self):
		super(Messaging, self).__init__()
		pass

	def notification_type_2(self, name, data, group, alert_type=None):
		print 'Starting Message'
		header = 'Event Notice %s' % str(datetime.datetime.now())[:-7]
		message = '[START]:\n\n[NAME]: %s\n\n[ERRORS]:' % name
		message_2 = 'error on %s with' % name
		for error in data:
			message = message + '\n\n%s: %s' % (error, data[error])
			message_2 = message_2 + ' %s' % data[error]
		self.notify(
			message,
			message_2,
			header,
			group,
			alert_type
			)

	def send_text(self, recipient, username, password, message, header):
		msg = 'From: %s\nTo: %s\nSubject: Warning %s\n%s\n\nEnd Message' % (
			username,
			recipient,
			header,
			str(message)
			)
		server = smtplib.SMTP('smtp.mandrillapp.com',2525)
		server.starttls()
		server.login(
			username,
			password
			)
		server.sendmail(
			username,
			recipient,
			str(msg)
			)
		server.quit()

		return server

	def notify(self, message, message_2, header, group=None, alert_type=None):
		username = "user-mandril"
		password = "password"
		default_users = {
			'kelcey_text': 'fake@email.com'
			}
		recurring_users = {
			'kelcey_email': 'fake@email.com'
			}
		test = {
			'kelcey_email': 'fake@email.com'
			}
		operations = {
			'kelcey_email': 'fake@email.com'
			}
		if group == 'recurring':
			users = recurring_users
		elif group == 'test':
			users = test
		elif group == 'operations':
			users = operations
		else:
			users = default_users
		for user in users:
			print '---------------------'
			print 'user: %s' % user
			print 'alert_type: %s' % alert_type
			if alert_type != None:
				for method in alert_type:
					if method in user:
						msg = message
						print 'MESSAGING: Message sent'
						self.send_text(
							recipient=users[user],
							username=username,
							password=password,
							message=msg,
							header=header
							)
			else:
				print 'Error, no alert_type specified'
