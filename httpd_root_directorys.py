import os
import sys
import re

import re

def http_includes():
	config_directory=[]
	include = re.compile("^\s*include")
	with open("/etc/httpd/conf/httpd.conf", "r") as search_file:
		for line in search_file:
	        	if include.match(line.lower()):
				config_directory.append(line)
		for i in config_directory: print i
			
def website_configuration(webserver_config, config_suffix):
        global config_files
        config_files=[]
        for root, dirs, files in os.walk(webserver_config):
                for file in files:
                        if file.endswith(config_suffix):
                                config_files.append(os.path.join(root, file))

def document_root(files_to_search):
        global DocRoots
        DocRoots=[]
        pattern = re.compile("^\s*documentroot")
        for i in files_to_search:
                with open(i, "r") as search_file:
                        for line in search_file:
                                if pattern.match(line.lower()):
                                        DocRoots.append(line)
                                        DocRoots = [x.replace(' ','') for x in DocRoots]
        for print_doc_root in DocRoots: print print_doc_root

website_configuration("/etc/httpd/conf.d/", ".conf")
document_root(config_files)
