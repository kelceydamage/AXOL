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
#+

import os, sys, re, subprocess, tty, argparse, termios
import MySQLdb as mdb

user = 'select_user'
password = 'password'
host = 'ip'
host_production = 'ip'
version = 'v0.9.9a-8371'

class Select(object):
	"""docstring for Select"""
	def __init__(self, user, password, host, host_production, version):
		super(Select, self).__init__()
		self.menu_bar = '\n\033[40m\033[1m\033[37m\033[31m[x]\033[0m \033[22mExit\033[1m \033[40m\033[32m[c]\033[0m \
\033[22mMain Menu\033[1m \033[40m\033[32m[d]\033[0m \033[22mDescribe Table By ID\033[1m \033[40m\033[32m[f]\033[0m \
\033[22mFormat\033[1m \033[40m\033[32m[m]\033[0m \033[22mMirror Mode\033[1m \033[40m\033[32m[q]\033[0m \033[22mQuery \
Mode (Raw SELECT Query)\033[0m\n'
		self.version = '\033[44m\033[1m\033[37m### SELECT %s ###\033[0m\n' % version
		self.user = user
		self.password = password
		self.host = host
		self.host_production = host_production
		self.database = ''
		self.mirror_mode = False
		self.columns = 6
		self.db_columns = 2
		self.query_result = []
		self.query_result_2 = []
		self.record_divider = '_________________________________'
		self.record_divider_2 = '________________________________________________________'
		self.spacer = '        '
		self.buffer = ''
		self._init()

	def _init(self):
		self._connect()
		self.cursor.execute('show databases')
		self.query_result = []
		for item in self.cursor.fetchall():
			self.query_result.append(item)
		self.database_list = self.query_result
		self._display_menu()

	def _print_record_divider(self, columns, divider):
		for item in range(int(columns)):
			if item == 0:
				record_divider = '         ' + divider
			else:
				record_divider = record_divider + divider
		return record_divider

	def _connect(self, database=''):
		self.cnx = mdb.connect(
			user=self.user,
			passwd=self.password,
			host=self.host,
			db=database
			)
		self.cnx2 = mdb.connect(
			user=self.user,
			passwd=self.password,
			host=self.host_production,
			db=database
			)
		self.cursor = self.cnx.cursor()
		self.cursor_2 = self.cnx2.cursor()

	def _query(self, query, parent=''):
		def __query(query, parent):
			def ___build_list(cursor, query, result):
				cursor.execute(query)
				q_r = cursor.fetchall()
				for row in q_r:
					new_list = []
					for column in row:
						new_list.append(column)
					while not len(new_list) % 3 == 0:
						new_list.append('')
					result.append(new_list)

			___build_list(
				cursor=self.cursor,
				query=query,
				result=self.query_result
				)
			___build_list(
				cursor=self.cursor_2,
				query=query,
				result=self.query_result_2
				)

			self._display_result(
				result=self.query_result,
				result_2=self.query_result_2,
				parent=parent
				)

		def __error(e, parent):
			self.query_result = ('Error: ', str(e))
			self.query_result_2 = ('Error: ', str(e))
			self._display_result(
				result=self.query_result,
				result_2=self.query_result_2,
				e=e,
				parent=parent
				)

		self.query_result = []
		self.query_result_2 = []
		try:
			__query(
				query=query,
				parent=parent
				)
		except Exception, e:
			__error(
				e=e,
				parent=parent
				)

	def _close(self):
		self.cursor.close()
		self.cnx.close()
		self.cursor_2.close()
		self.cnx2.close()

	def _describe_table(self):
		record = raw_input('Please enter the table number: ')
		try:
			table = self.record_dict[int(record)][0]
		except Exception, e:
			table = record
		self._query(
			query='describe %s' % table,
			parent=table
			)

	def _display_result(self, result, result_2='', e='', parent=''):
		def __spacing(count_2='',count_4=0, len_data=1, _type=''):
			if self.mirror_mode == False:
				if (count_2 % int(self.columns)) == 0:
					if _type == 'header':
						print '\n',self.spacer,
					else:
						print '\n',self.spacer,
			else:
				if self.len_data < 2:
					if (count_2 % self.len_data) == 0:
						print self.spacer,
				else:
					if (count_2 % int(self.columns)) == 0:
						if _type == 'header':
							print '\n',self.spacer,
						else:
							print '\n',self.spacer,
					elif (count_2 % 3) == 0:
						print self.spacer,

		def __data_view(count_2, count_3, parent, _type, data_set='', data_set_2='', count=0):
			def ___divider_style():
				if self.mirror_mode == False:
					print self.buffer
					print self._print_record_divider(
						columns=self.columns,
						divider=self.record_divider
						)
				else:
					print self.buffer
					print '%s%s' % (
						self._print_record_divider(
							columns=self.columns / 2,
							divider=self.record_divider
							),
						self._print_record_divider(
							columns=self.columns / 2,
							divider=self.record_divider
							)
						)

			def ___header_check():
				def ____build_list(description, data_set):
					for row in description:
						new_list = []
						for column in row:
							new_list.append(column)
						data_set.append(new_list)
					while not len(data_set) % 3 == 0:
						data_set.append([''])
					return data_set

				if self.cursor.description == None or self.cursor_2.description == None:
					data_set = [['',]]
					data_set_2 = [['',]]
				else:
					data_set = []
					data_set_2 = []

					data_set = ____build_list(
						description=self.cursor.description,
						data_set=data_set
						)
					data_set_2 = ____build_list(
						description=self.cursor_2.description,
						data_set=data_set_2
						)

				return data_set, data_set_2

			def ___print_op(data_set, count, count_2, x, y, record_ids):
				if _type == 'header':
					print_block = '\033[40m\033[1m\033[37m|-- %-24s --|\033[0m'
					print print_block % data_set[count_2][0],
				else:
					print_block = '%-32s'
					try:
						print print_block % data_set[y][count_2],
					except Exception:
						pass

				count = count + x
				count_2 = count_2 + 1
				if count_2 >= self.len_data:
					count_2 = 0
				return count, count_2

			count_4 = 0
			count_5 = 0
			count_6 = 0
			if _type == 'header':
				data_set, data_set_2 = ___header_check()
				print_block = '\033[40m\033[1m\033[37m|-- %-24s --|\033[0m'
				self.len_data = len(data_set)
				if parent != '':
					print self.spacer,print_block % parent

			record_ids = range(len(data_set)+1)
			if self.len_data == self.len_data:
				while count_3 < (self.len_data * 2):
					__spacing(
						count_2=count_2,
						count_4=count_4,
						len_data=self.len_data,
						_type=_type
						)
					if self.mirror_mode == False:
						count_3, count_4 = ___print_op(
							data_set=data_set,
							count=count_3,
							count_2=count_4,
							x=2,
							y=count,
							record_ids=record_ids
							)
					else:
						if count_6 < 3:
							count_6, count_4 = ___print_op(
								data_set=data_set,
								count=count_6,
								count_2=count_4,
								x=1,
								y=count,
								record_ids=record_ids
								)
						else:
							count_6, count_5 = ___print_op(
								data_set=data_set_2,
								count=count_6,
								count_2=count_5,
								x=1,
								y=count,
								record_ids=record_ids
								)
						count_3 = count_3 + 1
					count_2 = count_2 + 1
					if count_6 == self.len_data \
					or count_6 == 6:
						count_6 = 0
				if _type == 'body':
					___divider_style()

		if self.mirror_mode == True:
			self.columns = 6
		if str(result[1]) == str(e):
			data_set = [result,(0)]
			data_set_2 = [result_2,(0)]
		else:
			data_set = result
			data_set_2 = result_2

		record_dict = {}
		menu_selection = ''
		while not re.search(r'x|a|c', menu_selection):
			count = 0
			count_2 = 0
			count_3 = 0
			os.system('clear')
			os.system('clear')
			print self.version
			__data_view(
				count_2=count_2,
				count_3=count_3,
				parent=parent,
				_type='header'
				)
			print self.buffer
			for item in data_set:
				__data_view(
					count_2=count_2,
					count_3=count_3,
					parent=parent,
					_type='body',
					data_set=data_set,
					data_set_2=data_set_2,
					count=count
					)
				count = count + 1
			print self.buffer
			self._menu_actions()

	def _display_menu(self):
		menu_selection = ''
		while not re.search(r'[0-9]|x|a|c', menu_selection):
			os.system('clear')
			db_map = self._build_db_menu()
			menu_selection = self._menu_actions()
		try:
			self.database = db_map[int(menu_selection)]
		except Exception, e:
			self._display_menu()
		self._list_tables()

	def _list_tables(self):
		menu_selection = ''
		self._connect(self.database)
		self.cursor.execute('show tables')
		result_list = self.cursor.fetchall()
		header = self.cursor.description
		record_ids = range(len(result_list)+1)
		self.record_dict = {}

		while not re.search(r'x|a|c', menu_selection):
			os.system('clear')
			count = 0
			print self.version
			print self.spacer,
			print '\033[40m\033[1m\033[37m[-- Tables in %s --]\033[0m' % self.database
			for record, record_id in zip(result_list, record_ids[1:]):
				column_list = range(len(record))
				self.record_dict[record_id] = record
				if (count % int(self.db_columns)) == 0:
					print self.buffer
					print self.spacer,
				print '\033[40m\033[1m\033[32m[%-6s]\033[0m %-44s' % (
					record_id,
					str(record[0])
					),
				count = count + 1
			count = 0

			print self.buffer
			self._print_record_divider(
				columns=self.db_columns,
				divider=self.record_divider_2
				)
			self._menu_actions()

	def _user_input_no_delay(self):
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(
				fd,
				termios.TCSADRAIN,
				old_settings
				)

		return ch

	def _build_db_menu(self):
		print self.version
		print self.spacer,
		print '\033[40m\033[1m\033[37m[-- Database Selection --]\033[0m\n'
		count = 1
		db_map = {}
		while count < len(self.database_list)+1:
			print '         \033[40m\033[1m\033[37m\033[32m[%-6s]\033[37m\033[0m %s' % (
				count,
				self.database_list[count-1][0]
				)
			db_map[count] = self.database_list[count-1][0]
			count = count + 1

		return db_map

	def _build_select_query(self):
		select_query = raw_input('Please enter your \033[40m\033[1m\033[37m[ SELECT ]\033[0m query: ')
		self._query(
			query=select_query,
			parent=self.database
			)

	def _menu_actions(self):
		print self.menu_bar
		menu_selection = self._user_input_no_delay()
		if menu_selection == 'x':
			self._close()
			exit('Program terminated by user')
		elif menu_selection == 'q':
			self._build_select_query()
		elif menu_selection == 'c':
			self._init()
		elif menu_selection == 'f':
			if self.mirror_mode == False:
				print 'Please enter the number of columns to be printed [0-9]: '
				self.columns = self._user_input_no_delay()
				if not re.search(r'[0-9]', str(self.columns)):
					print 'Invalid selection'
					self.columns = 6
				if int(self.columns) == 0:
					self.columns = 1
				print self.columns
			else:
				self.columns = 6
		elif menu_selection == 'd':
			self._describe_table()
		elif menu_selection == 'm':
			if self.mirror_mode == False:
				self.mirror_mode = True
				self.columns = 6
			else:
				self.mirror_mode = False
		else:
			pass
		return menu_selection

S = Select(
	user,
	password,
	host,
	host_production,
	version
	)
