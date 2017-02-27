import os
import sys
import re
import copy


nginx_config_files = '/etc/nginx/conf.d/website2.conf, /etc/nginx/conf.d/website1.conf, /etc/nginx/conf.d/random.conf'

def document_root(files_to_search):
        global NginxDocRoots
        NginxDocRoots = []
        nginx_root_path = []
        pattern = re.compile("^\s*root")
        for i in files_to_search:
                with open(i, "r") as search_file:
                        for line in search_file:
                                if pattern.match(line.lower()):
                                        nginx_root_path = line.split(" ")[1]
                                        NginxDocRoots.append(nginx_root_path)
                                        NginxDocRoots = [x.rstrip() for x in NginxDocRoots] # strips all whitespace after each docroot
					NginxDocRoots = filter(None, NginxDocRoots) # remove empty string from array

document_root(nginx_config_files)
print NginxDocRoots
