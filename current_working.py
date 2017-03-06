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
        # local_xml = re.compile("^local.xml$") ---> doesnt work with os.path.join
        local_xml_to_find = "local.xml"
        for root in document_root:
                        xml_full_path.append(os.path.join(root, app_etc))
        for x in xml_full_path:
                for root, dirs, files in os.walk(x):
                        if local_xml_to_find in files:
                                magento_file.append(os.path.join(root, local_xml_to_find))

def replace_CDATA(xml_variable):
	xml_variable = xml_variable.replace("<![CDATA[", "")
	xml_variable = xml_variable.replace("]]>","")
	return xml_variable

def replace_session_CDATA(session_variable):
        session_variable = session_variable.replace("<![CDATA[", "")
        session_variable = session_variable.replace("]]>","")
        session_variable = session_variable.replace("<session_save>", "")
        session_variable = session_variable.replace("</session_save>", "")
        return session_variable

# open file and search for all lines between open and closing of adminhtml tags
def admin_url():
        with open(local_xml) as infile:
                record = False
                for line in infile:
                        if line.strip() == "<adminhtml>":
                                record = True
                        elif line.strip() == "</adminhtml>":
                                record = False
                        elif record:
				admin_information(line)

# find the admin url present between the frontName tag
def admin_information(line):
	admin = re.search("<frontName>(.*)</frontName>",line)
	if admin:
		print "-" * 50
		admin = str(admin.group(1))
		admin = replace_CDATA(admin)
		print "Admin URL:", admin
        	print "-" * 50
		print ""

def db_connection():
	print "-" * 50
	print "DATABASE INFORMATION"
	print "-" * 50
	with open(local_xml) as infile:
		record = False
		for line in infile:
			if line.strip() == "<connection>":
				record = True
			elif line.strip() == "</connection>":
				record = False
			elif record:
				db_information(line)
def db_information(line):
	find_db_host = re.search("<host>(.*)</host>", line)
	find_db_username = re.search("<username>(.*)</username>", line)
        find_db_password = re.search("<password>(.*)</password>", line)
        find_db_dbname = re.search("<dbname>(.*)</dbname>", line)
        if find_db_host:
        	find_db_host = find_db_host.group(1)
                find_db_host = replace_CDATA(find_db_host)
                print "Host      :", find_db_host
       	if find_db_username:
                find_db_username = str(find_db_username.group(1))
                find_db_username = replace_CDATA(find_db_username)
                print "Username  :", find_db_username
        if find_db_password:
                find_db_password = str(find_db_password.group(1))
                find_db_password = replace_CDATA(find_db_password)
                print "Password  :", find_db_password
        if find_db_dbname:
                find_db_dbname = str(find_db_dbname.group(1))
                find_db_dbname = replace_CDATA(find_db_dbname)
                print "Database  :", find_db_dbname

def session_save():
	print "-" * 50
	print "SESSION INFORMATION"
	print "-" * 50
        with open(local_xml) as infile:
                for line in infile:
			line = replace_session_CDATA(line)
			if line.strip() == "db":
				session_db_information()
			elif line.strip() == "memcache":
				session_db_memecache()
			elif line.strip() == "files":
				print "Sessions    : Files"
def session_db_memecache():
	service = "Memcache"
	with open(local_xml) as infile:
		for line in infile:
			session_save_path = re.search("<session_save_path>(.*)</session_save_path>" , line)
			if session_save_path:
				session_save_path = str(session_save_path.group(1))
				session_save_path = replace_CDATA(session_save_path)
				print "Service   :", service
				print "Save Path :", session_save_path
	
def session_db_information():
	global session_service_name
        with open(local_xml) as infile:
                record = False
	        for line in infile:
			if line.strip() == "<redis_session>":
				record = True
				session_service_name = "Redis"
			elif line.strip() == "<memcache_session>":
				record = True
				session_service_name = "Memcache"
			elif line.strip() == "<backend>Cm_Cache_Backend_Redis</backend>":
				record = True
				session_service_name = "redis"
                        elif line.strip() == "</cache>":
                                record = False
                        elif record:
                                session_information(line)

