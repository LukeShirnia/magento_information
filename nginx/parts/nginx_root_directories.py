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
				# remove all empty array entries
				config_directory_nginx = filter(None, config_directory_nginx)
				# remove ; from directory path
				config_directory_nginx = [x.replace(';', "") for x in config_directory_nginx]
	# find the suffix for each directory and then remove it from the array of includes	
	suffix_nginx = config_directory_nginx[1]

	# probably need to loop the suffix through all includes instead of manually selecting the first array entry
	suffix_nginx = suffix_nginx.split('/')[-1]
	suffix_nginx = suffix_nginx.replace('*', "")
	config_directory_nginx = [ remove_nginx_suffix.replace(suffix_nginx, "") for remove_nginx_suffix in config_directory_nginx ] 
	print config_directory_nginx
	print suffix_nginx

get_nginx_includes()
