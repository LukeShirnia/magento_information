import os
import sys
import re
import copy

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
                                CONFIG_DIR = line.split("/")[0]
				print CONFIG_DIR
                                config_directory.append(CONFIG_DIR)

get_http_includes()
