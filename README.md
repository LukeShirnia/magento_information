# python-not-production-
This python section is for current projects. Nothing in here should be cloned/run unless stated in the README!


### XML Parsing

Run the command below to quickly pull in the details for the local.xml file.
<br /> 
Replace "local.xml" in the command below with the full path to your file. 


```
curl -s https://raw.githubusercontent.com/LukeShirnia/magento_information/master/Parsing_XML.py | python - local.xml
```
<br />

<br />


### Magento Information Gathering

* Still in Testing Phase - USE AT YOUR OWN RISK *

This script can be used on a CentOS/RHEL box running apache. It will present you with potential xml files to parse and then as you for your option 

<br />
Current working version of "Magento Information Gatherer" can be used by running the following command:



```
python <(curl -s https://raw.githubusercontent.com/LukeShirnia/magento_information/master/magento_information_gathering.py)
```

This script is only tested on:
  RHEL 7/CentOS 7 with Httpd 2.4.x
