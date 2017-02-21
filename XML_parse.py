#!/usr/bin/python
from xml.etree import ElementTree

with open('local.xml', 'rt') as f:
    tree = ElementTree.parse(f)

for node in tree.iter():
    print node.tag, node.attrib
