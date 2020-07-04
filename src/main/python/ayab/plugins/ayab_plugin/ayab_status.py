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
#    Copyright 2014 Sebastian Oliva, Christian Obersteiner, Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

from PyQt5.QtCore import QCoreApplication
from bitarray import bitarray


class Status(object):
    """Data object to update the status tab and knit progress window.

    @author Tom Price
    @date   June 2020
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_row = -1
        self.line_number = -1
        self.total_rows = -1
        self.repeats = -1
        self.color_symbol = ""
        self.hall_l = 0
        self.hall_r = 0
        self.carriage_type = ""
        self.carriage_position = 0
        self.color = -1
        self.alt_color = None
        self.bits = bitarray()

    def get_carriage_info(self, msg):
        hall_l = int((msg[2] << 8) + msg[3])
        hall_r = int((msg[4] << 8) + msg[5])

        if msg[6] == 1:
            carriage_type = "K "
        elif msg[6] == 2:
            carriage_type = "L "
        elif msg[6] == 3:
            carriage_type = "G "
        else:
            carriage_type = ""
        if carriage_type != "":
            carriage_type += QCoreApplication.translate("Progress", "Carriage")

        carriage_position = int(msg[7])

        self.hall_l = hall_l
        self.hall_r = hall_r
        self.carriage_type = carriage_type
        self.carriage_position = carriage_position
