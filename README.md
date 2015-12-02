AXOL Automation Platform
------------------------

Axol is a versatile task management platform designed to scale and handle millions of tasks.

Out of the box there are a few plugins for common things, but the idea is that any task can 
be created in a simple plugin. Examples would include:
* Data collection
* Realtime execution
* Any push style request
* Any pull stule request
* Feedback loops, open and closed

Installation Guide
------------------
* Development Setup
  * Minimum size: 
    * EC2 micro instance - AXOL, RMQ, LMDB
  * Install Guide
    * Comming Soon

* Cluster Setup
  * Minimum size: 
    * 2x EC2 micro instances - AXOL, RMQ, LMDB
  * Install Guide
    * Comming Soon

* High Performance Setup
  * Minimum size:
    * 3x EC2 micro instances - AXOL Node
    * 3x EC2 micro instances - RMQ Node
    * IPC: Elasticache Redis Micro - Option 1
    * IPC: LMDB on RMQ nodes - Option 2
  * Install Guide
    * Coming Soon

Plugin Creation Guide
---------------------
* Coming Soon

Core Components
---------------
* Celery
* Flask
* RabbitMQ
* LMDB

Optional Components
-------------------
* Elasticsearch
* Cassandra
* Elasticache
* Amazon SQS
* Amazon ELB
