#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2015

# Imports
#-----------------------------------------------------------------------#
import time
from axol_common.classes.common_data_object import GenericDataObject
from datetime import datetime

def insert(data_object, table_space):
	cols = []
	values = []
	query = 'begin batch '
	insert_time = int(time.time()) * 1000
	#insert_time = datetime.utcnow()
	time_string = str(time.time())
	data_object = GenericDataObject().convert(data_object)
	for server in data_object:
		if server != 'method':
			cols.append('insert_time')
			cols.append('time_string')
			values.append(str(insert_time))
			values.append(time_string)
			for key, value in data_object[server].iteritems():
				cols.append(key)
				values.append(value)
			command = 'insert into %s %s values %s;' % (
				table_space,
				str(tuple(cols)).replace('\'', ''),
				tuple(values)
				)
			cols = []
			values = []
			query = query + command
	query = query + ' APPLY BATCH'
	return query
