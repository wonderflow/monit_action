__author__ = 'sun'

import os,urllib2,urllib,base64
import xml.etree.ElementTree as ET

stackname = "mystack"
username = "vcap"
password = "password"


#iplist_cmd  = "nova list  | grep %s | awk '{print $12}' | cut -f 2 -d '=' | cut -f 1 -d ',' "%(stackname)

iplist_cmd = "cat list"

iplist = os.popen(iplist_cmd).read().split("\n")


# ip = "10.10.101.132"

def monit_job(ip):
    url = "http://"+ip+":2822/_status?format=xml"
    request = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    result = urllib2.urlopen(request)
    status_xml = result.read().strip()
    root = ET.fromstring(status_xml)
    #tree = ET.parse(status_xml)
    #root = tree.getroot()



    for ch1 in root:
        #print child.tag,child.attrib
        if ch1.tag == "service" and ch1.attrib['type']=='3':
            for ch2 in ch1:
                if ch2.tag == 'name':
                    print ch2.text,
                if ch2.tag == 'monitor':
                    if ch2.text == '1':
                        print "runing"
                    else:
                        print "not monitored"




for ip in iplist:
    if ip != "":
        print ip
        monit_job(ip)



