import re
from sys import argv


class bcolors:
<<<<<<< HEAD
    '''
    Class used for colour formatting
    '''
    HEADER = '\033[95m'
    RED = '\033[91m'
    RESET = '\033[0m'
    GREEN = '\033[1;32m'
    YELLOW = '\033[93m'
    PURPLE = '\033[35m'
    LIGHTRED = '\033[91m'
    #CYAN = '\033[36m'
    CYAN = '\033[96m'
    UNDERLINE = '\033[4m'
=======
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

>>>>>>> 85aaca50733f90297c5856587cc4b8dfc8c2750f

#class XML_Parse(object):
        #def __init__(self, local_xml)
                #self.local_xml=local_xml

<<<<<<< HEAD
class XML_Parse(object):
    def __init__(self, arg):
        self.local_xml = arg
        self._xml_check()
    
    
    def replace_CDATA(self, xml_variable):
=======
# function used to strip CDATA if present
def replace_CDATA(xml_variable):
>>>>>>> 85aaca50733f90297c5856587cc4b8dfc8c2750f
        '''
        Replace the CDATA from the lines, stripping out the data
        '''
        xml_variable = xml_variable.replace("<![CDATA[", "")
        xml_variable = xml_variable.replace("]]>","")
        return xml_variable
<<<<<<< HEAD
    
    
    def replace_session_CDATA(self, session_variable):
=======


def replace_session_CDATA(session_variable):
>>>>>>> 85aaca50733f90297c5856587cc4b8dfc8c2750f
        '''
        Replace "session" string from extracted data
        '''
        session_variable = session_variable.replace("<![CDATA[", "")
        session_variable = session_variable.replace("]]>","")
        session_variable = session_variable.replace("<session_save>", "")
        session_variable = session_variable.replace("</session_save>", "")
        return session_variable
<<<<<<< HEAD
    
    
    def admin_url(self):
        '''
        Open the xml file and locate the admin url tags, record all lines in between <adminhtml>
        '''
        with open(self.local_xml) as infile:
            record = False
            for line in infile:
                    if line.strip() == "<adminhtml>":
                        record = True
                    elif line.strip() == "</adminhtml>":
                        record = False
                    elif record:
                        self.admin_information(line)
    
    
    def admin_information(self, line):
=======


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
>>>>>>> 85aaca50733f90297c5856587cc4b8dfc8c2750f
        '''
        Based on the information obtained in the previous function, find the URL inbetween the <frontName> tag
        '''
        admin = re.search("<frontName>(.*)</frontName>",line)
        if admin:
<<<<<<< HEAD
            print "-" * 50
            admin = str(admin.group(1))
            admin = self.replace_CDATA(admin)
            print bcolors.GREEN + "Admin URL:" + bcolors.RESET , admin
            print "-" * 50
            print ""
    
    
    def db_connection(self):
        '''
        Start "recording" once the <connection> tag is found. 
        Every line is then searched in the db_information() function
        '''
        print "-" * 50
        print bcolors.CYAN + "DATABASE INFORMATION" + bcolors.RESET
        print "-" * 50
        with open(self.local_xml) as infile:
            record = False
            for line in infile:
                if line.strip() == "<connection>":
                    record = True
                elif line.strip() == "</connection>":
                    record = False
                elif record:
                    self.db_information(line)
    
    
    def db_information(self, line):
=======
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
>>>>>>> 85aaca50733f90297c5856587cc4b8dfc8c2750f
        '''
        Extract database information
        '''
        find_db_host = re.search("<host>(.*)</host>", line)
        find_db_username = re.search("<username>(.*)</username>", line)
        find_db_password = re.search("<password>(.*)</password>", line)
        find_db_dbname = re.search("<dbname>(.*)</dbname>", line)
        if find_db_host:
<<<<<<< HEAD
            find_db_host = find_db_host.group(1)
            find_db_host = self.replace_CDATA(find_db_host)
            print bcolors.YELLOW + "Host      :" + bcolors.RESET, find_db_host
            if find_db_username:
                find_db_username = str(find_db_username.group(1))
                find_db_username = self.replace_CDATA(find_db_username)
                print bcolors.YELLOW + "Username  :" + bcolors.RESET, find_db_username
            if find_db_password:
                find_db_password = str(find_db_password.group(1))
                find_db_password = self.replace_CDATA(find_db_password)
                print bcolors.YELLOW + "Password  :" + bcolors.RESET, find_db_password
            if find_db_dbname:
                find_db_dbname = str(find_db_dbname.group(1))
                find_db_dbname = self.replace_CDATA(find_db_dbname)
                print bcolors.YELLOW + "Database  :" + bcolors.RESET, find_db_dbname
    
    
    def session_save(self):
=======
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
>>>>>>> 85aaca50733f90297c5856587cc4b8dfc8c2750f
        '''
        Check to see where sessions are saved. Run different functions depending on the session location
        '''
        print "-" * 50
