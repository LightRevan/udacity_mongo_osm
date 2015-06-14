# -*- coding: utf-8 -*-

import pymongo
import json

client = pymongo.MongoClient()
db = client.osm

# db.streets_raw.create_index('file')
# db.nodes_raw.create_index('file')
#
# db.meta.create_index('file')
# db.meta.create_index('element')
# db.meta.create_index('tag.name')
# db.meta.create_index('tag.count')

