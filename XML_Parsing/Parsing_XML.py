# http://stackoverflow.com/questions/18865058/extract-values-between-two-strings-in-a-text-file-using-python
import re

def replace_CDATA(xml_variable):
	xml_variable = xml_variable.replace("<![CDATA[", "")
	xml_variable = xml_variable.replace("]]>","")
	return xml_variable

def admin_url():
        with open('long.local.xml') as infile:
                record = False
                for line in infile:
                        if line.strip() == "<adminhtml>":
                                record = True
                        elif line.strip() == "</adminhtml>":
                                record = False
                        elif record:
				admin_information(line)

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
	with open('long.local.xml') as infile:
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
	session_db_start = ("<redis_session>","<memcache_session>")
	session_db_end = ("</backend_options>", "</redis_session>","</memcache_session>")
        with open('long.local.xml') as infile:
                for line in infile:
			if line.strip() == "<session_save><![CDATA[db]]></session_save>":
				session_db_information()

def session_db_information():
#        session_db_start = ("<redis_session>","<memcache_session>")
#        session_db_end = ("</backend_options>", "</redis_session>","</memcache_session>")
        with open('long.local.xml') as infile:
                record = False
	        for line in infile:
			if line.strip() == "<redis_session>":
				record = True
                        elif line.strip() == "</cache>":
                                record = False
                        elif record:
                                session_information(line)

def session_information(line):
        find_session_host = re.search("<host>(.*)</host>", line)
        find_session_port = re.search("<port>(.*)</port>", line)
        find_session_password = re.search("<password>(.*)</password>", line)
        find_databases_number = re.search("<database>(.*)</database>" , line)
	if find_session_host:
		find_session_host = str(find_session_host.group(1))
		find_session_host = replace_CDATA(find_session_host)
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
		
admin_url()
db_connection()
print ""
print ""
session_save()
