#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2014

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
