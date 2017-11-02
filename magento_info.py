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


class get_os_webservers():

    def cmd_output(self, cmdline, silentfail=False):
        """
        Run the given command and return the output
        """
        p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            if silentfail:
                return ''
            else:
                raise RuntimeError('Error while executing \'%s\': %s' % (cmdline, stderr.strip()))
        return stdout


    def cmd_returncode(self, cmdline):
        """
        Run the given command and return it's return code
        """
        devnull = open(os.devnull, 'wb')
        p = subprocess.Popen(cmdline, shell=True, stdout=devnull, stderr=devnull)
        p.wait()
        return p.returncode


    def file2dict(self, filename, separator='=', valproc=lambda x: x):
        """
        Read key-value type config file into a dictionary
        """
        f = open(filename)
        lines = [x.split(separator, 1) for x in f.readlines()]
        f.close()
        res = {}
        for key, val in lines:
            res[key.strip()] = valproc(val.strip().strip('"'))
        return res


    def readfile(self, filename):
        """
        Return the whole contents of the given file
        """
        f = open(filename)
        ret = f.read().strip()
        f.close()
        return ret


    def check_os(self):
        if os.path.exists('/etc/redhat-release'):
            s = self.readfile('/etc/redhat-release')
            if s.startswith('Red Hat Enterprise Linux'):
                server_id = 'rhel'
                server_distr = 'RHEL'
                return server_id
            elif s.startswith('CentOS'):
                server_id = 'centos'
                server_distro = 'CentOS'
                return server_id
            elif s.startswith('Fedora'):
                server_id = 'fedora'
                server_distro = 'Fedora'
                return server_id
            for i in s.split(' '):
                if i[0].isdigit():
                    server_version = i
                    break
        elif os.path.exists('/etc/lsb-release'):
            lsb = self.file2dict('/etc/lsb-release')
            server_id = lsb['DISTRIB_ID'].lower()
            server_distro = lsb['DISTRIB_ID']
            server_version = lsb['DISTRIB_RELEASE']
            return server_id
        elif os.path.exists('/etc/os-release'):
            lsb = self.file2dict('/etc/os-release')
            server_id = lsb['ID'].lower()
            server_distro = lsb['ID'].capitalize()
            server_version = lsb['VERSION']
            return server_id
        else:
            server_id = 'unknown'
            server_distro = 'Unknown Distro'
            server_version = 'Unknown Version'
            return server_id


    def SystemD(self, _apache):
        s = Systemd()
        if s.service_running('nginx') and s.service_running(_apache) == False:
            web_server = []
            web_server = ['nginx']
            return web_server
        elif s.service_running(_apache) and s.service_running('nginx') == False:
            web_server = []
            web_server = ['httpd']
            return web_server
        elif s.service_running(_apache) and s.service_running('nginx'):
            web_server = []
            web_server = ['httpd', 'nginx']
            return web_server
        else:
            print "Non-legacy"
            print "No web servers appear to be running"
            print "You can run the script manually with '--nginx' or '--apache' "
            print _apache


    def Legacy_init(self, _apache):
        l = LegacyInit()
        if l.service_running('nginx') and l.service_running(_apache) == False:
            web_server = 'nginx'
            return web_server
        elif l.service_running(_apache) and l.service_running('nginx') == False:
            web_server = 'apache'
            return web_server
        elif l.service_running(_apache) and l.service_running('nginx'):
            web_server = []
            web_server = ['apache2', 'nginx']
            return web_server
        else:
            print "Legacy"
            print "No web servers appear to be running"
            print "You can run the script manually with '--nginx' or '--apache' "
            print _apache

    def _get_distro(self):
        _web_distro = self.check_os()
        _web_age = self._web_age()
        if _web_distro == 'centos' or _web_distro == 'rhel':
            apache_server = 'httpd'
            if _web_age == 'SystemD':
                web_server = self.SystemD(apache_server)
            else:
                web_server = self.Legacy_init(apache_server)
        elif _web_distro == 'ubuntu' or _web_distro == 'debian':
            apache_server = 'apache2'
            if _web_age == 'SystemD':
                web_server = self.SystemD(apache_server)
            else:
                web_server = self.Legacy_init(apache_server)
        return web_server

    def _web_age(self):
        if os.path.exists('/proc/1/comm') and 'systemd' in self.readfile('/proc/1/comm'):
            age = 'SystemD'
        else:
            age = 'Legacy'
        return age


