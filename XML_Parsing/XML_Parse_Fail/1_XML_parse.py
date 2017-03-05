import xml.etree.ElementTree as ET

tree = ET.fromstring("local.xml")
# tree = ET.parse('local.xml')
# tree = ET.parse('test.local.xml')
# root = tree.getroot()

#print ""
#print root.tag
#print root.attrib
#print "space"
#print ""

#for child in root:
#        print child.tag
#	print child.attrib
#        print ""


#print root.findall(".")
#print root.findall("./country/neighbor")

#for neighbor in root.iter(tree):
#        print neighbor.text
#        print ""
