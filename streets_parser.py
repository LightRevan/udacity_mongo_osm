# -*- coding: utf-8 -*-

import xml.sax as sax
import pymongo
from bson.dbref import DBRef
import itertools

from dbconnection import *

class OSMStreetHandler(sax.ContentHandler):
    interesting_tags = ['addr', 'cladr', 'name', 'building']

    def __init__(self, fname, collection):
        sax.ContentHandler.__init__(self)

        self.fname = fname
        self.collection = collection

        self.current_way = {}
        self.nodes = []
        self.tags = {}
        self.processed_num = 0

    def save_to_db(self):
        self.current_way['nodes'] = [DBRef('nodes_raw', id) for id in self.nodes]
        self.current_way['is_closed'] = len(self.nodes) != len(set(self.nodes))

        split_tags = [(k.split(':'), v) for k, v in self.tags.items()]
        group_func = lambda row: row[0][0]
        sort_func = lambda row: (row[0][0], len(row[0]))
        for group, rows in itertools.groupby(sorted(split_tags, key=sort_func), group_func):
            has_default = False
            for tag, v in rows:
                if len(tag) == 1:
                    has_default = True
                    self.current_way[group] = v
                else:
                    attr_name = ':'.join(tag[1:])
                    if len(tag) > 2:
                        group_name = group + '_long'
                    elif has_default:
                        group_name = group + '_additional'
                    else:
                        group_name = group

                    ins_group = self.current_way.get(group_name, {})
                    ins_group[attr_name] = v
                    self.current_way[group_name] = ins_group

        res = self.collection.insert_one(self.current_way)
        assert res.inserted_id == self.current_way['_id'], self.current_way['_id']
        self.processed_num += 1
        self.clear_way()

        if self.processed_num == 1 or self.processed_num % 1000 == 0:
            print self.processed_num

    def clear_way(self):
        self.current_way = {}
        self.nodes = []
        self.tags = {}

    def startElement(self, name, attrs):
        if name == 'way':
            self.current_way = {'_id': attrs.getValue('id'),
                                'file': self.fname,
                                'created': {'user': attrs.getValue('user'),
                                            'id': attrs.getValue('uid'),
                                            'version': attrs.getValue('version'),
                                            'timestamp': attrs.getValue('timestamp'),
                                            'changeset': attrs.getValue('changeset')}}

        if self.current_way and name == 'nd':
            self.nodes.append(attrs.getValue('ref'))

        if self.current_way and name == 'tag':
            key = attrs.getValue('k')
            if key.split(':')[0] in self.interesting_tags:
                self.tags[key] = attrs.getValue('v')

    def endElement(self, name):
        if name == 'way':
            self.save_to_db()


if __name__ == '__main__':
    fname = 'data/moscow_russia.osm'

    db.streets_raw.delete_many({'file': fname})

    with open(fname, 'r') as f:
        handler = OSMStreetHandler(fname, db.streets_raw)
        sax.parse(f, handler)