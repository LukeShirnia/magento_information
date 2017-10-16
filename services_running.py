#!/usr/bin/python

import os



def cmd_output_iter(cmdline, silentfail=False):
    """
    Run the given command and return the output line by line (generator)
    Use this for iterating over long command outputs. Unlike cmd_output, it doesn't store
    it whole in memory.
    """
    devnull = open(os.devnull, 'wb')
    p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=devnull)
    for line in p.stdout:
        yield line
    p.wait()
    devnull.close()
    if p.returncode != 0 and not silentfail:
        raise RuntimeError('Error while executing: \'%s\'' % cmdline)



class LegactInit():

 
    def list_services():
        return list(os.listdir('/etc/init.d'))

        def service_enabled(self, svc):
            # If upstart files detected, assume the service is normally enabled (parsing upstart
            # files properly would be too much pain). Only return False if service was set to
            # 'manual'.
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
            return cmd_returncode(cmd) == 0


class Systemd():


        def list_services(self):
            ret = []
            cmd = 'systemctl -l --plain --no-legend list-units --all --type service | tr -s " "'
            for line in cmd_output_iter(cmd):
                (unit, load, active, sub, description) = line.strip().split(' ', 4)
                ret.append(unit[:-8])
            return ret

        def _service_is(self, what, svc):
            cmd = 'systemctl is-%s %s.service' % (what, svc)
            return cmd_output(cmd, silentfail=True).strip() == what

        def service_enabled(self, svc):
            return self._service_is('enabled', svc)

        def service_running(self, svc):
            return self._service_is('active', svc)


Systemd().list_services
