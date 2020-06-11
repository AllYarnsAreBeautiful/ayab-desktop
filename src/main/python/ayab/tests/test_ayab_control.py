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
#    Copyright 2020 Sebastian Oliva, Christian Obersteiner,
#    Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

import pytest
import unittest
from ayab.plugins.ayab_plugin.ayab_control import AYABControl


class TestAYABControl(unittest.TestCase):
    def setUp(self):
        pass

    def test_set_bit(self):
        ayab_control = AYABControl()
        assert ayab_control._set_bit(0, 0) == 1
        assert ayab_control._set_bit(1, 0) == 1
        assert ayab_control._set_bit(0, 1) == 2
        assert ayab_control._set_bit(0, 8) == 256
        assert ayab_control._set_bit(0, 16) == 65536

        with pytest.raises(ValueError):
            ayab_control._set_bit(0, -1)
        with pytest.raises(ValueError):
            ayab_control._set_bit(-1, 0)

    def test_set_pixel(self):
        ayab_control = AYABControl()

        line = bytearray([0, 0, 0])
        expected_line = bytearray([1, 0, 0])
        ayab_control._set_pixel(line, 0)
        assert line == expected_line

        line = bytearray([0, 0, 0])
        expected_line = bytearray([0, 0, 0x80])
        ayab_control._set_pixel(line, 23)
        assert line == expected_line

        line = bytearray([0, 0, 0])
        with pytest.raises(IndexError):
            ayab_control._set_pixel(line, 24)
