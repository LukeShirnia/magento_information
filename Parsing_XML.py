import re
from sys import argv


class bcolors:
        '''
        Class used for colour formatting
        '''
        HEADER = '\033[95m'
        RED = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        PURPLE = '\033[35m'
        LIGHTRED = '\033[91m'
        CYAN = '\033[36m'
        UNDERLINE = '\033[4m'


#class XML_Parse(object):
        #def __init__(self, local_xml)
                #self.local_xml=local_xml

# function used to strip CDATA if present
def replace_CDATA(xml_variable):
        '''
        Replace the CDATA from the lines, stripping out the data
        '''
        xml_variable = xml_variable.replace("<![CDATA[", "")
        xml_variable = xml_variable.replace("]]>","")
        return xml_variable


def replace_session_CDATA(session_variable):
        '''
        Replace "session" string from extracted data
        '''
        session_variable = session_variable.replace("<![CDATA[", "")
        session_variable = session_variable.replace("]]>","")
        session_variable = session_variable.replace("<session_save>", "")
        session_variable = session_variable.replace("</session_save>", "")
        return session_variable


def admin_url():
        '''
        Open the xml file and locate the admin url tags, record all lines in between <adminhtml>
        '''
        with open(local_xml) as infile:
                record = False
                for line in infile:
                        if line.strip() == "<adminhtml>":
                                record = True
                        elif line.strip() == "</adminhtml>":
                                record = False
                        elif record:
                                admin_information(line)


def admin_information(line):
        '''
        Based on the information obtained in the previous function, find the URL inbetween the <frontName> tag
        '''
        admin = re.search("<frontName>(.*)</frontName>",line)
        if admin:
                print "-" * 50
                admin = str(admin.group(1))
                admin = replace_CDATA(admin)
                print bcolors.GREEN + "Admin URL:" + bcolors.ENDC , admin
                print "-" * 50
                print ""


def db_connection():
        '''
        Start "recording" once the <connection> tag is found.
        Every line is then searched in the db_information() function
        '''
        print "-" * 50
        print bcolors.CYAN + "DATABASE INFORMATION" + bcolors.ENDC
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
        '''
        Extract database information
        '''
        find_db_host = re.search("<host>(.*)</host>", line)
        find_db_username = re.search("<username>(.*)</username>", line)
        find_db_password = re.search("<password>(.*)</password>", line)
        find_db_dbname = re.search("<dbname>(.*)</dbname>", line)
        if find_db_host:
                find_db_host = find_db_host.group(1)
                find_db_host = replace_CDATA(find_db_host)
                print bcolors.YELLOW + "Host      :" + bcolors.ENDC, find_db_host
        if find_db_username:
                find_db_username = str(find_db_username.group(1))
                find_db_username = replace_CDATA(find_db_username)
                print bcolors.YELLOW + "Username  :" + bcolors.ENDC, find_db_username
        if find_db_password:
                find_db_password = str(find_db_password.group(1))
                find_db_password = replace_CDATA(find_db_password)
                print bcolors.YELLOW + "Password  :" + bcolors.ENDC, find_db_password
        if find_db_dbname:
                find_db_dbname = str(find_db_dbname.group(1))
                find_db_dbname = replace_CDATA(find_db_dbname)
                print bcolors.YELLOW + "Database  :" + bcolors.ENDC, find_db_dbname


def session_save():
        '''
        Check to see where sessions are saved. Run different functions depending on the session location
        '''
        print "-" * 50
        print bcolors.CYAN + "SESSION INFORMATION" + bcolors.ENDC
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
        '''
        If sessions are saved in memcache, check for specific directives in the line
        '''
        service = "Memcache"
        with open(local_xml) as infile:
                for line in infile:
                        session_save_path = re.search("<session_save_path>(.*)</session_save_path>" , line)
                        if session_save_path:
                                session_save_path = str(session_save_path.group(1))
                                session_save_path = replace_CDATA(session_save_path)
                                print bcolors.YELLOW + "Service   :" + bcolors.ENDC , service
                                print bcolors.YELLOW + "Save Path :" + bcolors.ENDC, session_save_path


def session_db_information():
        '''
        Find out if redis, memcache is used
        '''
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
                                session_information(line, session_service_name)


def session_information(line, session_service_name):
        '''
        Get the session db information
        '''
        find_session_host = re.search("<host>(.*)</host>", line)
        find_session_port = re.search("<port>(.*)</port>", line)
        find_session_password = re.search("<password>(.*)</password>", line)
        find_databases_number = re.search("<database>(.*)</database>", line)
        if find_session_host:
                find_session_host = str(find_session_host.group(1))
                find_session_host = replace_CDATA(find_session_host)
                print bcolors.YELLOW + "Service   :" + bcolors.ENDC, session_service_name
                print bcolors.YELLOW +  "Host      :" + bcolors.ENDC, find_session_host
        if find_session_port:
                find_session_port = str(find_session_port.group(1))
                find_session_port = replace_CDATA(find_session_port)
                print bcolors.YELLOW + "Port      :" + bcolors.ENDC, find_session_port
        if find_session_password:
                find_session_password = str(find_session_password.group(1))
                find_session_password = replace_CDATA(find_session_password)
                print bcolors.YELLOW + "Password  :" + bcolors.ENDC, find_session_password
        if find_databases_number:
                find_databases_number = str(find_databases_number.group(1))
                find_databases_number = replace_CDATA(find_databases_number)
                print bcolors.YELLOW + "Database #:" + bcolors.ENDC, find_databases_number


def full_page_cache():
        '''
        Find out if full page cache is used
        '''
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
        '''
        If full page cache is used, find out all the information about it
        '''
        find_full_page_service = re.search("<backend>Mage_Cache_Backend_(.*)</backend>", line)
        find_full_page_service_legacy = re.search("<backend>Cm_Cache_Backend_(.*)</backend>", line)
        find_full_page_server = re.search("<server>(.*)</server>", line)
        find_full_page_port = re.search("<port>(.*)</port>", line)
        find_full_page_db_number = re.search("<database>(.*)</database>", line)
        find_full_page_password = re.search("<password>(.*)</password>", line)
        if find_full_page_service or find_full_page_service_legacy:
                print "-" * 50
                print bcolors.CYAN + "FULL PAGE CACHE" + bcolors.ENDC
                print "-" * 50
                find_full_page_service = str(find_full_page_service.group(1))
                print bcolors.YELLOW + "Service  :" + bcolors.ENDC, find_full_page_service
        if find_full_page_server:
                find_full_page_server = str(find_full_page_server.group(1))
                find_full_page_server = replace_CDATA(find_full_page_server)
                print bcolors.YELLOW + "Host     :" + bcolors.ENDC, find_full_page_server
        if find_full_page_port:
                find_full_page_port = str(find_full_page_port.group(1))
                find_full_page_port = replace_CDATA(find_full_page_port)
                print bcolors.YELLOW + "Port     :" + bcolors.ENDC, find_full_page_port
        if find_full_page_db_number:
                find_full_page_db_number = str(find_full_page_db_number.group(1))
                find_full_page_db_number = replace_CDATA(find_full_page_db_number)
                print bcolors.YELLOW + "DB #     :" + bcolors.ENDC, find_full_page_db_number
        if find_full_page_password:
                find_full_page_password = str(find_full_page_password.group(1))
                find_full_page_password = replace_CDATA(find_full_page_password)
                print bcolors.YELLOW + "Password :" + bcolors.ENDC, find_full_page_password


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
