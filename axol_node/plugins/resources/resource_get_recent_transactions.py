#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
from axol_common.classes.common_logger import CommonLogger
from axol_common.classes.common_data_object import GenericDataObject
from axol_common.classes.common_resource import CommonResource
from axol_common.classes.common_math import CommonMath
from axol_common.database.cassandra_wrapper import insert
from classes.axol_resource import AxolResource
from axol_config import api
from aapi.aapi import app as app
from flask import jsonify
from flask import request

class ResourceGetRecentTransactions(AxolResource):
	"""docstring for ResourceGetRecentTransactions
	Must implement:
		_show_help()
		self.source = {keyword}
		self.local = Bool
		self.store = Bool
		self.profiler = Bool
		api_<name of your api>()
		calculate_new_fields()
		write_to_database()
	Optional:
		if self.store = True, write_to_database() function must be implemented
	"""
	required_post = {
		'role': (True, u's'),
		'profile': (False, u's')
		}

	def __init__(self):
		super(ResourceGetRecentTransactions, self).__init__()
		self.source = 'get_recent_transactions'
		self.local = False
		self.store = True
		self.profiler = True

	def _show_help(self):
		return {
			'help': {
				'usage': '/api/get_recent_transactions',
				'method': 'POST',
				'required_data': {
					'role': '<some role>'
					},
				'version': api
				}
			}

	@staticmethod
	@app.route('/api/get_recent_transactions', methods=['GET', 'POST'])
	def api_get_recent_transactions():
		if request.method == 'GET':
			return jsonify(ResourceGetRecentTransactions()._show_help())
		try:
			data = CommonResource.handle_request(
				request=request,
				params=ResourceGetRecentTransactions.required_post
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='get_recent_transactions',
				method='api_get_recent_transactions-1'
				)
			return jsonify(report)
		try:
			response = ResourceGetRecentTransactions().create_async_job(
				data=data
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='get_recent_transactions',
				method='api_get_recent_transactions-2'
				)
			return jsonify(report)
		return jsonify(response)

	def write_to_database(self, axol_task_value):
		pass
	'''
		self.query([
			insert(
				data_object=axol_task_value,
				table_space='axol_metrics.processor_usage'
				)]
			)
	'''
