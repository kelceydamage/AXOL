#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013
#+

import math
from math import *
import numpy

def x(n):
	return n * 2

l = {
	'a': 2,
	'b': 4,
	'c': 8,
	'd': 16
	}

t = [2, 4, 8, 16]

n = 1

y = [x(l[n]) for n in l if l[n] in t]

#y = [x(l[n]) for n in l if f(l[n]) == True]


def f(x, c):
	n = 1
	return (n / math.pow(x, 0.5))

def calc(func, x):
	x = float(x)
	c = float(1)
	y = float(100)
	y = y / c
	z = x / c
	print 100 - z
	d = func(x, c) * 1
	#print d
	print d

n = 1
x = float(0.9)

x = (x / n) * 100
#g =  math.log10(1.5670605)
#0.1950857
'''
c1 = 80
c2 = 0.1950857
c3 = 90
'''


'''
y = a / b
a = b * y
b = a / y
'''

def calculate_zero(h, k):
	a = (pow(h, 2) - h + k) / pow(h, 3)

	return a

def calculate_envelope(h, a, k):
	b = (k - ((a * pow(h, 3)) - (0.01 * (a * pow(h, 2))))) / h

	return b

def normalize_x(x, n):
	return (float(x) / float(n)) * 100

k = 100000
n = 1
h = 80
b = 1 #21.2
c = 1 #550

a = calculate_zero(h, k)
b = calculate_envelope(h, a, k)

t1 = float(3)
t2 = float(0.8)
z = 1
c = 50

matrix = []
print z
for x in numpy.arange(0.01, 1.01, 0.01):
	x = normalize_x(float(x), n)
	y = 100 - ((a * pow(x, 3)) - (0.01 * a * pow(x, 2)) + (b * x)) / 1000 + c
	if y > 100:
		y = 100
	matrix.append((round(y, 2), int(x)))

print matrix

api_list = [100, 100, 100, 89]

mean = sum(value for value in api_list)/len(api_list)
print mean
x = sum(pow((value-mean), 2) for value in api_list)/len(api_list)

print x
print sqrt(x)


