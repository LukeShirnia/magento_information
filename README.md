# Magento_Information


### Magento Information Gathering

This script is designed to quickly gather information about specific magento sites located on Linux devices. 


`wget https://raw.githubusercontent.com/LukeShirnia/magento_information/master/magento_info.py`

`sha1sum magento.py`

Output:

`15ec5fb834beb24ed8e760ad5acef6d8e6d5e9b4  magento_info.py`

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

If you would ONLY like to parse the local.xml file you can use the following script:
<br />
Replace "local.xml" in the command below with the full path to your file.


```
curl -s https://raw.githubusercontent.com/LukeShirnia/magento_information/master/Parsing_XML.py | python - local.xml
```

