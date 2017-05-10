#!/usr/bin/python
import platform
import sys
# does not currently work on RHEL/CENTOS 5

supported_centos = ['5', '6', '7']
supported_ubuntu = ['12', '14', '16']
CentOS_RedHat_Distro = ['redhat', 'centos', 'red', 'red hat']
Ubuntu_Debian_Distro = ['ubuntu', 'debian']

def version_check():
	os_version = platform.linux_distribution()[1]
	os_version = os_version.split(".")[0]
	
	if os_version in supported_centos:
		print "Supported RedHat/CentOS"
		print platform.linux_distribution()[1]
	elif os_version in supported_ubuntu:
		print "Supported Ubuntu/Debian"
		print platform.linux_distribution()[1]
	else:
		print "Something wrong"
		print os_version 

def os_check():
        os_platform = platform.system()
        if os_platform == "Linux":
                distro = platform.linux_distribution()[0]
                distro = distro.split()[0]
                return distro
        else:
		print "Stop Using a Rubbish OS!!"

os_check_value = os_check()
if os_check_value.lower() in CentOS_RedHat_Distro:
	print os_check_value
	version_check()
elif os_check_value.lower() in Ubuntu_Debian_Distro:
	print os_check_value
	version_check()
else:
	print "OS Not Recognised"
