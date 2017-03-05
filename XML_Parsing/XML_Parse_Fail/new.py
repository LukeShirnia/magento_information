from lxml import etree
import xml.etree.ElementTree as ElementTree

db_list = []

def parse_with_lxml():
	xml_dict = []
	with open("test.xml", "r") as search_file:
		for line in search_file:
			xml_dict = xml_dict.append(line)
			v = line.get("line", {}).get("db", {})
#def get_db():
	if v:
		if ({"host": v.get("host"),
		"dbname": v.get("dbname"),
		"password": v.get("password"),
		"username": v.get("username")} not in db_list):
			db_list.append({"host": v.get("host"),
	   		"dbname": v.get("dbname"),    
			"password": v.get("password"),
			"username": v.get("username")})

parse_with_lxml()
get_db()
print db_list
