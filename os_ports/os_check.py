#!/usr/bin/python
import platform
import sys

#global os_platform

def version_check():
        global os_version, supported_centos, supported_ubuntu, CentOS_RedHat_Distro
        CentOS_RedHat_Distro = ['redhat', 'centos']
        Ubuntu_Debian_Distro = ['ubuntu', 'debian']
        supported_centos = [6, 7]
        supported_ubuntu = [12, 14, 16]
        os_version = platform.linux_distribution()[1]
        os_version_test = os_version.split()

        if os_distro.lower() in CentOS_RedHat_Distro:
                print os_distro, os_version
        elif os_distro.lower() in Ubuntu_Debian_Distro:
                print os_distro, os_version
        else:
                print os_distro, os_version
                print "Something wrong"

def os_check():
        global os_distro, os_version, os_platform
        os_platform = platform.system()

        if os_platform == "Linux":
                os_distro = platform.linux_distribution()[0]
                os_distro = os_distro.split()[0]
                version_check()
        else:
                print "Stop Using A Rubish OS"

os_check()
