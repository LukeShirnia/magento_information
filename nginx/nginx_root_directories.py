import os
import sys
import re
import copy

# This function finds the SERVERROOT for nginx and then any potential INCLUDES for server block locations
def get_nginx_includes():
        global config_directory_nginx, suffix_nginx
        config_directory_nginx = []
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
	config_directory_nginx = [ remove_nginx_suffix.replace(suffix_nginx, "") for remove_nginx_suffix in config_directory_nginx ] 
	suffix_nginx = suffix_nginx.replace('*', "")

def nginx_website_configuration(webserver_config, config_suffix):
        global config_files
        config_files = []
        for i in webserver_config:
                for root, dirs, files in os.walk(i):
                        for file in files:
                                if file.endswith(config_suffix):
					config_files.append(os.path.join(root, file))
					print config_files

get_nginx_includes()
nginx_website_configuration(config_directory_nginx, suffix_nginx)
