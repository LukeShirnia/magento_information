# Magento_Information


### Magento Information Gathering

Currently there are 2 versions of this script, 1 for httpd (CentOS/RHEL) and one for nginx (CentOS/RHEL and possible Ubuntu/Debian).

<br />
There are currently plans to merge the scripts together and "clean" the code. 

<br />
### HTTP

* ONLY works on CentOS/RHEL

This script can be used on a CentOS/RHEL box running apache. It will present you with potential xml files to parse and then as you for your option 

<br />
Current working version of httpd "Magento Information Gatherer" can be used by running the following command:


```
python <(curl -s https://raw.githubusercontent.com/LukeShirnia/magento_information/master/httpd_magento_information_gathering.py)
```

This script is only tested on:
  RHEL 7/CentOS 7 with Httpd 2.4.x

<br />

<br />

### Nginx

* Only tested on CentOS/RHEL...this script may also work with Ubuntu/Debian

<br />

```
python <(curl -shttps://raw.githubusercontent.com/LukeShirnia/magento_information/master/nginx_magento_information_gathering.py)

```
<br />

<br />

### XML Parsing

Run the command below to quickly pull in the details for the local.xml file.
<br />
Replace "local.xml" in the command below with the full path to your file.


```
curl -s https://raw.githubusercontent.com/LukeShirnia/magento_information/master/Parsing_XML.py | python - local.xml
```

