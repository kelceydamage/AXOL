import elasticsearch
import datetime
import inspect

node = 'Elasticsearch:80'
#node = '54.186.33.136:9200'

es = elasticsearch.Elasticsearch(node)

def index():
	response = es.index(
		index='test',
		doc_type='blog_post',
		id=1,
		body={
			'title': 'es test entry',
			'content': 'blah blah blah',
			'date': datetime.date(2014, 4,  29)
			}
		)
	return response

def get():
	es.get(
		index='test',
		doc_type='blog_post',
		id=1
		)

def search():
	response = es.search(
		index='test',
		body={
			'query': {
				'match': {
					'doc_type': 'transaction'
					}
				}
			}
		)
	return response

def delete():
	response = es.delete(
		index='test',
		doc_type='blog_post',
		id='1',
		refresh=True
		)
	return response

#print inspect.getargspec(es.index)
print search()
