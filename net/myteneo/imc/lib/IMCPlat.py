# (c) 2014, Aaron Paxson <aj@thepaxson5.org>
# http://www.myteneo.net
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

"""
This module is a library for HP Intelligent Management Center functions.  It is meant to be used as an
import and then called on.

     from net.myteneo.imc.lib.IMCPlat import IMCConnection

     my_imc = IMCConnection(hostname,port,username,password)

At this point, you should load IMCConnection() with your IMC Master hostname, user/password, etc.  You get data
by calling the get() method with the url.

     data = my_imc.get('/plat/res/device?sysName=hostname')

'data' should then be an XML-based response which you can parse.

     devices = IMCConnection.parseDeviceListing(data.read())

To find out how many devices were returned:

     count = len(devices)

To access the 'ip' attribute of the first device (or only device if 1 result):

     ip_addr = devices[0]['ip']

To list all attributes of the first device:

     print devices[0].getKeys()

"""

import urllib
import urllib2
import xml.etree.ElementTree as ET

class IMCConnection(object):

    def __init__(self, host, port, user, passwd):
        self.host = host
        self.port = port
        self.username = user
        self.passwd = passwd

        imcWebURI = "http://" + self.host + ":" + self.port
        auth_handler = urllib2.HTTPDigestAuthHandler()
        auth_handler.add_password(
            realm='iMC RESTful Web Services',
            uri = imcWebURI,
            user = self.username,
            passwd=self.passwd
        )
        opener = urllib2.build_opener(auth_handler)
        urllib2.install_opener(opener)

    def get(self,url):
        return urllib2.urlopen(url)

    def parseDeviceListing(self,xmldata):
        """
        :param String xmldata:
        :return: a List of Dicts or None if could not parse
        Parse the xmldata for devices.  Accessing is done by object[index]['tag']
        """
        deviceListing = []
        root = ET.fromstring(xmldata)
        if root.tag == 'list':
            for child in root:
                device = {}
                for sub in child:
                    device[sub.tag]=sub.text
                deviceListing.append(device)
            return deviceListing
        elif root.tag == 'device':
            device = {}
            for child in root:
                device[child.tag]=child.text
            deviceListing.append(device)
            return deviceListing
        return None

    def put(self,url,data):
        data_encoded = urllib.urlencode(data)
        return urllib2.urlopen(url,data_encoded).read()

    def isListXML(self,xmldata):
        root = ET.fromstring(xmldata)
        if root.tag == "list":
            return True
        return False

    def isDeviceXML(self,xmldata):
        root = ET.fromstring(xmldata)
        if root.tag == 'device':
            return True
        return False

    def countDataListXML(self,xmldata):
        self.count = 0
        root = ET.fromstring(xmldata)
        for child in root:
            self.count +=1
        return self.count

class Device(object):

    def __init__(self,attribs=None):
        self.attribs = {}

    def loadAttributesDict(self,dict):
        """
        :param dict of values.  Replaces current attributes.
        :return: None
        """
        self.attribs = dict

    def getAttribute(self,attrib):
        if self.attribs.has_key(attrib):
            return self.attribs.get(attrib)
        else:
            return None

    def setAttribute(self,attrib,value):
        self.attribs[attrib] = value

class Interface(object):

    def __init__(self,device=None,attribs=None):
        self.device = device
        self.attribs = dict(attribs)