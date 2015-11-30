#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2014

# Import main
#-----------------------------------------------------------------------#

import sys
sys.path.append("/opt/AXOL_Management/AXOL")
sys.path.append("/opt/AXOL_Management/AXOL/axol_node")
from celery.app.registry import TaskRegistry
from celery.utils.log import get_task_logger
from task_engine.TaskEngine import celery, TE
import os

# Application Start
#-----------------------------------------------------------------------#
print 'STARTING AXOL'

tasks = [
	'classes',
	]

TE.engine.autodiscover_tasks(tasks, related_name='axol_resource')
