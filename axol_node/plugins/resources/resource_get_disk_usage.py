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
import re

class ResourceGetDiskUsage(AxolResource):
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
		super(ResourceGetDiskUsage, self).__init__()
		self.source = 'disk'
		self.local = False
		self.store = True
		self.profiler = True

	def _show_help(self):
		return {
			'help': {
				'usage': '/api/get_disk_usage',
				'method': 'POST',
				'required_data': {
					'role': '<some role>',
					'alert_type': ['email', 'text']
					},
				'version': api
				}
			}

	@staticmethod
	@app.route('/api/get_disk_usage', methods=['GET', 'POST'])
	def api_get_disk_usage():
		if request.method == 'GET':
			return jsonify(ResourceGetDiskUsage()._show_help())
		try:
			data = CommonResource.handle_request(
				request=request,
				params=ResourceGetDiskUsage.required_post
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='get_disk_usage',
				method='api_get_disk_usage'
				)
			return jsonify(report)
		try:
			response = ResourceGetDiskUsage().create_async_job(
				data=data
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='get_disk_usage',
				method='api_get_disk_usage'
				)
			return jsonify(report)
		return jsonify(response)

	def calculate_new_fields(self, response_object):
		def calculate_current_usage(response_object):
			disk_list = []
			for attr in response_object.__dict__:
				if re.search(r'disk.*', attr):
					usage = getattr(response_object, attr)
					disk_list.append(int(usage['percent_used']))
			response_object.current_usage = float(max(disk_list))
			return response_object

		def calculate_usage_for_health(response_object):
			response_object.normalized_indicator = response_object.current_usage / 100
			response_object.multiplier = 1
			response_object.threshold_red = 80
			response_object.scale = 50
			return response_object

		if response_object.error == None:
			response_object = calculate_current_usage(
				response_object=response_object
				)
			response_object = calculate_usage_for_health(
				response_object=response_object
				)
			response_object.health_indicator = CommonMath.adaptive_filtration(
				normalized_indicator=response_object.normalized_indicator,
				multiplier=response_object.multiplier,
				threshold_red=response_object.threshold_red,
				scale=response_object.scale
				)
			self.threshold_validation(response_object)
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
				table_space='axol_metrics.disk_usage'
				)]
			)
