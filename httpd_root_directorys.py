import os
import sys
import re
import copy


def print_header():
        print "-" * 60
        print ""
        print " _____ _____ _____ _____ _____ _____ _____"
        print "|     |  _  |  ___|   __|   | |_   _|     |"
        print "| | | |     | |_| |   __| | | | | | |  |  |"
        print "|_|_|_|__|__|_____|_____|_|___| |_| |_____|"
        print ""
        print "-" * 60
        print ""


# This function finds the SERVERROOT for apache and then any potential INCLUDES for vhost locations
def get_http_includes():
        global server_root, config_directory, SUFFIX
        config_directory = []
        server_root = []
        SUFFIX = ".conf"
        CONFIG_DIR = []
        PATH = []
        include = re.compile("^\s*include")
        serverroot = re.compile("^\s*serverroot")

        with open("/etc/httpd/conf/httpd.conf", "r") as search_file:
                for line in search_file:
                        if include.match(line.lower()):
                                line = line.split(" ")[1]
#                               suffix_match = line.split("*")[1]
                                # SUFFIX = [x.replace('*','') for x in SUFFIX]
                                CONFIG_DIR = line.split("/")[0]
                                config_directory.append(CONFIG_DIR)
#                               SUFFIX.append(suffix_match)
                        if serverroot.match(line.lower()):
                                line = line.split('"')[1]
                                server_root.append(line)
                                server_root = [x.replace("ServerRoot", "") for x in server_root]

# os.path.join - joins SERVERROOT and INCLUDES directory for vhost_directory_path
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

# Finds all VHOSTS in vhost_directory_path ending with SUFFIX defined in INCLUDE (get_http_includes)
def website_configuration(webserver_config, config_suffix):
        global config_files
        config_files = []
        for i in webserver_config:
                for root, dirs, files in os.walk(i):
                        for file in files:
                                if file.endswith(config_suffix):
                                        config_files.append(os.path.join(root, file))

# Using the vhost files found in website_configuration, obtains DOCUMENTROOT directories
def document_root(files_to_search):
        global DocRoots
        DocRoots = []
        root_path = []
        pattern = re.compile("^\s*documentroot")
        for i in files_to_search:
                with open(i, "r") as search_file:
                        for line in search_file:
                                if pattern.match(line.lower()):
                                        line = line.strip()
                                        root_path = line.split(" ")[1]
                                        DocRoots.append(root_path)
                                        DocRoots = [x.rstrip() for x in DocRoots] # strips all whitespace after each docroot
                                        DocRoots = filter(None, DocRoots) # remove empty string from array


# Locating LOCAL.XML file using DocRoots and os.path.join
def find_xml_file(document_root):
        global xml_full_path, magento_file
        app_etc = 'app/etc/'
        xml_full_path = []
        convert_path = []
        magento_file = []
        #local_xml = re.compile("^local.xml$") ---> doesnt work with os.path.join
        local_xml = "local.xml"
        for root in document_root:
                        xml_full_path.append(os.path.join(root, app_etc))
        for x in xml_full_path:
                for root, dirs, files in os.walk(x):
                        if local_xml in files:
                                magento_file.append(os.path.join(root, local_xml))


get_http_includes()
http_vhost_directory_fullpath(server_root, config_directory)
website_configuration(vhost_directory_path, SUFFIX)
document_root(config_files)
find_xml_file(DocRoots)

print ""
print ""
print_header()
for w in magento_file: print w
print ""
print ""
