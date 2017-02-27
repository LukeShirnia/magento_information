import os
import sys
import re
import copy
import fnmatch



# document_root = ['/var/wwwwww/','/var/www/vhost/test1','/var/www/vhost/test2']
document_root = '/var/wwwwww/'
# xml_file_location = ['app/etc/']
xml_file_location = ['app/etc/']


def find_xml_file(document_root, xml_file_location):
	global xml_full_path
	xml_path = []
	local_xml = re.compile("local.xml")
	xml_full_path = []
	for root in document_root:
		for path in xml_file_location:
			print os.path.join(root, path)
#			xml_path.append(os.path.join(root, path))
#	for i in document_root:
#		for path, dirs, files in os.walk(document_root):
#			if local_xml in files:
#				xml_full_path.append(os.path.join(root, local_xml))
		

find_xml_file(document_root, xml_file_location)
print xml_path
#print xml_full_path
