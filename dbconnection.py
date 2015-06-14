# -*- coding: utf-8 -*-

import pymongo
import json

client = pymongo.MongoClient()
db = client.osm

db.streets_raw.create_index('file')
db.nodes_raw.create_index('file')

db.meta.create_index('file')
db.meta.create_index('element')
db.meta.create_index('tag.name')
db.meta.create_index('tag.count')

# test = client.test.test
# client.drop_database('test')

# test.delete_many({})

# test.insert_one({'ar': [{'f':1}, {'f': 2}]})
# test.insert_one({'ar': [{'f':3}]})
# test.insert_one({'ar': [{'f':3}, {'f':2}]})
#
# for o in test.find({'ar.f': 2}):
#     print o

# test.update_one({'f.name': 1, 'f.f.name': 1}, {'$addToSet': {'f.f.f': {'name': 1}}}, upsert=True)
# test.update_one({'f.name': 1, 'f.f.name': 2}, {'$addToSet': {'f.f.f': {'name': 1}}}, upsert=True)
#
# for o in test.find():
#     print o


# for doc in db.meta.aggregate([{'$match': {'element': 'way'}},
#                               {'$sort': {'tag.count': -1}},
#                               {'$project': {'_id': False,
#                                             'element': True,
#                                             'tagname': '$tag.name',
#                                             'subtags': {'$size': {'$ifNull': ['$tag.subtags', []]}}}},
#                               {'$limit': 10}]):
#     print json.dumps(doc, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False)


# for doc in db.meta.find({'element': 'way', 'tag.name': 'name'},
#                         {'_id': False, 'file': False}).\
#         sort('tag.count', pymongo.DESCENDING).limit(10):
#     print json.dumps(doc, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=True)
