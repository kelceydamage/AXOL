#! /usr/bin/env python
#-----------------------------------------#
# Copyright [2015] [Kelcey Jamison-Damage]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Imports
#-----------------------------------------------------------------------#
from math import *

class CommonMath(object):
	"""docstring for CommonMath"""
	def __init__(self):
		super(CommonMath, self).__init__()
		pass

	@staticmethod
	def derive_clusters(clusters, map_value, axol_task_value):
		for name in axol_task_value:
			if 'api' in name:
				clusters['api'].append(axol_task_value[name][map_value])
			elif 'web' in name:
				clusters['web'].append(axol_task_value[name][map_value])
		return clusters

	@staticmethod
	def map_deviation(integer_list):
		a = integer_list
		x = sum(a)
		if len(integer_list) == 0:
			z = 1
		else:
			z = len(integer_list)
		y = x / z
		mean = float(round(y, 2))
		variance = sum(pow((value - mean), 2) for value in integer_list) / z
		deviation = round(sqrt(float(variance)), 2)
		results = {
			'deviation_positive': mean + deviation,
			'deviation_negative': mean - deviation,
			'deviation_mean': mean,
			'deviation_variance': variance
			}
		return results

	@staticmethod
	def adaptive_filtration(normalized_indicator, multiplier, threshold_red, scale):
		x = normalized_indicator
		n = multiplier
		h = threshold_red
		z = scale
		k = 100000
		def calculate_zero(h, k):
			a = (pow(h, 2) - h + k) / pow(h, 3)
			return a

		def calculate_envelope(h, a, k):
			b = (k - ((a * pow(h, 3)) - (0.01 * (a * pow(h, 2))))) / h
			return b

		def normalize_x(x, n):
			x = (float(x) / float(n)) * 100
			return x

		a = calculate_zero(h, k)
		b = calculate_envelope(h, a, k)
		x = normalize_x(x, n)
		y = 100 - ((a * pow(x, 3)) - (0.01 * a * pow(x, 2)) + b * x) / 1000 + z
		if y >= 100:
			y = 100
		return round(y, 2)

