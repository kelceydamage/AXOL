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

#axol_node = '10.100.10.34'

# API
#-----------------------------------------------------------------------#
api = {
	'version_name': 'Wonderboom',
	'version_number': '1.2.0'
	}

# Queue
#-----------------------------------------------------------------------#

'''
backend='amqp://celery:PASSWORD@localhost:5672/celery'
broker='amqp://celery:PASSWORD@localhost:5672/celery'

# For AWS
'''
backend = 'amqp://celery:PASSWORD@internal-axol-broker-internal-2120577614.us-west-2.elb.amazonaws.com:5672/celery'
broker = 'amqp://celery:PASSWORD@internal-axol-broker-internal-2120577614.us-west-2.elb.amazonaws.com:5672/celery'

# Cache
#-----------------------------------------------------------------------#

cache = 'elasticache'
'''
cache = 'lmdb'
'''
# Elasticsearch
#-----------------------------------------------------------------------#

node = 'internal-Elasticsearch-Internal-LB-729281810.us-west-2.elb.amazonaws.com:80'
'''
node = 'Elasticsearch-Cluster-1549281915.us-west-2.elb.amazonaws.com:80'
'''
# Logger
#-----------------------------------------------------------------------#
log_params = {
	'source': 'axol_event',
	'name': 'event_notice'
	}


