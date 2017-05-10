import os
import sys
import re
import copy

config_files = ['/etc/httpd/conf.d/test1.conf', '/etc/httpd/conf.d/welcome.conf', '/etc/httpd/conf.d/test2.conf', '/etc/httpd/conf.d/test3.conf']

def vhost_copy(i)
	copy_vhost = False
	with open(


# document roots
def document_root(files_to_search):
        global DocRoots
        DocRoots = []
	root_path = []
        pattern = re.compile("^\s*documentroot ")
        for i in files_to_search:
                with open(i, "r") as search_file:
                        for line in search_file:
                                if pattern.match(line.lower()):
					root_path = line.split(" ")[1]
					DocRoots.append(root_path)

document_root(config_files)
print DocRoots
