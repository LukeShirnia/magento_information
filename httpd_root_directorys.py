import os
import sys
import re
import copy

def http_includes():
        global server_root, config_directory
        config_directory=[]
        server_root=[]
        SUFFIX=".conf"
        CONFIG_DIR=[]
        PATH=[]
        include = re.compile("^\s*include")
        serverroot = re.compile("^\s*serverroot")

        with open("/etc/httpd/conf/httpd.conf", "r") as search_file:
                for line in search_file:
                        if include.match(line.lower()):
                                line = line.split(" ")[1]
#                               suffix_match = line.split("*")[1]
                                #SUFFIX = [x.replace('*','') for x in SUFFIX]
                                CONFIG_DIR = line.split("/")[0]
                                config_directory.append(CONFIG_DIR)
#                               SUFFIX.append(suffix_match)
                        if serverroot.match(line.lower()):
                                line = line.split('"')[1]
                                server_root.append(line)
                                server_root = [x.replace("ServerRoot", "") for x in server_root]

def http_vhost_directory_fullpath(file_root, docs_directory):
	global vhost_directory_path
 	PATH = []
	vhost_direcory_path=[]

	for i in docs_directory:
        	# since file_root can be an array, use copy to grab a copy 
        	# of the array
        	args = copy.copy(file_root)
        	args.append(i)
        	# and stick `i` on the end of that array so
        	# that we have our full param list for os.path.join
        	PATH = os.path.join(*args)
        	vhost_directory_path.append(PATH)
		
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
http_vhost_directory_fullpath(server_root, config_directory)
print vhost_directory_path[0]
