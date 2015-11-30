#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

class DataType(object):
	"""DataType Object creates a dynamic object whose attributes are determined at
	instanciations via a dict passed as args"""
	def __init__(self, args):
		super(DataType, self).__init__()
		self._set_attributes(args)

	def _set_attributes(self, args):
		for item in args:
			setattr(self, item, args[item])

	def list_dynamic_attributes(self):
		for value in self.__dict__:
			print value, self.__dict__[value]

	def list_all_attributes(self):
		for value in (value for value in dir(self) if '__' not in value):
			print value
