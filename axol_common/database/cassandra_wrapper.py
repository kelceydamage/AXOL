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
