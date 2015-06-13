# -*- coding: utf-8 -*-

import pymongo

client = pymongo.MongoClient()
db = client.osm
# db.drop_collection('meta')
# db.meta.create_index('file')
# db.meta.create_index('element')
# db.meta.create_index('tag.name')
# db.meta.create_index('tag.count')

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