#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

from datetime import datetime
import time

def base10_to_base_x(n, base):

	def match_char(number_list):
		convert_string = ''
		key = ('0','1','2','3','4','5','6','7','8','9', \
			'A','B','C','D','E','F','G','H', 'I','J','K', \
			'L','M','N','O','P','Q','R','S','T','U','V','W','X')
		for number in number_list:
			convert_string += key[number]
		return convert_string[::-1]

	number_list = []
	while n != 0:
		n, remainder = divmod(n, base)
		number_list.append(remainder)

	convert_string = match_char(number_list)
	return convert_string

def base_x_to_base10(n, base):

	def match_char(number_list):
		new_number_list = []
		key = ('0','1','2','3','4','5','6','7','8','9', \
			'A','B','C','D','E','F','G','H', 'I','J','K', \
			'L','M','N','O','P','Q','R','S','T','U','V','W','X')
		for char in number_list:
			if char in key:
				new_number_list.append(key.index(char))
		return new_number_list

	converted_string = 1
	counter = 0
	new_number_list = match_char(n)
	for i in new_number_list:
		if len(new_number_list) > (counter + 1):
			converted_string = converted_string * base + new_number_list[counter +1 ]
		else:
			pass
		counter += 1

	return converted_string

def format_record_id(date, time, ms, merchant_id, transaction_id):
	string_list = [date, time, ms, merchant_id, transaction_id]

	def pad_string(value, size):
		pass

	def colate_string(string_list):
		encoded_string = ''
		for string in string_list:
			encoded_string += string.rstrip('0') + '::'
		return encoded_string

	encoded_string = colate_string(string_list)
	return encoded_string

def decode_string(string):
	string_list = string.split('::')
	keys = (5, 4, 3, 7, 7)

	def re_pad_string(string_list, keys):
		new_string_list = []
		for string, key in zip(string_list, keys):
			if len(string) < key:
				n = key - len(string)
				string += '0' * n
				new_string_list.append(string)
			else:
				new_string_list.append(string)
		return new_string_list

	new_string_list = re_pad_string(string_list, keys)
	decoded_string = ''
	for string in new_string_list:
		decoded_string += string + '::'
	return decoded_string


# How to use this library:

dt = datetime.utcnow()
date = int(dt.strftime('%d%m%Y'))
time = int(dt.strftime('%H%M%S'))
ms = str(dt.strftime('%f'))[:4]

e = format_record_id(
	base10_to_base_x(date, 32),
	base10_to_base_x(time, 32),
	base10_to_base_x(int(ms), 32),
	base10_to_base_x(2147483648, 32),
	base10_to_base_x(2147483648, 32)
	)

z = base10_to_base_x(str({'data': {'WritebackTmp': 0, 'SwapTotal': 917500, 'Active(anon)': 573060, 'SwapFree': 901280, 'KernelStack': 1568, 'MemFree': 176644, 'HugePages_Rsvd': 0, 'Committed_AS': 1415616, 'NFS_Unstable': 0, 'Writeback': 0, 'Inactive(file)': 139400, 'MemTotal': 1692560, 'VmallocUsed': 11272, 'HugePages_Free': 0, 'AnonHugePages': 0, 'Shmem': 368, 'Inactive': 385188, 'Active': 995996, 'MemUsed': 1515916, 'Inactive(anon)': 245788, 'CommitLimit': 1763780, 'Hugepagesize': 2048, 'Cached': 421452, 'SwapCached': 3884, 'VmallocTotal': 34359738367, 'VmallocChunk': 34359724940, 'Dirty': 16, 'Mapped': 25852, 'SUnreclaim': 18892, 'Unevictable': 0, 'SReclaimable': 71728, 'Slab': 90620, 'DirectMap2M': 0, 'HugePages_Surp': 0, 'Bounce': 0, 'HugePages_Total': 0, 'AnonPages': 815520, 'PageTables': 14068, 'HardwareCorrupted': 0, 'DirectMap4k': 1748992, 'Mlocked': 0, 'Buffers': 141252, 'Active(file)': 422936}, 'd_time': 0.17880487442016602, 'server': u'54.201.95.77'}), 32)


d = decode_string(str({'data': {'WritebackTmp': 0, 'SwapTotal': 917500, 'Active(anon)': 573060, 'SwapFree': 901280, 'KernelStack': 1568, 'MemFree': 176644, 'HugePages_Rsvd': 0, 'Committed_AS': 1415616, 'NFS_Unstable': 0, 'Writeback': 0, 'Inactive(file)': 139400, 'MemTotal': 1692560, 'VmallocUsed': 11272, 'HugePages_Free': 0, 'AnonHugePages': 0, 'Shmem': 368, 'Inactive': 385188, 'Active': 995996, 'MemUsed': 1515916, 'Inactive(anon)': 245788, 'CommitLimit': 1763780, 'Hugepagesize': 2048, 'Cached': 421452, 'SwapCached': 3884, 'VmallocTotal': 34359738367, 'VmallocChunk': 34359724940, 'Dirty': 16, 'Mapped': 25852, 'SUnreclaim': 18892, 'Unevictable': 0, 'SReclaimable': 71728, 'Slab': 90620, 'DirectMap2M': 0, 'HugePages_Surp': 0, 'Bounce': 0, 'HugePages_Total': 0, 'AnonPages': 815520, 'PageTables': 14068, 'HardwareCorrupted': 0, 'DirectMap4k': 1748992, 'Mlocked': 0, 'Buffers': 141252, 'Active(file)': 422936}, 'd_time': 0.17880487442016602, 'server': u'54.201.95.77'}))
d = d.split('::')
print e
print d
for i in d:
	print base_x_to_base10(i, 32)

print base_x_to_base10('1DK', 32)
