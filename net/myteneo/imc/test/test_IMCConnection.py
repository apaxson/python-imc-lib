#!/usr/bin/python
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

import unittest
from net.myteneo.imc.lib.IMCConnection import IMCConnection
from net.myteneo.imc.test.test_xml_devData import IMCTestDeviceData

class TestIMCConnection(unittest.TestCase):

    def setUp(self):
        # Setup a connection to IMC Web Services
        unittest.TestCase.setUp(self)
        host = "10.200.0.95"
        port = "8080"
        username = "admin"
        passwd = "admin"
        self.imc_conn = IMCConnection(host,port,username,passwd)

        # Load test XML Data
        self.testDeviceListing = IMCTestDeviceData.DEVICELIST
        self.testDeviceDataManaged = IMCTestDeviceData.deviceManaged
        self.testDeviceDataUnmanaged = IMCTestDeviceData.deviceUnManaged
        self.testDeviceDataManagedList = IMCTestDeviceData.deviceUnManagedList

    def test_IMCConnection(self):
        # Make a call to IMC web services and make sure we are authorized
        data = self.imc_conn.get("http://10.200.0.95:8080/imcrs")
        self.assertEqual(data.getcode(),200)

    def test_countDataList(self):
        count = self.imc_conn.countDataList(self.testDeviceListing)
        self.assertEqual(count,6)

    def test_isList(self):
        self.assertTrue(self.imc_conn.isList(self.testDeviceListing))
        self.assertFalse(self.imc_conn.isList(self.testDeviceDataUnmanaged))

    def test_parseDeviceListing(self):
        deviceListing = self.imc_conn.parseDeviceListing(self.testDeviceListing)
        device = self.imc_conn.parseDeviceListing(self.testDeviceDataManaged)
        self.assertEqual(len(deviceListing),6)
        self.assertEqual(deviceListing[0]['id'],'6')
        self.assertEqual(deviceListing[5]['id'],'1014')

    if __name__ == '__main__':
        unittest.main()
