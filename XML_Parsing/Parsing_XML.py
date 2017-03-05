# http://stackoverflow.com/questions/18865058/extract-values-between-two-strings-in-a-text-file-using-python
import re

def replace_cdata(xml_variable):
	xml_variable = xml_variable.replace("<![CDATA[", "")
	xml_variable = xml_variable.replace("]]>","")
	return xml_variable
	
def db_connection():
	with open('local.xml') as infile:
		copy = False
		for line in infile:
			if line.strip() == "<connection>":
				copy = True
			elif line.strip() == "</connection>":
				copy = False
			elif copy:
				find_db_host = re.search("<host>(.*)</host>", line)
				find_db_username = re.search("<username>(.*)</username>", line)
				find_db_password = re.search("<password>(.*)</password>", line)
				find_db_dbname = re.search("<dbname>(.*)</dbname>", line)
				if find_db_host:
					find_db_host = find_db_host.group(1)
					find_db_host = replace_cdata(find_db_host)
					print "Host     :", find_db_host
				if find_db_username:
					find_db_username = str(find_db_username.group(1))
					find_db_username = replace_cdata(find_db_username)
					print "Username :", find_db_username
				if find_db_password:
					find_db_password = str(find_db_password.group(1))
					find_db_password = replace_cdata(find_db_password)
					print "Password :", find_db_password
				if find_db_dbname:
					find_db_dbname = str(find_db_dbname.group(1))
					find_db_dbname = replace_cdata(find_db_dbname)					
					print "Database :", find_db_dbname

db_connection()
# print "Host ", find_db_hostdd
# print "Username ", find_db_username
# print "Password ", find_db_password
# print "DB ", find_db_db
