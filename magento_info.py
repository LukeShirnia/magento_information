#!/usr/bin/env python
import subprocess
import re
import sys
import os
import urllib2


class bcolors:
    """
    This class is to display differnet colour fonts
    """
    GREEN = '\033[1;32m'
    RESET = '\033[0m'
    WHITE = '\033[1m'
    CYAN = '\033[96m'


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
            self.webserver_config = '/etc/httpd/conf/httpd.conf'
            self.doc_root_name = 'documentroot '
            self.webServerName = 'ServerName'
            self.webServerAlias = 'ServerAlias'
            self.StartsWith = '<VirtualHost '
            self.listen_port = '<VirtualHost '
            self.port_split = ':'
            self.EndsWith =  '</VirtualHost>'
            self.re_start_match = '<VirtualHost'
            self.web_path = '/etc/httpd'
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
    #n = webserver_Ctl('httpd')
    n = webserver_Ctl('nginx')

    if len(sys.argv) == 1:
        n.select_option()
    else:
        print "No options available"
        print "Re-run script with NO options"
if __name__ == "__main__":
    main()
