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
#    Copyright 2013 Christian Obersteiner, Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

# from PyQt5.QtCore import QCoreApplication


class Machine(object):
    """Machine configuration class.

    @author Tom Price
    @date   July 2020
    """
    WIDTH = 200

    def add_items(box):
        """Add items to alignment combo box."""
        box.addItem("KH-910, KH-950i")
        box.addItem("KH-900, KH-930, KH-940, KH-965i")
        box.addItem("KH-270")
