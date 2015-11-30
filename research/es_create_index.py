import elasticsearch
import datetime

node = 'Elasticsearch:80'
#node = '54.186.33.136:9200'

es = elasticsearch.Elasticsearch(node)

entry_mapping = {
    'entry-type': {
        'properties': {
            'id': {'type': 'string'},
            'created': {'type': 'date'},
            'title': {'type': 'string'},
            'tags': {'type': 'string', 'analyzer': 'keyword'},
            'content': {'type': 'string'}
            }
        }
    }

es.index(
    index='test-index',
    doc_type='test_type',
    id='test_id',
    body={
        'title': 'test_title',
        'content': 'This is the content',
        },
    op_type='create'
    )
