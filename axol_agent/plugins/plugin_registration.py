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

from resources import ar_heartbeat
from resources import ar_processor
from resources import ar_memory
from resources import ar_disk
from resources import ar_service
from resources import ar_hq_logs
from resources import ar_mysql
from resources import ar_java_logs

ar_methods = {
	'heartbeat': ar_heartbeat.ARHeartbeat,
	'cpu': ar_processor.ARProcessor,
	'memory': ar_memory.ARMemory,
	'disk': ar_disk.ARDisk,
	'service': ar_service.ARService,
	'hq_logs': ar_hq_logs.ARHQLogs,
	'mysql': ar_mysql.ARMysql,
	'java_logs': ar_java_logs.ARJavaLogs,
    'get_recent_transactions': ar_get_recent_transactions.ARGetRecentTransactions
	}