def session_information(line):
        find_session_host = re.search("<host>(.*)</host>", line)
        find_session_port = re.search("<port>(.*)</port>", line)
        find_session_password = re.search("<password>(.*)</password>", line)
        find_databases_number = re.search("<database>(.*)</database>", line)
	if find_session_host:
		find_session_host = str(find_session_host.group(1))
		find_session_host = replace_CDATA(find_session_host)
		print "Service   :", session_service_name
		print "Host      :", find_session_host
	if find_session_port:
		find_session_port = str(find_session_port.group(1))
		find_session_port = replace_CDATA(find_session_port)
		print "Port      :", find_session_port
	if find_session_password:
		find_session_password = str(find_session_password.group(1))
		find_session_password = replace_CDATA(find_session_password)
		print "Password  :", find_session_password
	if find_databases_number:
		find_databases_number = str(find_databases_number.group(1))
		find_databases_number = replace_CDATA(find_databases_number)
		print "Database #:", find_databases_number

def full_page_cache():
        with open(local_xml) as infile:
	        record = False
                for line in infile:
                        if line.strip() == "<full_page_cache>":
                                record = True
			elif line.strip() == "<backend>Cm_Cache_Backend_Redis</backend>":
				record = True
                        # elif line.strip() == "</full_page_cache>":
                        elif line.strip() == "</backend_options>":
                                record = False
                        elif record:
                                full_page_information(line)

def full_page_information(line):
	find_full_page_service = re.search("<backend>Mage_Cache_Backend_(.*)</backend>", line)
	find_full_page_service_legacy = re.search("<backend>Cm_Cache_Backend_(.*)</backend>", line)
	find_full_page_server = re.search("<server>(.*)</server>", line)
	find_full_page_port = re.search("<port>(.*)</port>", line)
	find_full_page_db_number = re.search("<database>(.*)</database>", line)
	find_full_page_password = re.search("<password>(.*)</password>", line)
	if find_full_page_service or find_full_page_service_legacy:
	# if find_full_page_service or find_full_page_service_legacy:
                print "-" * 50
                print "FULL PAGE CACHE"
                print "-" * 50
		find_full_page_service = str(find_full_page_service.group(1))
		print "Service  :", find_full_page_service
	if find_full_page_server:
		find_full_page_server = str(find_full_page_server.group(1))
		find_full_page_server = replace_CDATA(find_full_page_server)
		print "Host     :", find_full_page_server
	if find_full_page_port:
		find_full_page_port = str(find_full_page_port.group(1))
		find_full_page_port = replace_CDATA(find_full_page_port)
		print "Port     :", find_full_page_port
	if find_full_page_db_number:
		find_full_page_db_number = str(find_full_page_db_number.group(1))
		find_full_page_db_number = replace_CDATA(find_full_page_db_number)
		print "DB #     :", find_full_page_db_number
	if find_full_page_password:
		find_full_page_password = str(find_full_page_password.group(1))
		find_full_page_password = replace_CDATA(find_full_page_password)
		print "Password :", find_full_page_password

def xml_inspect():		
	print ""
	admin_url()
	db_connection()
	print ""
	session_save()
	print ""
	full_page_cache()
	print ""

def XML_option():
	global local_xml
	xml_array = []
	# print "Which XML file would you like to inspect? "
	x = 0
	for w in magento_file:
		xml_array.append(w)
	for y in xml_array:
	        print "Option ", x, " ", y
        	x += 1
	input_incorrect = True
	while input_incorrect:
		XML_answer = raw_input("Which XML file would you like to inspect? ")
		XML_answer = int(XML_answer)
		if ( XML_answer + 1) <= len(xml_array):
			XML_option = xml_array[XML_answer]
		 	input_incorrect = False
			local_xml = str(XML_option)
			return XML_option
		else:
			print "Incorrect Value, please try again"
			input_incorrect = True


get_http_includes()
http_vhost_directory_fullpath(server_root, config_directory)
website_configuration(vhost_directory_path, SUFFIX)
document_root(config_files)
find_xml_file(DocRoots)

print ""
print ""
print_header()
XML_option()
print ""
print ""
xml_inspect()
