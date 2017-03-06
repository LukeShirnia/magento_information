Not_Integer = True
while Not_Integer:
	XML_answer = raw_input("Which XML file would you like to inspect? ")
	if XML_answer.isdigit():
		print "Yes"
		Not_Integer = False
