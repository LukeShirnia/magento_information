import re
from sys import argv


#class XML_Parse(object):


# function used to strip CDATA if present
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


if len(argv) == 1:	
	print "Please add an argument of the local.xml file"
elif len(argv) == 2:
	script, local_xml = argv
	print ""
	admin_url()
	db_connection()
	print ""
	session_save()
	print ""
	full_page_cache()
	print ""
else:
	print "Too many arguments"