'''
{
'com_prepare_sql': 0,
'tc_log_max_pages_used': 0,
'handler_read_last': 774,
'flush_commands': 1,
'com_stmt_prepare': 214016,
'innodb_buffer_pool_wait_free': 0,
'com_create_index': 0,
'select_scan': 423641,
'innodb_data_fsyncs': 1522,
'com_resignal': 0,
'questions': 31945429,
'com_show_table_status': 0,
'com_reset': 0,
'bytes_received': 4443028782,
'innodb_page_size': 16384,
'com_call_procedure': 0,
'performance_schema_thread_instances_lost': 0,
'com_set_option': 321,
'com_assign_to_keycache': 0,
'efficiency_key_read_miss_rate': 2634,
'performance_schema_cond_classes_lost': 0,
'com_ha_read': 0,
'com_do': 0,
'com_show_create_table': 0,
'select_range_check': 0,
'ssl_accept_renegotiates': 0,
'innodb_data_pending_reads': 0,
'com_show_variables': 9,
'com_preload_keys': 0,
'network_time': 0.1465919017791748,
'com_alter_procedure': 0,
'innodb_log_write_requests': 7295,
'com_drop_trigger': 0,
'handler_read_key': 17573755,
'innodb_buffer_pool_pages_free': 7625,
'innodb_row_lock_time': 0,
'start_time': 1412018370.209193,
'performance_schema_rwlock_classes_lost': 0,
'com_show_grants': 0,
'ssl_session_cache_overflows': 0,
'com_insert_select': 0,
'com_show_profile': 0,
'innodb_data_pending_writes': 0,
'created_tmp_files': 119,
'innodb_data_read': 8933376,
'innodb_buffer_pool_read_ahead_rnd': 0,
'open_files': 202,
'com_stmt_reprepare': 0,
'ssl_cipher': u'',
'com_drop_table': 96,
'com_show_engine_status': 0,
'innodb_buffer_pool_read_requests': 149272,
'com_help': 0,
'name': u'live_hq_db_master',
'handler_savepoint': 0,
'created_tmp_tables': 15961,
'ssl_accepts': 0,
'opened_table_definitions': 307,
'com_change_master': 0,
'handler_read_rnd_next': 48603595722,
'innodb_buffer_pool_pages_total': 8191,
'slave_retried_transactions': 0,
'innodb_data_writes': 2614,
'com_repair': 0,
'com_savepoint': 0,
'com_show_relaylog_events': 0,
'innodb_buffer_pool_bytes_data': 9158656,
'queries': 32373753,
'com_show_function_status': 0,
'com_show_charsets': 0,
'opened_files': 8727,
'key_write_requests': 6549656,
'innodb_os_log_pending_fsyncs': 0,
'handler_update': 2023405,
'key_writes': 376458,
'com_show_create_func': 0,
'threads_connected': 5,
'ssl_verify_depth': 0,
'innodb_truncated_status_writes': 0,
'connections': 440041,
'com_drop_user': 9,
'error_count': 0,
'com_create_db': 4,
'qcache_free_blocks': 2818,
'ssl_callback_cache_hits': 0,
'innodb_row_lock_time_max': 0,
'handler_commit': 564152,
'com_xa_commit': 0,
'efficiency_qcache_hit_rate': 94.89,
'com_show_processlist': 0,
'slave_open_temp_tables': 0,
'com_drop_index': 0,
'key_blocks_used': 40118,
'innodb_row_lock_time_avg': 0,
'com_xa_rollback': 0,
'com_stmt_close': 214016,
'innodb_log_waits': 0,
'com_show_privileges': 0,
'com_delete': 3740,
'innodb_buffer_pool_pages_data': 559,
'com_revoke_all': 0,
'innodb_have_atomic_builtins': u'ON',
'com_truncate': 0,
'com_show_open_tables': 0,
'innodb_data_reads': 422,
'com_show_fields': 146,
'performance_schema_thread_classes_lost': 0,
'com_create_function': 0,
'innodb_os_log_fsyncs': 1460,
'com_rename_user': 0,
'tc_log_page_size': 0,
'handler_discover': 0,
'innodb_pages_created': 148,
'threads_created': 61,
'threads_cached': 56,
'com_binlog': 0,
'innodb_rows_inserted': 7178,
'ssl_sessions_reused': 0,
'efficiency_key_write_miss_rate': 17.4,
'com_begin': 399388,
'com_lock_tables': 95,
'com_show_authors': 0,
'com_grant': 0,
'innodb_log_writes': 1450,
'uptime_since_flush_status': 328447,
'com_drop_server': 0,
'ssl_session_cache_hits': 0,
'threads_running': 4,
'com_ha_close': 0,
'innodb_rows_read': 9752,
'com_show_create_event': 0,
'com_execute_sql': 0,
'open_table_definitions': 93,
'sort_scan': 3335,
'ssl_used_session_cache_entries': 0,
'qcache_total_blocks': 12468,
'com_create_view': 0,
'bytes_sent': 11840237600,
'innodb_rows_updated': 255,
'com_show_warnings': 0,
'efficiency_key_write': Decimal('5.747752248'),
'com_kill': 0,
'efficiency_qcache_prune_rate': 0.0,
'threshold_time': 0.0019001960754394531,
'sort_merge_passes': 45,
'select_full_range_join': 0,
'slow_queries': 0,
'com_alter_db_upgrade': 0,
'com_xa_prepare': 0,
'com_signal': 0,
'binlog_cache_disk_use': 3,
'performance_schema_rwlock_instances_lost': 0,
'com_create_server': 0,
'com_revoke': 0,
'com_show_collations': 0,
'processing_time': 0.0027039051055908203,
'table_locks_immediate': 2318689,
'com_optimize': 0,
'com_admin_commands': 9,
'performance_schema_table_handles_lost': 0,
'com_alter_tablespace': 0,
'tc_log_page_waits': 0,
'handler_prepare': 1440,
'com_show_events': 0,
'com_analyze': 0,
'com_commit': 399267,
'qcache_queries_in_cache': 4781,
'ssl_session_cache_size': 0,
'innodb_buffer_pool_pages_misc': 7,
'com_stmt_execute': 214016,
'performance_schema_cond_instances_lost': 0,
'com_show_binlogs': 0,
'handler_delete': 3750,
'compression': u'OFF',
'open_tables': 139,
'select_range': 30998,
'com_alter_db': 0,
'sort_rows': 4191670,
'ssl_connect_renegotiates': 0,
'com_alter_server': 0,
'com_show_triggers': 0,
'performance_schema_file_handles_lost': 0,
'not_flushed_delayed_rows': 0,
'table_locks_waited': 21783,
'slave_running': u'OFF',
'com_drop_view': 0,
'innodb_buffer_pool_reads': 412,
'com_show_slave_hosts': 0,
'com_select': 1549876,
'key_blocks_unused': 1207888,
'com_purge_before_date': 0,
'handler_read_next': 100441719,
'com_stmt_send_long_data': 0,
'com_show_storage_engines': 0,
'efficiency_qcache_fragmentation_ratio': 32,
'com_show_status': 12242,
'innodb_buffer_pool_pages_flushed': 1116,
'max_used_connections': 61,
'com_create_udf': 0,
'com_show_contributors': 0,
'opened_tables': 353,
'handler_rollback': 77,
'com_xa_recover': 0,
'qcache_hits': 28805314,
'efficiency_qcache_insert_rate': 5.06,
'innodb_buffer_pool_read_ahead_evicted': 0,
'com_check': 0,
'ssl_cipher_list': u'',
'com_show_procedure_status': 0,
'ssl_verify_mode': 0,
'com_show_binlog_events': 0,
'performance_schema_table_instances_lost': 0,
'innodb_os_log_pending_writes': 0,
'com_insert': 55052,
'performance_schema_locker_lost': 0,
'com_stmt_fetch': 0,
'slave_heartbeat_period': u'1800.000',
'performance_schema_mutex_instances_lost': 0,
'com_xa_start': 0,
'delayed_writes': 0,
'com_dealloc_sql': 0,
'ssl_default_timeout': 0,
'qcache_free_memory': 93161408,
'innodb_rows_deleted': 229,
'com_create_trigger': 0,
'binlog_stmt_cache_disk_use': 504,
'key_read_requests': 92445628,
'efficiency_key_read': Decimal('0.0003795095643'),
'delayed_errors': 0,
'innodb_row_lock_current_waits': 0,
'innodb_buffer_pool_write_requests': 59616,
'com_install_plugin': 0,
'performance_schema_file_instances_lost': 0,
'select_full_join': 1202,
'ssl_session_cache_misses': 0,
'created_tmp_disk_tables': 299,
'aborted_clients': 13,
'com_show_databases': 3,
'qcache_inserts': 1536012,
'slave_received_heartbeats': 0,
'handler_savepoint_rollback': 0,
'innodb_pages_read': 411,
'com_release_savepoint': 0,
'performance_schema_mutex_classes_lost': 0,
'com_show_tables': 4,
'com_purge': 0,
'innodb_dblwr_pages_written': 1116,
'prepared_stmt_count': 0,
'com_create_table': 98,
'innodb_buffer_pool_pages_dirty': 0,
'com_empty_query': 0,
'host': u'54.68.64.40',
'innodb_os_log_written': 4197376,
'sort_range': 5159,
'ssl_client_connects': 0,
'com_show_create_proc': 0,
'com_rollback_to_savepoint': 0,
'delayed_insert_threads': 0,
'com_slave_start': 0,
'qcache_not_cached': 13864,
'slow_launch_threads': 0,
'source': 'mysql',
'ssl_finished_accepts': 0,
'com_xa_end': 0,
'handler_read_prev': 167070904,
'innodb_data_written': 40771584,
'handler_write': 10968511,
'handler_read_rnd': 5477261,
'com_uninstall_plugin': 0,
'com_alter_event': 0,
'com_show_master_status': 10,
'rpl_status': u'AUTH_MASTER',
'com_slave_stop': 1,
'handler_read_first': 580,
'com_unlock_tables': 95,
'com_create_user': 0,
'com_ha_open': 0,
'com_rollback': 121,
'com_create_procedure': 0,
'innodb_row_lock_waits': 0,
'com_flush': 0,
'com_update_multi': 0,
'com_show_create_trigger': 0,
'binlog_stmt_cache_use': 337652,
'warnings': {
	'status': 0, u'live_hq_db_master': {
		'error': 'no errors found'
		}
	},
'com_show_plugins': 0,
'innodb_buffer_pool_bytes_dirty': 0,
'ssl_ctx_verify_depth': 0,
'uptime': 328447,
'qcache_lowmem_prunes': 0,
'innodb_buffer_pool_read_ahead': 0,
'innodb_dblwr_writes': 31,
'com_alter_function': 0,
'ssl_ctx_verify_mode': 0,
'com_show_errors': 0,
'com_stmt_reset': 0,
'com_drop_procedure': 0,
'innodb_data_pending_fsyncs': 0,
'com_checksum': 0,
'com_show_engine_logs': 0,
'com_load': 0,
'aborted_connects': 9,
'binlog_cache_use': 737,
'com_drop_event': 0,
'com_show_create_db': 0,
'last_query_cost': u'0.000000',
'com_show_keys': 0,
'com_update': 279597,
'com_create_event': 0,
'com_rename_table': 0,
'com_delete_multi': 0,
'ssl_finished_connects': 0,
'com_show_profiles': 0,
'ssl_version': u'',
'key_blocks_not_flushed': 0,
'ssl_session_cache_timeouts': 0,
'com_alter_table': 190,
'com_drop_db': 1,
'ssl_session_cache_mode': u'NONE',
'key_reads': 35084,
'com_change_db': 6,
'innodb_pages_written': 1116,
'performance_schema_file_classes_lost': 0,
'open_streams': 0,
'com_show_engine_mutex': 0,
'com_show_slave_status': 1,
'com_drop_function': 0,
'com_replace': 0,
'com_replace_select': 0
}
'''
