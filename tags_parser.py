# -*- coding: utf-8 -*-

import xml.sax as sax
import collections

from dbconnection import *


class OSMTagHandler(sax.ContentHandler):
    def __init__(self, fname, db):
        sax.ContentHandler.__init__(self)

        self.fname = fname
        self.db = db

        self.attribute_dict = collections.defaultdict(set)
        self.subelements = collections.defaultdict(set)
        self.open_elements = []

        self.interesting_elements = ['node', 'way', 'tag', 'nd']

    def save_to_db(self, elem, k, v):
        parts = k.split(':')
        query = {'file': self.fname, 'element': elem, 'tag.name': parts[0]}
        doc = self.db.find_one(query)
        is_changed = False
        if not doc:
            doc = {'file': self.fname, 'element': elem, 'tag': {'name': parts[0], 'count': 0, 'examples': [v]}}

        cur_tag = doc['tag']
        cur_tag['count'] += 1
        for tag_part in parts[1:]:
            subtags = cur_tag.get('subtags', None)
            if subtags is None:
                subtags = []
                cur_tag['subtags'] = subtags

            for tag in subtags:
                if tag['name'] == tag_part:
                    cur_tag = tag
                    cur_tag['count'] += 1
                    break
            else:
                cur_tag = {'name': tag_part, 'count': 1, 'examples': []}
                subtags.append(cur_tag)

        examples = cur_tag['examples']
        if len(examples) < 11 and v not in examples:
            examples.append(v)

        res = self.db.replace_one(query, doc, upsert=True)

    def startElement(self, name, attrs):
        if name not in self.interesting_elements:
            return

        for attr in attrs.getNames():
            self.attribute_dict[name].add(attr)

        self.open_elements.append(name)
        if len(self.open_elements) > 1:
            self.subelements[self.open_elements[-2]].add(name)

        if len(self.open_elements) > 1 and name == 'tag':
            self.save_to_db(self.open_elements[-2], attrs.getValue('k'), attrs.getValue('v'))

    def endElement(self, name):
        if name in self.interesting_elements:
            self.open_elements.pop()

if __name__ == '__main__':
    fname = 'data/moscow_russia.osm'

    db.meta.delete_many({'file': fname})

    tags = set()
    with open(fname, 'r') as f:
        handler = OSMTagHandler(fname, db.meta)
        sax.parse(f, handler)

    # defaultdict(<type 'set'>, {u'node': set([u'changeset', u'uid', u'timestamp', u'lon', u'version', u'user', u'lat', u'id']),
    #                            u'tag': set([u'k', u'v']),
    #                            u'nd': set([u'ref']),
    #                            u'way': set([u'changeset', u'uid', u'timestamp', u'version', u'user', u'id'])})
    # defaultdict(<type 'set'>, {u'node': set([u'tag']), u'way': set([u'tag', u'nd'])})

    print handler.attribute_dict
    print handler.subelements
    print db.meta.count()