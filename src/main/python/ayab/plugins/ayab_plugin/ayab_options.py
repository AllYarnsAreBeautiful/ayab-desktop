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
from PyQt5.QtWidgets import QCheckBox, QSpinBox, QComboBox, QTabWidget, QLineEdit


class Options (object):
    """Class for configuration options."""

    def __init__(self):
        # FIXME: Initialize from default settings
        self.__continuousReporting = False
        self.__num_colors = 2
        self.__start_row = 0
        self.__start_needle = 0 
        self.__stop_needle = 0  # Machine.MACHINE_WIDTH - 1
        self.__alignment = "CENTER"
        self.__inf_repeat = False
        self.__auto_mirror = False
        self.__knitting_mode = 0
        self.__portname = ""
        self.__filename = ""

    def get_configuration_from_ui(self, ui):
        """Get configuration options from the UI elements."""
        self.__continuousReporting = ui.findChild(
            QCheckBox, "checkBox_ContinuousReporting").isChecked()

        color_line_text = ui.findChild(QSpinBox, "color_edit").value()
        self.__num_colors = int(color_line_text)

        # Internally, we start counting from zero
        # (for easier handling of arrays)
        start_row_text = ui.findChild(QSpinBox, "start_row_edit").value()
        self.__start_row = int(start_row_text) - 1

        start_needle_color = ui.findChild(QComboBox, "start_needle_color").currentIndex()
        start_needle_text = ui.findChild(QSpinBox, "start_needle_edit").value()
        self.__start_needle = NeedleColor(start_needle_color).read_settings(start_needle_text)

        stop_needle_color = ui.findChild(QComboBox, "stop_needle_color").currentIndex()
        stop_needle_text = ui.findChild(QSpinBox, "stop_needle_edit").value()
        self.__stop_needle = NeedleColor(stop_needle_color).read_settings(stop_needle_text)

        alignment_index = ui.findChild(QComboBox, "alignment_combo_box").currentIndex()
        self.__alignment = Alignment(alignment_index).name

        self.__inf_repeat = int(ui.findChild(QCheckBox, "infRepeat_checkbox").isChecked())
        self.__auto_mirror = int(ui.findChild(QCheckBox, "autoMirror_checkbox").isChecked())
        self.__knitting_mode = ui.findChild(QComboBox, "knitting_mode_box").currentIndex()
        self.__portname = str(ui.findChild(QComboBox, "serial_port_dropdown").currentText())
        self.__filename = str(ui.findChild(QLineEdit, "filename_lineedit").text())

    def validate_configuration(self):
        if self.__start_needle and self.__stop_needle:
            if self.__start_needle > self.__stop_needle:
                return False, "Invalid needle start and end."

        if self.__portname == '':
            return False, "Please choose a valid port."

        if self.__knitting_mode == KnittingMode.SINGLEBED.value \
                and self.__num_colors >= 3:
            return False, "Singlebed knitting currently supports only 2 colors."

        if self.__knitting_mode == KnittingMode.CIRCULAR_RIBBER.value \
                and self.__num_colors >= 3:
            return False, "Circular knitting supports only 2 colors."

        return True, None

    # getter methods
    def get_continuousReporting(self): return self.__continuousReporting
    def get_num_colors(self): return self.__num_colors
    def get_start_row(self): return self.__start_row
    def get_start_needle(self): return self.__start_needle
    def get_stop_needle(self): return self.__stop_needle
    def get_alignment(self): return self.__alignment
    def get_inf_repeat(self): return self.__inf_repeat
    def get_auto_mirror(self): return self.__auto_mirror
    def get_knitting_mode(self): return self.__knitting_mode
    def get_portname(self): return self.__portname
    def get_filename(self): return self.__filename


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

    MACHINE_WIDTH = 200

    def addItems(box):
        box.addItem(QCoreApplication.translate("NeedleColor", "orange"))
        box.addItem(QCoreApplication.translate("NeedleColor", "green"))

    def read_settings(self, needle):
        '''Reads the Needle Settings UI Elements and normalizes'''
        if self.name == "ORANGE":
            return self.MACHINE_WIDTH.value // 2 - int(needle)
        elif self.name == "GREEN":
            return self.MACHINE_WIDTH.value // 2 - 1 + int(needle)