class Systemd(object):
    """
    Systemd (systemctl) wrapper
    """
    def list_services(self):
        ret = []
        cmd = 'systemctl -l --plain --no-legend list-units --all --type service | tr -s " "'
        for line in cmd_output_iter(cmd):
            (unit, load, active, sub, description) = line.strip().split(' ', 4)
            ret.append(unit[:-8])
        return ret

    def _service_is(self, what, svc):
        cmd = 'systemctl is-%s %s.service' % (what, svc)
        return get_os_webservers().cmd_output(cmd, silentfail=True).strip() == what

    def service_running(self, svc):
        return self._service_is('active', svc)



class LegacyInit(object):
    """
    SystemV and Upstart wrapper
    """
    def list_services(self):
        return list(os.listdir('/etc/init.d'))

    def service_enabled(self, svc):
        upstart = False
        for upstartf in ('/etc/init/%s.override', '/etc/init/%s.conf'):
            if os.path.exists(upstartf % svc):
                upstart = True
                f = open(upstartf % svc)
                for line in f:
                    if line.split(' ')[0].strip() == 'manual':
                        return False
                f.close()
        if upstart:
            return True

        for s in os.listdir('/etc/rc3.d'):
            if s[0] == 'S' and s[3:] == svc:
                return True
        return False

    def service_running(self, svc):
        cmd = 'service %s status' % svc
        return get_os_webservers().cmd_returncode(cmd) == 0



class XML_Parse(object):
    def __init__(self, arg):
        self.local_xml = arg['magento_root']
        self.s_name = arg['servername']
        self.doc_root = arg['document_root']
        self.magento_config = arg['config_file']
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
            #print "-" * 50
            admin = str(admin.group(1))
            admin = self.replace_CDATA(admin)
            print "{0}Admin URL:{1:>8}{2}".format(bcolors.GREEN, bcolors.RESET, admin)
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
   

    def vhost_information(self):
        print '{0}Domain:{1:>11}{2}'.format(bcolors.YELLOW, bcolors.RESET,
                                        self.s_name)
        print '{0}DocumentRoot:{1:>5}{2}'.format(bcolors.YELLOW, bcolors.RESET,
                                        self.doc_root)
        print '{0}Config File:{1:6}{2}'.format(bcolors.YELLOW, bcolors.RESET,
                                        self.magento_config)

 
    def _xml_check(self):
        self.vhost_information()
        self.admin_url()
        self.db_connection()
        print ""
        self.session_save()
        print ""
        self.full_page_cache()
        print ""


class webserver_Ctl(object):
        

    def __init__(self, arg1, arg2):
        self.webserver = arg1
        self.magento_counter = arg2
        if self.webserver == 'nginx':
            self.webserver_config = '/etc/nginx/nginx.conf'
            self.doc_root_name = 'root '
            self.webServerName = 'server_name'
            self.webServerAlias = 'server_name'
            self.StartsWith = '{'
            self.listen_port = 'listen'
            self.port_split = ''
            self.EndsWith =  '}'
            self.re_start_match = 'server '
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
            print "Web Server Wrong: ", self.webserver, self.magento_counter
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
            path = os.path.join(included_from_dir, self._strip_line(path))
            if not os.path.exists(os.path.dirname(path)) or not os.path.isfile(path):
                path = os.path.join(root, orig_path)

        if os.path.isfile(path):
            return [path]
        elif '/*' not in path and not os.path.exists(path):
            return []

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
                if line_num >= server_block[0]:
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
#                    if vhost_list[i]['config_file'] == vhost_list[b]['config_file']:
#                       print vhost_list[i]['config_file'], vhost_list[b]['config_file']
#                       print "config_match"
#                    for r in vhost_list[i]['alias']:
#                        print r, vhost_list[b]['servername']
#                        if r == vhost_list[b]['servername']:
#                            print "alias"
#                    for l in vhost_list[b]['alias']:
#                        print l, vhost_list[i]['servername']
#                        if b in vhost_list[i]['servername']:
#                            print "alias2"
#                    for sba in vhost_list[b]['alias']:
#                       for sib in vhost_list[i]['alias']:
#                           if sba == sib:
#                                print "match"
 #                               print sba, sib
                    if vhost_list[i]['servername'] == vhost_list[b]['servername']:
                        if len(vhost_list[i]['ip_port']) >= len(vhost_list[b]['ip_port']):
