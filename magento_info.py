#!/usr/bin/env python
import subprocess
import re
import sys
import os
import urllib2
from optparse import OptionParser


class bcolors:
    """
    This class is to display differnet colour fonts
    """
    GREEN = '\033[1;32m'
    RESET = '\033[0m'
    WHITE = '\033[1m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'


class XML_Parse(object):
    def __init__(self, arg):
        self.local_xml = arg
        self._xml_check()
    
    def replace_CDATA(self, xml_variable):
        '''
        Replace the CDATA from the lines, stripping out the data
        '''
        xml_variable = xml_variable.replace("<![CDATA[", "")
        xml_variable = xml_variable.replace("]]>","")
        return xml_variable
    
    def replace_session_CDATA(self, session_variable):
        '''
        Replace "session" string from extracted data
        '''
        session_variable = session_variable.replace("<![CDATA[", "")
        session_variable = session_variable.replace("]]>","")
        session_variable = session_variable.replace("<session_save>", "")
        session_variable = session_variable.replace("</session_save>", "")
        return session_variable
    
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
        '''
        Based on the information obtained in the previous function, find the URL inbetween the <frontName> tag
        '''
        admin = re.search("<frontName>(.*)</frontName>",line)
        if admin:
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
        '''
        Extract database information
        '''
        find_db_host = re.search("<host>(.*)</host>", line)
        find_db_username = re.search("<username>(.*)</username>", line)
        find_db_password = re.search("<password>(.*)</password>", line)
        find_db_dbname = re.search("<dbname>(.*)</dbname>", line)
        if find_db_host:
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
        '''
        Check to see where sessions are saved. Run different functions depending on the session location
        '''
        print "-" * 50
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
        '''
        If sessions are saved in memcache, check for specific directives in the line
        '''
        service = "Memcache"
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
        '''
        Get the session db information
        '''
        find_session_host = re.search("<host>(.*)</host>", line)
        find_session_port = re.search("<port>(.*)</port>", line)
        find_session_password = re.search("<password>(.*)</password>", line)
        find_databases_number = re.search("<database>(.*)</database>", line)
        if find_session_host:
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
        #self.XML_Parse(xml_file)
        #print ""
        self.admin_url()
        self.db_connection()
        print ""
        self.session_save()
        print ""
        self.full_page_cache()
        print ""


