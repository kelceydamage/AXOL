#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2014

# Import main
#-----------------------------------------------------------------------#
import sys
sys.path.append("/opt/AXOL_Management/AXOL")
from aapi.aapi import app as app

# Import AXOL APIs (Registry)
#-----------------------------------------------------------------------#
from plugins.resources.resource_template import ResourceTemplate
from plugins.resources.resource_get_processor_usage import ResourceGetProcessorUsage
from plugins.resources.resource_get_memory_usage import ResourceGetMemoryUsage
from plugins.resources.resource_get_disk_usage import ResourceGetDiskUsage
from plugins.resources.resource_get_all_roles import ResourceGetAllRoles
from plugins.resources.resource_get_alert_servers import ResourceGetAlertServers
from plugins.resources.resource_get_production_servers import ResourceGetProductionServers
from plugins.resources.resource_create_event_notice import ResourceCreateEventNotice
from plugins.resources.resource_remove_alert_server import ResourceRemoveAlertServer
from plugins.resources.resource_restore_alert_servers import ResourceRestoreAlertServers
from plugins.resources.resource_send_warnings_alerts import ResourceSendWarningsAlerts
from plugins.resources.resource_create_log_entry import ResourceCreateLogEntry
from plugins.resources.resource_get_recent_transactions import ResourceGetRecentTransactions

from plugins.resources.resource_administration import ResourceAdmin
request_admin_api = ResourceAdmin.request_admin_api
'''
from plugins.resources.resource_dashboard import ResourceDashboard
request_dashboard_api = ResourceDashboard.request_dashboard_api
'''

# Application Start
#-----------------------------------------------------------------------#
if __name__ == '__main__':

	app.debug = True
	app.run(host='0.0.0.0')

