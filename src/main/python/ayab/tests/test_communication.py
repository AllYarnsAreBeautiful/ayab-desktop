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

import pytest
import serial
import unittest
from mock import patch

from ..engine.communication import Communication, Token


class TestCommunication(unittest.TestCase):
    def setUp(self):
        self.dummy_serial = serial.serial_for_url("loop://logging=debug", timeout=0.1)
        self.comm_dummy = Communication(self.dummy_serial)

    def test_close_serial(self):
        before = self.dummy_serial.is_open
        assert before
        self.comm_dummy.close_serial()
        after = self.dummy_serial.is_open
        assert after is False

    def test_open_serial(self):
        with patch.object(serial, "Serial") as mock_method:
            self.ayabCom = Communication()
            openStatus = self.ayabCom.open_serial("dummyPortname")
            assert openStatus
            mock_method.assert_called_once_with("dummyPortname", 115200, timeout=0.1)

        with patch.object(serial, "Serial") as mock_method:
            with pytest.raises(Exception) as excinfo:
                mock_method.side_effect = serial.SerialException()
                self.ayabCom = Communication()
                openStatus = self.ayabCom.open_serial("dummyPortname")
            assert "CommunicationException" in str(excinfo.type)
            mock_method.assert_called_once_with("dummyPortname", 115200, timeout=0.1)

    def test_update_API6(self):
        byte_array = bytearray([0xC0, Token.cnfStart.value, 1, 0xC0])
        self.dummy_serial.write(byte_array)
        result = self.comm_dummy.update_API6()
        expected_result = (bytes([Token.cnfStart.value, 1]), Token.cnfStart, 1)
        assert result == expected_result

    def test_req_start_API6(self):
        start_val, end_val, continuous_reporting, disable_hardware_beep, crc8 = (
            0,
            10,
            True,
            False,
            0x8A,
        )
        self.comm_dummy.req_start_API6(
            start_val, end_val, continuous_reporting, disable_hardware_beep
        )
        byte_array = bytearray(
            [
                Token.slipFrameEnd.value,
                Token.reqStart.value,
                start_val,
                end_val,
                1 * continuous_reporting + 2 * (not disable_hardware_beep),
                crc8,
                Token.slipFrameEnd.value,
            ]
        )
        bytes_read = self.dummy_serial.read(len(byte_array))
        self.assertEqual(bytes_read, byte_array)

    def test_req_info(self):
        self.comm_dummy.req_info()
        byte_array = bytearray(
            [Token.slipFrameEnd.value, Token.reqInfo.value, Token.slipFrameEnd.value]
        )
        bytes_read = self.dummy_serial.read(len(byte_array))
        assert bytes_read == byte_array

    def test_req_test_API6(self):
        self.comm_dummy.req_test_API6()
        byte_array = bytearray(
            [Token.slipFrameEnd.value, Token.reqTest.value, Token.slipFrameEnd.value]
        )
        bytes_read = self.dummy_serial.read(len(byte_array))
        assert bytes_read == byte_array

    def test_cnf_line_API6(self):
        line_number = 0
        color = 0
        flags = 1
        line_data = b"\xde\xad\xbe\xef\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
        crc8 = 0xA7
        self.comm_dummy.cnf_line_API6(line_number, color, flags, line_data)
        byte_array = bytearray(
            [Token.slipFrameEnd.value, Token.cnfLine.value, line_number, color, flags]
        )
        byte_array.extend(line_data)
        byte_array.extend(bytes([crc8, Token.slipFrameEnd.value]))
        bytes_read = self.dummy_serial.read(len(byte_array))
        assert bytes_read == byte_array
