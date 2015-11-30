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

class ResourceGetProcessorUsage(AxolResource):
	"""docstring for ResourceGetProcessorUsage
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
		super(ResourceGetProcessorUsage, self).__init__()
		self.source = 'cpu'
		self.local = False
		self.store = True
		self.profiler = True

	def _show_help(self):
		return {
			'help': {
				'usage': '/api/get_processor_usage',
				'method': 'POST',
				'required_data': {
					'role': '<some role>'
					},
				'version': api
				}
			}

	@staticmethod
	@app.route('/api/get_processor_usage', methods=['GET', 'POST'])
	def api_get_processor_usage():
		if request.method == 'GET':
			return jsonify(ResourceGetProcessorUsage()._show_help())
		try:
			data = CommonResource.handle_request(
				request=request,
				params=ResourceGetProcessorUsage.required_post
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='get_processor_usage',
				method='api_get_processor_usage-1'
				)
			return jsonify(report)
		try:
			response = ResourceGetProcessorUsage().create_async_job(
				data=data
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='get_processor_usage',
				method='api_get_processor_usage-2'
				)
			return jsonify(report)
		return jsonify(response)

	def calculate_new_fields(self, response_object):
		def calculate_current_usage(response_object):
			n = float(response_object.one_minute) * 100
			n = float(n) / float(response_object.number_of_processing_units)
			if n == 0:
				n = 1
			response_object.current_usage = n
			return response_object

		def calculate_usage_for_health(response_object):
			x = (2 * float(response_object.one_minute) + 3 * float(response_object.five_minute)) / 5
			response_object.normalized_indicator = x
			response_object.multiplier = response_object.number_of_processing_units
			response_object.threshold_red = 100
			response_object.scale = 0
			return response_object

		if response_object.error == None:
			response_object = calculate_usage_for_health(
				response_object=response_object
				)
			response_object = calculate_current_usage(
				response_object=response_object
				)
			response_object.health_indicator = CommonMath.adaptive_filtration(
				normalized_indicator=response_object.normalized_indicator,
				multiplier=response_object.multiplier,
				threshold_red=response_object.threshold_red,
				scale=response_object.scale
				)
			response_object = self.threshold_validation(response_object)
		return response_object

	def post_processing(self, axol_task_value):
		clusters = {'api': [], 'web': []}
		clusters = CommonMath.derive_clusters(
			clusters=clusters,
			map_value='current_usage',
			axol_task_value=axol_task_value
			)
		for cluster in clusters:
			clusters[cluster] = CommonMath.map_deviation(
				integer_list=clusters[cluster]
			)
			clusters[cluster]['source'] = self.source
			clusters[cluster]['name'] = cluster
		self.query([
			insert(
				data_object=clusters,
				table_space='axol_metrics.clusters'
				)]
			)
		return axol_task_value

	def write_to_database(self, axol_task_value):
		self.query([
			insert(
				data_object=axol_task_value,
				table_space='axol_metrics.processor_usage'
				)]
			)
