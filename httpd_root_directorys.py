import os
import sys

def website_configuration(webserver_config):
        config_files=[]
        for root, dirs, files in os.walk(webserver_config):
                for file in files:
                        if file.endswith(".conf"):
                                config_files.append(os.path.join(root, file))
                for print_config in config_files: print print_config

website_configuration("/etc/httpd/conf.d/")
