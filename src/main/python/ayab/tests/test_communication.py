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
from ayab.plugins.ayab_plugin.ayab_communication import AyabCommunication
from mock import patch


class TestCommunication(unittest.TestCase):

    def setUp(self):
        self.dummy_serial = serial.serial_for_url("loop://logging=debug",
                                                  timeout=0.1)
        self.comm_dummy = AyabCommunication(self.dummy_serial)

    def test_close_serial(self):
        before = self.dummy_serial.is_open
        assert before
        self.comm_dummy.close_serial()
        after = self.dummy_serial.is_open
        assert after is False

    def test_open_serial(self):
        with patch.object(serial, 'Serial') as mock_method:
            mock_method.return_value = object()
            self.ayabCom = AyabCommunication()
            openStatus = self.ayabCom.open_serial('dummyPortname')
            assert openStatus
            mock_method.assert_called_once_with('dummyPortname', 115200,
                                                timeout=0.1)

        with patch.object(serial, 'Serial') as mock_method:
            with pytest.raises(Exception) as excinfo:
                mock_method.side_effect = serial.SerialException()
                self.ayabCom = AyabCommunication()
                openStatus = self.ayabCom.open_serial('dummyPortname')
            assert "CommunicationException" in str(excinfo.type)
            mock_method.assert_called_once_with('dummyPortname', 115200,
                                                timeout=0.1)

    def test_update(self):
        byte_array = bytearray([0xc0, 0xc1, 0xc0])
        self.dummy_serial.write(byte_array)
        result = self.comm_dummy.update()
        expected_result = bytearray([0xc1])
        assert result == expected_result

    def test_req_start(self):
        start_val, end_val, continuous_reporting = 0, 10, True
        self.comm_dummy.req_start(start_val, end_val, continuous_reporting)
        byte_array = bytearray([0xc0, 0x01,
                                start_val, end_val, continuous_reporting,
                                0xc0])
        bytes_read = self.dummy_serial.read(len(byte_array))
        self.assertEqual(bytes_read, byte_array)

    def test_req_info(self):
        self.comm_dummy.req_info()
        byte_array = bytearray([0xc0, 0x03, 0xc0])
        bytes_read = self.dummy_serial.read(len(byte_array))
        assert bytes_read == byte_array

    def test_req_test(self):
        self.comm_dummy.req_test()
        byte_array = bytearray([0xc0, 0x04, 0xc0])
        bytes_read = self.dummy_serial.read(len(byte_array))
        assert bytes_read == byte_array

    def test_cnf_line(self):
        lineNumber = 13
        lineData = [0x23, 0x24]
        flags = 0x12
        crc8 = 0x57
        self.comm_dummy.cnf_line(lineNumber, lineData, flags, crc8)
        byte_array = bytearray([0xc0, 0x42])
        byte_array.append(lineNumber)
        byte_array.extend(lineData)
        byte_array.append(flags)
        byte_array.append(crc8)
        byte_array.append(0xc0)
        bytes_read = self.dummy_serial.read(len(byte_array))
        assert bytes_read == byte_array
