import xml.etree.ElementTree as ET
# https://docs.python.org/3/library/xml.etree.elementtree.html

tree = ET.parse('local.xml')
root = tree.getroot()

print root.tag
print root.attrib
print ""

for child in root:
        print child.tag, child.attrib
        print ""
for neighbor in root.iter('neighbor'):
        print neighbor.attrib
        print ""
