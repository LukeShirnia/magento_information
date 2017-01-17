#!/usr/bin/python
import platform
import sys

def os_check():
        global os_platform, os_distro, os_version
        os_platform = platform.system()

        if os_platform == "Linux":
                os_distro = platform.linux_distribution()[0]
                #os_version = int(float(platform.linux_distribution()[1]))
                os_version = platform.linux_distribution()[1]
                print os_distro, os_version
         else:
                print "Stop Using A Rubish OS"



os_check()
