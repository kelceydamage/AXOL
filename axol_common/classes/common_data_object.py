#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

import ast
import collections

class GenericDataObject(object):
	"""GenericDataObject creates a dynamic object whose attributes are determined at
	instanciations via a dict passed as args"""
	def __init__(self, args={}):
		super(GenericDataObject, self).__init__()
		self._set_attributes(args)

	def _set_attributes(self, args):
		for item in args:
			setattr(self, item, args[item])

	def print_attributes_with_values(self):
		for value in self.__dict__:
			print '%s: %s' % (value, self.__dict__[value])

	def print_all_attributes(self):
		for value in (value for value in dir(self) if '__' not in value):
			print value

	def return_attribute_dict(self):
		return self.__dict__

	def converted_attribute_dict(self):
		return self.convert(self.__dict__)

	def convert(self, data):
		if isinstance(data, basestring):
			return data.encode('latin-1')
		elif isinstance(data, collections.Mapping):
			return dict(map(self.convert, data.iteritems()))
		elif isinstance(data, collections.Iterable):
			return type(data)(map(self.convert, data))
		elif data == None:
			return 'None'
		else:
			return data
