#! /usr/bin/env python
#-----------------------------------------#
#Copyright [2015] [Kelcey Jamison-Damage]

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

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
