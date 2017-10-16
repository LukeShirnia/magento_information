# Magento_Information


### Magento Information Gathering

This script is designed to quickly gather information about specific magento sites located on Linux devices. 

<br />

```
Usage: magento_info.py [option]

Options:
  -h, --help    show this help message and exit
  -a, --apache  Check apache webserver for magento sites
  -n, --nginx   Check nginx webserver for magento sites
```



* Works on CentOS/RHEL
* Designed to work on Ubuntu/Debian...Not yet tested


<br />


### XML Parsing

Run the command below to quickly pull in the details for the local.xml file.
<br />
Replace "local.xml" in the command below with the full path to your file.


```
curl -s https://raw.githubusercontent.com/LukeShirnia/magento_information/master/Parsing_XML.py | python - local.xml
```

