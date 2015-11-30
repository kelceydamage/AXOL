#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

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


