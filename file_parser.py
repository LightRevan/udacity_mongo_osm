# -*- coding: utf-8 -*-

import xml.sax as sax
import collections


class OSMHandler(sax.ContentHandler):
    def __init__(self):
        sax.ContentHandler.__init__(self)
        self.attribute_dict = collections.defaultdict(set)
        self.subelements = collections.defaultdict(set)
        self.open_elements = []

        self.interesting_elements = ['node', 'way', 'tag', 'nd']

    def startElement(self, name, attrs):
        if name not in self.interesting_elements:
            return

        for attr in attrs.getNames():
            self.attribute_dict[name].add(attr)

        self.open_elements.append(name)
        if len(self.open_elements) > 1:
            self.subelements[self.open_elements[-2]].add(name)

    def endElement(self, name):
        if name in self.interesting_elements:
            self.open_elements.pop()

if __name__ == '__main__':
    fname = 'data/moscow_russia.osm'

    tags = set()
    with open(fname, 'r') as f:
        handler = OSMHandler()
        sax.parse(f, handler)

    print handler.attribute_dict
    print handler.subelements