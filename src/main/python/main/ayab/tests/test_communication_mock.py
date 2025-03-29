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

from ..engine.communication import Token
from ..engine.communication_mock import CommunicationMock
from ..machine import Machine


class TestCommunicationMock(unittest.TestCase):
    def setUp(self):
        self.comm_dummy = CommunicationMock(delay=False)

    def test_close_serial(self):
        self.comm_dummy.close_serial()
        assert self.comm_dummy.is_open() is False

    def test_open_serial(self):
        assert self.comm_dummy.is_open() is False
        self.comm_dummy.open_serial()
        assert self.comm_dummy.is_open()

    def test_update_API6(self):
        assert self.comm_dummy.update_API6() == (None, Token.none, 0)

    def test_req_start_API6(self):
        start_val, end_val, continuous_reporting, disable_hardware_beep = (
            0,
            10,
            True,
            False,
        )
        expected_result = (bytes([Token.cnfStart.value, 0]), Token.cnfStart, 0)
        self.comm_dummy.req_start_API6(
            start_val, end_val, continuous_reporting, disable_hardware_beep
        )
        bytes_read = self.comm_dummy.update_API6()
        assert bytes_read == expected_result

    def test_req_info(self):
        # expecting 1.0.0-mock
        expected_result = (
            bytes([Token.cnfInfo.value, 6, 1, 0, 0, 109, 111, 99, 107, 0]),
            Token.cnfInfo,
            6,
        )
        self.comm_dummy.req_info()
        bytes_read = self.comm_dummy.update_API6()
        assert bytes_read == expected_result

    def test_req_init_API6(self):
        expected_result = (bytes([Token.cnfInit.value, 0]), Token.cnfInit, 0)
        self.comm_dummy.req_init_API6(Machine.KH910_KH950)
        bytes_read = self.comm_dummy.update_API6()
        assert bytes_read == expected_result
        # indState shall be sent automatically, also
        expected_result = (
            bytes([Token.indState.value, 0, 1, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0, 1]),
            Token.indState,
            0,
        )
        bytes_read = self.comm_dummy.update_API6()
        assert bytes_read == expected_result

    def test_req_test_API6(self):
        expected_result = (bytes([Token.cnfTest.value, 0]), Token.cnfTest, 0)
        self.comm_dummy.req_test_API6()
        bytes_read = self.comm_dummy.update_API6()
        assert bytes_read == expected_result

    def test_cnf_line_API6(self):
        lineNumber = 13
        color = 0
        flags = 0x12
        lineData = [0x23, 0x24]
        # crc8 = 0x24
        assert self.comm_dummy.cnf_line_API6(lineNumber, color, flags, lineData)

    def test_req_line_API6(self):
        self.comm_dummy.open_serial()
        start_val, end_val, continuous_reporting, disable_hardware_beep = (
            0,
            10,
            True,
            False,
        )
        self.comm_dummy.req_start_API6(
            start_val, end_val, continuous_reporting, disable_hardware_beep
        )
        self.comm_dummy.update_API6()  # cnfStart

        # Alternates between requesting a line and no output
        for i in range(0, 256):
            bytes_read = self.comm_dummy.update_API6()
            assert bytes_read == (bytearray([Token.reqLine.value, i]), Token.reqLine, i)
            bytes_read = self.comm_dummy.update_API6()
            assert bytes_read == (None, Token.none, 0)
