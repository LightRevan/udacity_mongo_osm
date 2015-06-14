# -*- coding: utf-8 -*-

from dbconnection import *

# defaultdict(<type 'set'>, {u'node': set([u'changeset', u'uid', u'timestamp', u'lon', u'version', u'user', u'lat', u'id']),
#                            u'tag': set([u'k', u'v']),
#                            u'nd': set([u'ref']),
#                            u'way': set([u'changeset', u'uid', u'timestamp', u'version', u'user', u'id'])})
# defaultdict(<type 'set'>, {u'node': set([u'tag']), u'way': set([u'tag', u'nd'])})

def pretty_print(doc, ensure_ascii=False):
    print json.dumps(doc, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=ensure_ascii)

if __name__ == '__main__':
    for doc in db.meta.aggregate([{'$match': {'element': 'way'}},
                                  {'$sort': {'tag.count': -1}},
                                  {'$project': {'_id': False,
                                                'element': True,
                                                'tagname': '$tag.name',
                                                'subtags': {'$size': {'$ifNull': ['$tag.subtags', []]}}}},
                                  {'$limit': 10}]):
        pretty_print(doc)

    for doc in db.meta.find({'element': 'way', 'tag.name': 'name'},
                            {'_id': False, 'file': False}).\
            sort('tag.count', pymongo.DESCENDING).limit(10):
        pretty_print(doc)
