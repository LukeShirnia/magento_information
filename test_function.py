xml_array = ['file1', 'file2', 'file3']

def XML_option():
        print "Which XML file would you like to inspect? "
	x = 0
        for y in xml_array:
                print "Option ", x , y
                XML_answer = raw_input("Which XML file would you like to inspect? ")
                XML_answer = int(XML_answer)
		x += 1
        if ( XML_answer + 1) <= len(xml_array)
                XML_option == xml_array[XML_answer]
                return XML_option

XML_option()