class webserver_Ctl(object):

    def __init__(self, arg):
        self.magento_counter = 1
        self.webserver = arg
        if self.webserver == 'nginx':
            self.webserver_config = '/etc/nginx/nginx.conf'
            self.doc_root_name = 'root '
            self.webServerName = 'server_name'
            self.webServerAlias = 'server_name'
            self.StartsWith = '{'
            self.listen_port = 'listen'
            self.port_split = ''
            self.EndsWith =  '}'
            self.re_start_match = 'root '
            self.web_path = '/etc/nginx'
        elif self.webserver == 'httpd':
            if os.path.isfile('/etc/httpd/conf/httpd.conf'):
                self.webserver_config = '/etc/httpd/conf/httpd.conf'
                self.web_path = '/etc/httpd'
            elif os.path.isfile('/etc/apache/apache.conf'):
                self.webserver_config = '/etc/apache/apache.conf'
                self.web_path = '/etc/apache'
            self.doc_root_name = 'documentroot '
            self.webServerName = 'ServerName'
            self.webServerAlias = 'ServerAlias'
            self.StartsWith = '<VirtualHost '
            self.listen_port = '<VirtualHost '
            self.port_split = ':'
            self.EndsWith =  '</VirtualHost>'
            self.re_start_match = '<VirtualHost'
        else:
            print 'error'
            sys.exit(1)

    def _get_vhosts(self):
        """
        get vhosts
        """
        ret = []
        for f in self._get_all_config():
            ret += self._get_vhosts_info(f)
        return ret

    def _strip_line(self, path, remove=None):
        """
        Removes any trailing semicolons, and all quotes from a string
        """
        if remove is None:
            remove = ['"', "'", ';']
        for c in remove:
            if c in path:
                path = path.replace(c, '')
        return path

    def _get_includes_line(self, line, parent, root):
        path = self._strip_line(line.split()[1])
        orig_path = path
        included_from_dir = os.path.dirname(parent)

        if not os.path.isabs(path):
            """ Path is relative - first check if path is
                relative to 'current directory' """
            path = os.path.join(included_from_dir, self._strip_line(path))
            if not os.path.exists(os.path.dirname(path)) or not os.path.isfile(path):
                """ If not, it might be relative to the root """
                path = os.path.join(root, orig_path)

        if os.path.isfile(path):
            return [path]
        elif '/*' not in path and not os.path.exists(path):
            """ File doesn't actually exist - probably IncludeOptional """
            return []

        """ At this point we have an absolute path to a basedir which
            exists, which is globbed
        """
        basedir, extension = path.split('/*')
        try:
            if extension:
                return [
                    os.path.join(basedir, f) for f in os.listdir(
                        basedir) if f.endswith(extension)]

            return [os.path.join(basedir, f) for f in os.listdir(basedir)]
        except OSError:
            return []

    def _get_all_config(self, config_file=None): #working for httpd
        """
        Reads all config files, starting from the main one, expands all
        includes and returns all config in the correct order as a list.
        """
        if config_file is None:
            config_file = self.webserver_config
        else:
            config_file
        ret = [config_file]

        config_data = open(config_file, 'r').readlines()

        for line in [line.strip().strip(';') for line in config_data]:
            if line.startswith('#'):
                continue
            line = line.split('#')[0]
            if line.lower().startswith('include'):
                includes = self._get_includes_line(line,
                                                   config_file,
                                                   self.web_path)
                for include in includes:
                    try:
                        ret += self._get_all_config(include)
                    except IOError:
                        pass
        return ret

    def _get_vhosts_info(self, config_file):
        server_block_boundry = []
        server_block_boundry_list = []
        vhost_data = open(config_file, "r").readlines()
        open_brackets = 0
        found_server_block = False
        for line_number, line in enumerate(vhost_data):
            if line.startswith('#'):
                continue
            line = line.split('#')[0]
            line = line.strip().strip(';')
            if re.match(r"(%s) *"%self.re_start_match, line):
            #if re.match(r"server.*{", line):
                server_block_boundry.append(line_number)
                found_server_block = True
            if self.StartsWith in line:
                open_brackets += 1
            if self.EndsWith in line:
                open_brackets -= 1
            if open_brackets == 0 and found_server_block:
                server_block_boundry.append(line_number)
                server_block_boundry_list.append(server_block_boundry)
                server_block_boundry = []
                found_server_block = False

        server_dict_ret = []
        for server_block in server_block_boundry_list:
            alias = []
            ip_port = []
            server_name_found = False
            server_dict = {}
            for line_num, li in enumerate(vhost_data):
            #for line_num, li in enumerate(vhost_data, start=server_block[0]):
                l = vhost_data[line_num]
                if line_num >= server_block[1]:
                    server_dict['alias'] = alias
                    server_dict['l_num'] = server_block[0]
                    server_dict['config_file'] = config_file
                    server_dict['ip_port'] = ip_port
                    server_dict_ret.append(server_dict)
                    server_name_found = False
                    break

                if l.startswith('#'):
                    continue
                l = l.split('#')[0]
                l = l.strip().strip(';')

                if l.startswith(self.webServerAlias) and server_name_found:
                    alias += l.split()[1:]

                if l.startswith(self.webServerName):
                    if l.split()[1] == "_":
                        server_dict['servername'] = "default_server_name"
                    else:
                        server_dict['servername'] = l.split()[1]
                    server_name_found = True
                    if len(l.split()) >= 2:
                        alias += l.split()[2:]
                if l.startswith(self.listen_port):
                    if self.webserver == 'nginx':
                        ip_port.append(l.split()[1])
                    elif self.webserver == 'httpd':
                        ip_port.append(l.split(':')[1].strip('>'))
        return server_dict_ret

    def sort_sites_dict(self, vhost_list):
        length = len(vhost_list)
        for i in range(0, length):
            for b in range(1, length):
                try:
                    if vhost_list[i]['servername'] == vhost_list[b]['servername']:
                        if len(vhost_list[i]['ip_port']) >= len(vhost_list[b]['ip_port']):
                            del vhost_list[int(b)]
                        elif  len(vhost_list[b]['ip_port']) >  len(vhost_list[i]['ip_port']):
                            del vhost_list[int(i)]
                        else:
                            continue
                except:
                    return vhost_list
        return vhost_list

    def get_vhosts(self):
        vhosts_list = self._get_vhosts()
        print "%sMagento Site Configuration:%s" % (bcolors.WHITE, bcolors.RESET)
        all_magento_sites = {}
        vhosts_list = self.sort_sites_dict(vhosts_list)
        for vhost in vhosts_list:
            ip_port = vhost['ip_port']
            if '[::]' in ip_port:
                pattern = re.compile(r'(\[::\]):(\d{2,5})')
                pattern_res = re.match(pattern, ip_port)
                ip = pattern_res.groups()[0]
                port = pattern_res.groups()[1]
            else:
                ip_port = set(ip_port)
                ip_port = ",".join(map(str, ip_port))
                try:
                    ip = ip_port[0]
                    port = ip_port[1]
                except:
                    ip = '*'
                    port = ip_port[0]
            servername = vhost.get('servername', None)
            serveralias = vhost.get('alias', None)
            serveralias = set(serveralias)
            line_number = vhost.get('l_num', None)
            config_file = vhost.get('config_file', None)
            _document_root = self.document_root(config_file)
            _magento = self.find_xml_file(_document_root)
            if _magento:
                _magento = ''.join(_magento)
                all_magento_sites[self.magento_counter] = {}
                all_magento_sites[self.magento_counter]['servername'] = servername
                all_magento_sites[self.magento_counter]['magento_root'] = _magento
                print "%s%s%s - port %s %s %s %s (%s:%s)" % (bcolors.WHITE,
                                                        self.magento_counter,
                                                        bcolors.RESET,
                                                        ip_port,
                                                        bcolors.GREEN,
                                                        servername,
                                                        bcolors.RESET,
                                                        config_file,
                                                        line_number)
                for alias in serveralias:
                    if alias != servername:
                        print "\t\talias %s %s %s" % (bcolors.CYAN,
                                                      alias,
                                                      bcolors.RESET)
                self.magento_counter += 1
        return all_magento_sites

    def document_root(self, webserver_files_to_search):
        webserver_files_to_search = webserver_files_to_search.split()
        _doc_roots = []
