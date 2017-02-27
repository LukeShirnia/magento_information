import os
import sys
import re
import copy

config_directory_nginx = '/usr/share/nginx/modules/', '/etc/nginx/conf.d/', '/etc/nginx/default.d/'
suffix_nginx = '.conf'

def nginx_website_configuration(webserver_config, config_suffix):
        global config_files
        config_files = []
        for i in webserver_config:
                for root, dirs, files in os.walk(i):
                        for file in files:
                                if file.endswith(config_suffix):
					config_files.append(os.path.join(root, file))
					print config_files

nginx_website_configuration(config_directory_nginx, suffix_nginx)
