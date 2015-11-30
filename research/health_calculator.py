#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#

def calculate_health_indicator(x, n, h, z):
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


normalized_indicator = 1.5217512
multiplier = 1
threshold_red = 100
scale = 100

c = calculate_health_indicator(
	normalized_indicator,
	multiplier,
	threshold_red,
	scale
	)

print c

'''
"memfree": 122112,
"memtotal": 15339624,
"memused": 15217512,

'''
m1 = 15339624
m2 = 2798424
m3 = m1 - m2
print m3