#        del _doc_roots[:]
        root_path = []
        pattern = re.compile("^\s*(%s)"%self.doc_root_name )
        for i in webserver_files_to_search:
                with open(i, "r") as search_file:
                        for line in search_file:
                                if pattern.match(line.lower()):
                                        root_path = line.strip()
                                        root_path = re.split(self.doc_root_name, line, flags=re.IGNORECASE)[1]
                                        _doc_roots.append(root_path)
                                        _doc_roots = [x.rstrip() for x in _doc_roots]
                                        _doc_roots = [x.rstrip(';') for x in _doc_roots]
                                        _doc_roots = filter(None, _doc_roots)
                                        return _doc_roots

    def find_xml_file(self, document_root):
        _app_etc = 'app/etc/'
        xml_full_path = []
        convert_path = []
        webserver_magento_file = []
        local_xml = "local.xml"
        for root in document_root:
            xml_full_path.append(os.path.join(root, _app_etc))
        for p in xml_full_path:
                for root, dirs, files in os.walk(p):
                    if local_xml in files:
                                webserver_magento_file.append(os.path.join(root, local_xml))
                                webserver_magento_file = filter(None, webserver_magento_file)
                                return webserver_magento_file

    def select_option(self):
        vhosts = self.get_vhosts()
        incorrect = True
        while incorrect:
            not_integer = True
            while not_integer:
                print ""
                print "Please select and option: ",
                tty = open('/dev/tty')
                option_answer = tty.readline().strip()
                tty.close()
                if option_answer.isdigit():
                    option_answer = int(option_answer)
                    if ( option_answer ) < self.magento_counter and ( option_answer > 0 ):
                        print ""
                        _answer = vhosts[option_answer]
                        return _answer.get('magento_root')
                        incorrect = False
                        not_integer = False
                    else:
                        print "Option number out of range, try again"
                        print ""


def main():
    parser = OptionParser(usage='usage: %prog [option]')
    parser.add_option("-a", "--apache",
                    action="store_false",
                    default=True,
                    help="Check apache webserver for magento sites")
    parser.add_option("-n", "--nginx",
                    action="store_false",
                    dest="nginx",
                    help="Check nginx webserver for magento sites")

    (options, args) = parser.parse_args()
    if len(sys.argv) == 2:
        select_option = sys.argv[1:]
        select_option = select_option[0]
        if select_option == '-n' or select_option == '--nginx':
            option = 'nginx'
            n = webserver_Ctl(option) 
            try:
                XML_Parse(n.select_option())
            except:
                print "Nginx does not appear to have any magento sites"
        elif select_option == '-a' or select_option == '--apache':
            option = 'httpd'
            n = webserver_Ctl(option)
            try:
                XML_Parse(n.select_option())
            except:
                print ""
                print "Apache does not appear to be running or has no any magento sites"
    elif len(sys.argv) == 1:
        print ""
        print "No options selected, defaulting to apache"
        print ""
        option = 'httpd'
        n = webserver_Ctl(option)
        try:
            XML_Parse(n.select_option())
        except:
            print "Please specify a web server to run against"
            print ""
            print parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except(EOFError, KeyboardInterrupt):
        print
        sys.exit(0)
