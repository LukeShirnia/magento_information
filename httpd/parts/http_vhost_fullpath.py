import os
import sys
import re
import copy

server_root = ['/etc/httpd']
config_directory = ['vhost.d', 'conf.modules.d', 'conf.d']

def http_vhost_directory_fullpath(file_root, docs_directory):
        global vhost_directory_path
        PATH = []
        vhost_directory_path = []

        for i in docs_directory:
                # since file_root can be an array, use copy to grab a copy
                # of the array
                args = copy.copy(file_root)
                args.append(i)
                # and stick `i` on the end of that array so
                # that we have our full param list for os.path.join
                PATH = os.path.join(*args)
		vhost_directory_path.append(PATH)


http_vhost_directory_fullpath(server_root, config_directory)

for x in vhost_directory_path:
	print x
	print ""
