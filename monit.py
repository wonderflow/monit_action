__author__ = 'sun'

import os,urllib2,urllib,base64
import xml.etree.ElementTree as ET
from novaclient.client import Client


stackname = "mystack"
username = "vcap"
password = "password"

nova = Client(2, "admin", "zjuvlis", "demo", "http://10.10.101.106:35357/v2.0")
#iplist_cmd  = "nova list  | grep %s | awk '{print $12}' | cut -f 2 -d '=' | cut -f 1 -d ',' "%(stackname)


def monit_job(ip):
    url = "http://"+ip+":2822/_status?format=xml"
    request = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    result = urllib2.urlopen(request)
    status_xml = result.read().strip()
    root = ET.fromstring(status_xml)
    for ch1 in root:
        if ch1.tag == "service" and ch1.attrib['type']=='3':
            for ch2 in ch1:
                if ch2.tag == 'name':
                    print ch2.text,
                if ch2.tag == 'monitor':
                    if ch2.text == '1':
                        print "runing"
                    else:
                        print "not monitored"


servers = nova.servers.list()
for server in servers:
    if "mystack" not in server.name: continue
    ip = server.networks['private'][0]
    monit_job(ip)




#iplist_cmd = "cat list"

#iplist = os.popen(iplist_cmd).read().split("\n")

