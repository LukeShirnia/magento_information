# Magento_Information


### Magento Information Gathering

Note:Currently only works with magento 1.x

This script is designed to quickly gather information about specific magento sites located on Linux devices. 


`wget https://raw.githubusercontent.com/LukeShirnia/magento_information/master/magento_info.py`

`sha1sum magento.py`

Output:

`aa48d789d8aacd781f363c72e48b9f26285ceb6c  magento_info.py`

<br />

```
Usage: magento_info.py [option]

Options:
  -h, --help           show this help message and exit
  -a, --apache         Manually check apache webserver for magento sites
  -n, --nginx          Manually check nginx webserver for magento sites
  -x file, --xml=file  Manually parse magento local.xml file
```


* CentOS/RHEL 5, 6, 7 compatible
* Ubuntu/Debian 12, 14, 16.04LTS compatible


<br />

If you would ONLY like to parse the local.xml file you can use the following script:
<br />
Replace "local.xml" in the command below with the full path to your file.

```
python magento -x local.xml
```
