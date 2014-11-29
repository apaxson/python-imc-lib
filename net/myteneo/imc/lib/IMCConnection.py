# (c) 2014, Aaron Paxson <aj@thepaxson5.org>
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

    def isList(self,xmldata):
        root = ET.fromstring(xmldata)
        if root.tag == "list":
            return True
        return False

    def isDevice(self,xmldata):
        root = ET.fromstring(xmldata)
        if root.tag == 'device':
            return True
        return False

    def countDataList(self,xmldata):
        self.count = 0
        root = ET.fromstring(xmldata)
        for child in root:
            self.count = self.count+1
        return self.count


