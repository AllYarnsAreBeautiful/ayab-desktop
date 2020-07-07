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
#    Copyright 2013-2020 Sebastian Oliva, Christian Obersteiner,
#    Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop
"""
Functions for selecting USB port.

@author Tom Price
@date   July 2020
"""

import serial.tools.list_ports


def populate_ports(combo_box=None, port_list=None):
    if not port_list:
        port_list = get_serial_ports()
    combo_box.clear()
    populate(combo_box, port_list)


def populate(combo_box, port_list):
    for item in port_list:
        # TODO: should display the info of the device.
        combo_box.addItem(item[0])


def get_serial_ports():
    """Returns a list of all USB serial ports"""
    return list(serial.tools.list_ports.grep("USB"))
