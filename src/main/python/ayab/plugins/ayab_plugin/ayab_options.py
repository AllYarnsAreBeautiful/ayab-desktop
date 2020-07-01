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
from PyQt5.QtCore import QCoreApplication
from .machine import Machine


class Options (object):
    """Class for configuration options."""

    def __init__(self):
        # FIXME: Initialize from default settings
        self.portname = ""
        self.knitting_mode = KnittingMode(0)
        self.num_colors = 2
        self.start_row = 0
        self.inf_repeat = False
        self.start_needle = 0 
        self.stop_needle = Machine.WIDTH - 1
        self.alignment = Alignment(0)
        self.auto_mirror = False
        self.continuous_reporting = False

    def as_dict(self):
        return dict([
            ("portname", self.portname),
            ("knitting_mode", self.knitting_mode),
            ("num_colors", self.num_colors),
            ("start_row", self.start_row),
            ("inf_repeat", self.inf_repeat),
            ("start_needle", self.start_needle),
            ("stop_needle", self.stop_needle),
            ("alignment", self.alignment),
            ("auto_mirror", self.auto_mirror),
            ("continuous_reporting", self.continuous_reporting)])

    def read(self, ui):
        """Get configuration options from the UI elements."""
        self.portname = ui.serial_port_dropdown.currentText()
        self.knitting_mode = KnittingMode(ui.knitting_mode_box.currentIndex())
        self.num_colors = int(ui.color_edit.value())
        self.start_row = int(ui.start_row_edit.value()) - 1
        self.start_needle = NeedleColor.read_start_needle(ui)
        self.stop_needle = NeedleColor.read_stop_needle(ui)
        self.alignment = Alignment(ui.alignment_combo_box.currentIndex())
        self.inf_repeat = ui.infRepeat_checkbox.isChecked()
        self.auto_mirror = ui.autoMirror_checkbox.isChecked()
        self.continuous_reporting = ui.checkBox_ContinuousReporting.isChecked()

    def validate_configuration(self):
        if self.start_needle and self.stop_needle:
            if self.start_needle > self.stop_needle:
                return False, "Invalid needle start and end."

        if self.portname == '':
            return False, "Please choose a valid port."

        if self.knitting_mode == KnittingMode.SINGLEBED \
                and self.num_colors >= 3:
            return False, "Singlebed knitting currently supports only 2 colors."

        if self.knitting_mode == KnittingMode.CIRCULAR_RIBBER \
                and self.num_colors >= 3:
            return False, "Circular knitting supports only 2 colors."

        return True, None


class KnittingMode(Enum):
    SINGLEBED = 0
    CLASSIC_RIBBER = 1
    MIDDLECOLORSTWICE_RIBBER = 2
    HEARTOFPLUTO_RIBBER = 3
    CIRCULAR_RIBBER = 4

    def row_multiplier(self, ncolors):
        if self.name == "SINGLEBED":
            return 1
        if (self.name == "CLASSIC_RIBBER" and ncolors > 2) \
            or self.name == "CIRCULAR_RIBBER":
                # every second line is blank
                return 2 * ncolors
        if self.name == "MIDDLECOLORSTWICE_RIBBER" \
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

    def read(self, needle):
        '''Reads the Needle Settings UI Elements and normalizes'''
        if self.name == "ORANGE":
            return Machine.WIDTH // 2 - int(needle)
        elif self.name == "GREEN":
            return Machine.WIDTH // 2 - 1 + int(needle)

    def read_start_needle(ui):
        start_needle_color = NeedleColor(ui.start_needle_color.currentIndex())
        start_needle_text = ui.start_needle_edit.value()
        return start_needle_color.read(start_needle_text)

    def read_stop_needle(ui):
        stop_needle_color = NeedleColor(ui.stop_needle_color.currentIndex())
        stop_needle_text = ui.stop_needle_edit.value()
        return stop_needle_color.read(stop_needle_text)
