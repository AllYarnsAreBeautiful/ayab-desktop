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

from __future__ import annotations
from enum import Enum
from typing import Literal
from PySide6.QtWidgets import QComboBox


class Machine(Enum):
    """Machine configuration class.

    @author Tom Price
    @date   July 2020
    """

    KH910_KH950 = 0
    KH900_KH930_KH940_KH965 = 1
    KH270 = 2

    @property
    # number of needles on machine
    def width(self) -> Literal[112, 200]:
        if self == Machine.KH270:
            # The last needles don't pattern.
            return 112
        else:
            return 200

    @staticmethod
    def add_items(box: QComboBox) -> None:
        """Add items to alignment combo box."""
        box.addItem("KH-910, KH-950i")
        box.addItem("KH-900, KH-930, KH-940, KH-965i")
        box.addItem("KH-270")
