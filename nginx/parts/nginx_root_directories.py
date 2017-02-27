import os
import sys
import re
import copy

# This function finds the SERVERROOT for nginx and then any potential INCLUDES for server block locations
def get_nginx_includes():
        global config_directory_nginx, SUFFIX_NGINX
        config_directory_nginx = []
        SUFFIX_NGINX = ".conf"
        CONFIG_DIR_NGINX = []
        PATH_NGINX = []
        include = re.compile("^\s*include")

        with open("/etc/nginx/nginx.conf", "r") as search_file:
                for line in search_file:
                        if include.match(line.lower()):
 				line = line.strip()
                                line = line.split(" ")[1]
                                CONFIG_DIR_NGINX = line
                                config_directory_nginx.append(CONFIG_DIR_NGINX)
				config_directory_nginx = filter(None, config_directory_nginx)
				print config_directory_nginx

get_nginx_includes()
