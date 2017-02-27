
import os
import sys
import re
import copy


config_directories = ['/etc/httpd/conf.d/', '/etc/httpd/conf.modules.d/']
suffix ='.conf'


def website_configuration(webserver_config, config_suffix):
        global config_files
        config_files = []
	for i in webserver_config:
        	for root, dirs, files in os.walk(i):
               		for file in files:
                       		if file.endswith(config_suffix):
                               		config_files.append(os.path.join(root, file))


website_configuration(config_directories, suffix)
for x in config_files: print x
