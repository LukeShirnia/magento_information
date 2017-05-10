import os
import re
from sys import argv

#pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
#for pid in pids:
#	try:
#		processes = os.readlink('/proc/{0}/exe'.format(pid))
#		if 'httpd' in processes:
#			print processes
#	except:
#		pass

pid_name = []
#while True:
#	for pid in os.listdir('/proc'):
#			if pid.isdigit():
#				try:
#					process_path = '/proc/%s/exe' % (pid)
#					process = os.readlink(process_path)
#					if 'httpd' in process:
#						print process
#						quit()
#					
#				except:
#					pass

def find_pids(pid_to_find):
	continue_loop = True
	while continue_loop:
	       for pid in os.listdir('/proc'):
				try:
					process_path = '/proc/%s/exe' % (pid)
					process = os.readlink(process_path)
	        	                if pid.isdigit() and pid_to_find in process:
        	        	                print process, pid
                	        	        continue_loop = False
				except:
					pass

if len(argv) == 1:
	find_pids('http')
elif len(argv) == 2:
	script, pid = argv
	find_pids(pid)
else:
	print "Too many arguments"