<<<<<<< HEAD
        print bcolors.CYAN + "SESSION INFORMATION" + bcolors.RESET
        print "-" * 50
        with open(self.local_xml) as infile:
            for line in infile:
                line = self.replace_session_CDATA(line)
                if line.strip() == "db":
                    self.session_db_information()
                elif line.strip() == "memcache":
                    self.session_db_memecache()
                elif line.strip() == "files":
                    print "Sessions    : Files"
    
    
    def session_db_memecache(self):
=======
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
>>>>>>> 85aaca50733f90297c5856587cc4b8dfc8c2750f
        '''
        If sessions are saved in memcache, check for specific directives in the line
        '''
        service = "Memcache"
<<<<<<< HEAD
        with open(self.local_xml) as infile:
            for line in infile:
                session_save_path = re.search("<session_save_path>(.*)</session_save_path>" , line)
                if session_save_path:
                    session_save_path = str(session_save_path.group(1))
                    session_save_path = self.replace_CDATA(session_save_path)
                    print bcolors.YELLOW + "Service   :" + bcolors.RESET , service
                    print bcolors.YELLOW + "Save Path :" + bcolors.RESET, session_save_path
    
        
    def session_db_information(self):
        '''
        Find out if redis, memcache is used 
        '''
        with open(self.local_xml) as infile:
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
                     self.session_information(line, session_service_name)
    
    
    def session_information(self, line, session_service_name):
=======
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
>>>>>>> 85aaca50733f90297c5856587cc4b8dfc8c2750f
        '''
        Get the session db information
        '''
        find_session_host = re.search("<host>(.*)</host>", line)
        find_session_port = re.search("<port>(.*)</port>", line)
        find_session_password = re.search("<password>(.*)</password>", line)
        find_databases_number = re.search("<database>(.*)</database>", line)
        if find_session_host:
<<<<<<< HEAD
            find_session_host = str(find_session_host.group(1))
            find_session_host = self.replace_CDATA(find_session_host)
            print bcolors.YELLOW + "Service   :" + bcolors.RESET, session_service_name
            print bcolors.YELLOW +  "Host      :" + bcolors.RESET, find_session_host
        if find_session_port:
            find_session_port = str(find_session_port.group(1))
            find_session_port = self.replace_CDATA(find_session_port)
            print bcolors.YELLOW + "Port      :" + bcolors.RESET, find_session_port
        if find_session_password:
            find_session_password = str(find_session_password.group(1))
            find_session_password = self.replace_CDATA(find_session_password)
            print bcolors.YELLOW + "Password  :" + bcolors.RESET, find_session_password
        if find_databases_number:
            find_databases_number = str(find_databases_number.group(1))
            find_databases_number = self.replace_CDATA(find_databases_number)
            print bcolors.YELLOW + "Database #:" + bcolors.RESET, find_databases_number
    
    
    def full_page_cache(self):
        '''
        Find out if full page cache is used
        '''
        with open(self.local_xml) as infile:
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
                    self.full_page_information(line)
    
    
    def full_page_information(self, line):
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
            print bcolors.CYAN + "FULL PAGE CACHE" + bcolors.RESET
            print "-" * 50
            find_full_page_service = str(find_full_page_service.group(1))
            print bcolors.YELLOW + "Service  :" + bcolors.RESET, find_full_page_service
        if find_full_page_server:
            find_full_page_server = str(find_full_page_server.group(1))
            find_full_page_server = self.replace_CDATA(find_full_page_server)
            print bcolors.YELLOW + "Host     :" + bcolors.RESET, find_full_page_server
        if find_full_page_port:
            find_full_page_port = str(find_full_page_port.group(1))
            find_full_page_port = self.replace_CDATA(find_full_page_port)
            print bcolors.YELLOW + "Port     :" + bcolors.RESET, find_full_page_port
        if find_full_page_db_number:
            find_full_page_db_number = str(find_full_page_db_number.group(1))
            find_full_page_db_number = self.replace_CDATA(find_full_page_db_number)
            print bcolors.YELLOW + "DB #     :" + bcolors.RESET, find_full_page_db_number
        if find_full_page_password:
            find_full_page_password = str(find_full_page_password.group(1))
            find_full_page_password = self.replace_CDATA(find_full_page_password)
            print bcolors.YELLOW + "Password :" + bcolors.RESET, find_full_page_password
    
    
    def _xml_check(self):
        self.admin_url()
        self.db_connection()
        print ""
        self.session_save()
        print ""
        self.full_page_cache()
        print ""


def main():
    if len(argv) == 1:
        print "Please add an argument of the local.xml file"
    elif len(argv) == 2:
        script, xml_file = argv
        XML_Parse(xml_file) 
    else:
        print "Too many arguments"


if __name__ == "__main__":
    main()
=======
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
>>>>>>> 85aaca50733f90297c5856587cc4b8dfc8c2750f
