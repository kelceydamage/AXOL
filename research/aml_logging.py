#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

import logging, sys

class Logger(object):
	def __init__(self, logger_name, logging_level, log_file_path, format='%(asctime)s -%(levelname)s: %(message)s', date_format='%m/%d/%Y %I:%M:%S %p'):
		self.logger = logging.getLogger(logger_name)
		self.logger.setLevel(logging_level)
		logger_handler = logging.FileHandler(log_file_path)
		#logger_handler = logging.StreamHandler(sys.stderr)
		formatter = logging.Formatter(format, datefmt=date_format)
		logger_handler.setFormatter(formatter)
		self.logger.addHandler(logger_handler)
