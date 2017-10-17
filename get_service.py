#!/usr/bin/python
import os
import subprocess



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
            web_server = 'nginx'
            print "nginx enabled"
        elif s.service_running(_apache) and s.service_running('nginx') == False:
            web_server = 'httpd'
            print 'httpd running'
        elif s.service_running(_apache) and s.service_running('nginx'):
            web_server = []
            web_server = ['httpd', 'nginx']
            print "Two webservers running:"
            for i in web_server: print i
        else:
            print "Non-legacy"
            print "No web servers appear to be running"
            print "You can run the script manually with '--nginx' or '--apache' "
            print _apache


    def Legacy_init(self, _apache):
        l = LegacyInit()
        if l.service_running('nginx') and l.service_running(_apache) == False:
            web_server = 'nginx'
            print "nginx enabled"
        elif l.service_running(_apache) and l.service_running('nginx') == False:
            web_server = 'apache'
            print 'httpd running'
        elif l.service_running(_apache) and l.service_running('nginx'):
            web_server = []
            web_server = ['apache2', 'nginx']
            print "Two webservers running:"
            for i in web_server: print i
        else:
            print "Legacy"
            print "No web servers appear to be running"
            print "You can run the script manually with '--nginx' or '--apache' "
            print _apache


    def _get_distro(self):
        _web_distro = self.check_os()
        if _web_distro == 'centos' or _web_distro == 'rhel':
            apache_server = 'httpd'
            self.SystemD(apache_server)
        elif _web_distro == 'ubuntu' or _web_distro == 'debian':
            apache_server = 'apache2'
            self.Legacy_init(apache_server)
        return apache_server


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
        return _web.cmd_output(cmd, silentfail=True).strip() == what

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
        return _web.cmd_returncode(cmd) == 0



_web = get_os_webservers()
print _web._get_distro()
