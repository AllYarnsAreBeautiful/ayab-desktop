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
        assert self.comm_dummy.update() is None

    def test_req_start(self):
        expected_result = bytearray([0xC1, 0x1])

        self.comm_dummy.req_start()

        bytes_read = self.comm_dummy.update()
        assert bytes_read == expected_result

    def test_req_info(self):
        expected_result = bytearray([0xC3, 5, 0xFF, 0xFF])

        self.comm_dummy.req_info()

        bytes_read = self.comm_dummy.update()
        assert bytes_read == expected_result

    def test_req_test(self):
        expected_result = bytearray([0xC4, 0x1])

        self.comm_dummy.req_test()

        bytes_read = self.comm_dummy.update()
        assert bytes_read == expected_result

    def test_cnf_line(self):
        lineNumber = 13
        lineData = [0x23, 0x24]
        flags = 0x12
        crc8 = 0x57
        assert self.comm_dummy.cnf_line(lineNumber, lineData, flags, crc8)

    def test_req_line(self):
        self.comm_dummy.open_serial()
        bytes_read = self.comm_dummy.update()
        assert bytes_read == bytearray([0x82, 0])
        bytes_read = self.comm_dummy.update()
        assert bytes_read == bytearray([0x82, 1])
