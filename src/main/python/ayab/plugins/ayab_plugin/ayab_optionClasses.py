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

from enum import Enum
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
from .machine import Machine


class KnittingMode(Enum):
    SINGLEBED = 0
    CLASSIC_RIBBER = 1
    MIDDLECOLORSTWICE_RIBBER = 2
    HEARTOFPLUTO_RIBBER = 3
    CIRCULAR_RIBBER = 4

    def row_multiplier(self, ncolors):
        if self.name == "SINGLEBED":
            return 1
        elif (self.name == "CLASSIC_RIBBER" and ncolors > 2) \
            or self.name == "CIRCULAR_RIBBER":
            # every second line is blank
            return 2 * ncolors
        elif self.name == "MIDDLECOLORSTWICE_RIBBER" \
            or self.name == "HEARTOFPLUTO_RIBBER":
            # only middle lines doubled
            return 2 * ncolors - 2
        else:
            # one line per color
            return ncolors

    def good_ncolors(self, ncolors):
        if self.name == "SINGLEBED" or self.name == "CIRCULAR_RIBBER":
            return ncolors == 2
        else:
            # no maximum
            return ncolors >= 2

    def knit_func(self, ncolors):
        method = "_" + self.name.lower()
        if self.name == "CLASSIC_RIBBER":
            method += ["_2col", "_multicol"][ncolors > 2]
        return method

    # FIXME this function is supposed to select needles
    # to knit the background color along side the image pattern
    def flanking_needles(self, color, ncolors):
        # return (color == 0 and self.name == "CLASSIC_RIBBER") \
        #     or (color == ncolors - 1
        #         and (self.name == "MIDDLECOLORSTWICE_RIBBER"
        #             or self.name == "HEARTOFPLUTO_RIBBER"))
        return color == 0 and self.name != "CIRCULAR_RIBBER"

    def addItems(box):
        box.addItem(QCoreApplication.translate("KnittingMode",
            "Singlebed"))
        box.addItem(QCoreApplication.translate("KnittingMode",
            "Ribber: Classic"))
        box.addItem(QCoreApplication.translate("KnittingMode",
            "Ribber: Middle-Colors-Twice"))
        box.addItem(QCoreApplication.translate("KnittingMode",
            "Ribber: Heart of Pluto"))
        box.addItem(QCoreApplication.translate("KnittingMode",
            "Ribber: Circular"))


class Alignment(Enum):
    CENTER = 0
    LEFT = 1
    RIGHT = 2

    def addItems(box):
        box.addItem(QCoreApplication.translate("Alignment", "Center"))
        box.addItem(QCoreApplication.translate("Alignment", "Left"))
        box.addItem(QCoreApplication.translate("Alignment", "Right"))


class NeedleColor(Enum):
    ORANGE = 0
    GREEN = 1

    def addItems(box):
        box.addItem(QCoreApplication.translate("NeedleColor", "orange"))
        box.addItem(QCoreApplication.translate("NeedleColor", "green"))

    def read_needle_settings(self, needle):
        '''Reads the Needle Settings UI Elements and normalizes'''
        if self.name == "ORANGE":
            return Machine.MACHINE_WIDTH // 2 - int(needle)
        elif self.name == "GREEN":
            return Machine.MACHINE_WIDTH // 2 - 1 + int(needle)