#                            print 'del 1'
                            del vhost_list[int(b)]
                        elif  len(vhost_list[b]['ip_port']) >  len(vhost_list[i]['ip_port']):
                            del vhost_list[int(i)]
#                            print "del 2"
                        else:
                            print "continue.."
                            continue
#                    if vhost_list[i]['servername'] in vhost_list[b]['alias']:
#                        print "alias"
                except:
                    return vhost_list
        return vhost_list

    def get_vhosts(self):
        vhosts_list = self._get_vhosts()
        print ""
        print "%sMagento Site Configuration for %s:%s" % (bcolors.YELLOW, self.webserver, bcolors.RESET)
        print ""
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
            if servername != None: # catches ssl.conf etc which has no servername
                serveralias = vhost.get('alias', None)
                serveralias = set(serveralias)
                line_number = vhost.get('l_num', None)
                config_file = vhost.get('config_file', None)
                _document_root = self.document_root(config_file)
                _magento = self.find_xml_file(_document_root)
                if _magento:
                    _magento = ''.join(_magento)
                    _document_root = ''.join(_document_root)
                    all_magento_sites[self.magento_counter] = {}
                    all_magento_sites[self.magento_counter]['config_file'] = config_file
                    all_magento_sites[self.magento_counter]['document_root'] = _document_root 
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

    def return_counter(self):
        return self.magento_counter


class SelectAnOption(object):

    def __init__(self, arg):
        self.option = arg
        self.magento_counter = 1 

    def select_option(self):
        if self.option == "both":
            for i in ['nginx', 'httpd']:
                w = webserver_Ctl(i, self.magento_counter)
                if i == "nginx":
                     vhost_nginx = w.get_vhosts()
                else:
                     vhost_httpd = w.get_vhosts()
                self.magento_counter = w.return_counter()
            vhosts = self.combine_site_information(vhost_nginx, vhost_httpd)
        else:
            self.option = ''.join(self.option)
            w = webserver_Ctl(self.option, self.magento_counter)
            vhosts = w.get_vhosts()
        magento_counter = w.return_counter()
        incorrect = True
        option_information = {}
        while incorrect:
            not_integer = True
            while not_integer:
                print ""
                print "Please select and option: ",
                tty = open('/dev/tty')
                option_answer = tty.readline().strip()
                tty.close()
                print ""
                if option_answer.isdigit():
                    option_answer = int(option_answer)
                    if ( option_answer ) < magento_counter and ( option_answer > 0 ):
                        _answer = vhosts[option_answer]
                        return _answer
                        incorrect = False
                        not_integer = False
                    else:
                        print "Option number out of range, try again"
                        print ""

    def combine_site_information(self, vhost_nginx, vhost_httpd):
        entry = int( len(vhost_nginx) + 1 )
        
        for y in vhost_httpd:
            vhost_nginx[entry] = vhost_httpd[y]
            entry = entry + 1
        return vhost_nginx           



def choose_server(options):
    counter = len(options)
    for i in range(1, counter+1):
        print "%s\t%s" % (i, options[i-1])
    print "Select option ",
    tty = open('/dev/tty')
    option_answer = tty.readline().strip()
    tty.close()
    if option_answer.isdigit():
        option_answer = int(option_answer)
        if ( option_answer - 1 ) < counter and ( option_answer > 0 ):
            print ""
            _answer = options[option_answer - 1]
            return _answer
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
                print "Apache does not appear to have any magento sites"
    elif len(sys.argv) == 1:
        _web = get_os_webservers()
        option = _web._get_distro()
        if len(option) == 1:
            try:
                n = SelectAnOption(option)
                site_dict = n.select_option()
                XML_Parse(site_dict)
            except TypeError:
                print "No Magento Sites appear to be running on this webserver"
        elif len(option) == 2:
            print "2 WebServers running! " 
            option = "both"
            try:
                n = SelectAnOption(option)
                site_dict = n.select_option()
                XML_Parse(site_dict)
            except TypeError:
                print "No Magento Sites appear to be running on this webserver"
        else:
            print "No Webservers appear to be running"
            print "Run with --apache or --nginx to run manually"
            print ""


if __name__ == "__main__":
    try:
        main()
    except(EOFError, KeyboardInterrupt):
        print
        sys.exit(0)
