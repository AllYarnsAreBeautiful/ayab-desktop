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

import unittest

from ..engine.status import Status, Carriage, Direction


class TestStatus(unittest.TestCase):
    def setUp(self):
        # no setup
        pass

    def test_parse_device_state_API6(self):
        p = Status()
        p.active = True
        msg = bytes([0, 99, 1, 2, 3, 4, 5, 0, 7, 1])
        p.parse_device_state_API6(1, msg)
        assert p.hall_l == 0x203
        assert p.hall_r == 0x405
        assert p.carriage_type == Carriage.Knit
        assert p.carriage_position == 7
        assert p.carriage_direction == Direction.Right
