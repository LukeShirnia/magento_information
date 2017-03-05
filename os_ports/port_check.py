pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

def webserver_check():
	 for pid in pids:
		try:
			if os.path.exists('/proc/{0}/exe'.format(pid)):
				processes = os.readlink('/proc/{0}/exe'.format(pid))
				regex_process = re.search("(httpd|nginx|apache2)+", processes)
				print regex_process
webserver_check()
