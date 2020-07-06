# -*- coding: utf-8 -*-
# This file is part of AYAB.
#
#    AYAB is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AYAB is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with AYAB.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2014 Sebastian Oliva, Christian Obersteiner,
#    Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

import unittest
from ayab.plugins.ayab_plugin.ayab_communication import MessageToken
from ayab.plugins.ayab_plugin.ayab_communication_mockup \
    import AyabCommunicationMockup


class TestAyabCommunicationMockup(unittest.TestCase):
    def setUp(self):
        self.comm_dummy = AyabCommunicationMockup()

    def test_close_serial(self):
        self.comm_dummy.close_serial()
        assert self.comm_dummy.is_open() is False

    def test_open_serial(self):
        assert self.comm_dummy.is_open() is False
        self.comm_dummy.open_serial()
        assert self.comm_dummy.is_open()

    def test_update(self):
        assert self.comm_dummy.update() == (None, MessageToken.none, 0)

    def test_req_start(self):
        start_val, end_val, continuous_reporting = 0, 10, True
        expected_result = (b'\xc1\x01', MessageToken.cnfStart, 1)
        self.comm_dummy.req_start(start_val, end_val, continuous_reporting)
        bytes_read = self.comm_dummy.update()
        assert bytes_read == expected_result

    def test_req_info(self):
        expected_result = (b'\xc3\x05\xff\xff', MessageToken.cnfInfo, 5)
        self.comm_dummy.req_info()
        bytes_read = self.comm_dummy.update()
        assert bytes_read == expected_result

        # indState shall be sent automatically, also
        expected_result = (b'\x84\x01\xff\xff\xff\xff\x01\x7f',
                           MessageToken.indState, 1)
        bytes_read = self.comm_dummy.update()
        assert bytes_read == expected_result

    def test_req_test(self):
        expected_result = (b'\xc4\x01', MessageToken.cnfTest, 1)
        self.comm_dummy.req_test()
        bytes_read = self.comm_dummy.update()
        assert bytes_read == expected_result

    def test_cnf_line(self):
        lineNumber = 13
        lineData = [0x23, 0x24]
        flags = 0x12
        crc8 = 0x57
        assert self.comm_dummy.cnf_line(lineNumber, lineData, flags)

    def test_req_line(self):
        self.comm_dummy.open_serial()
        start_val, end_val, continuous_reporting = 0, 10, True
        self.comm_dummy.req_start(start_val, end_val, continuous_reporting)
        self.comm_dummy.update()  # cnfStart

        for i in range(0, 31):  # 256):  # too slow to test every single byte
            bytes_read = self.comm_dummy.update()
            assert bytes_read == (bytearray([0x82,
                                             i]), MessageToken.reqLine, i)
