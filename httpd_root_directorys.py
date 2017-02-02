import os
import sys
import re

def website_configuration(webserver_config):
        global config_files
        config_files=[]
        for root, dirs, files in os.walk(webserver_config):
                for file in files:
                        if file.endswith(".conf"):
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

website_configuration("/etc/httpd/conf.d/")
document_root(config_files)
