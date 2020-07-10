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
from PyQt5.QtCore import QCoreApplication, QSettings
from .ayab_knit_mode import KnitMode
from .machine import Machine


class Options(object):
    """Class for configuration options."""
    def __init__(self, prefs):
        self.prefs = prefs
        self.reset()

    def reset(self):
        """Reset configuration options to default prefs."""
        self.portname = ""
        self.machine = self.prefs.value("machine")
        self.knitting_mode = self.prefs.value("default_knitting_mode")
        self.num_colors = 2
        self.start_row = 0
        self.inf_repeat = self.prefs.value("default_infinite_repeat")
        self.start_needle = 0
        self.stop_needle = Machine.WIDTH - 1
        self.alignment = self.prefs.value("default_alignment")
        self.auto_mirror = self.prefs.value("default_mirroring")
        self.continuous_reporting = False

    def as_dict(self):
        return dict([("portname", self.portname), ("machine", self.machine),
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
        self.machine = self.prefs.value("machine")
        self.knit_mode = KnitMode(ui.knitting_mode_box.currentIndex())
        self.num_colors = int(ui.color_edit.value())
        self.start_row = self.read_start_row(ui)
        self.inf_repeat = ui.inf_repeat_checkbox.isChecked()
        self.start_needle = NeedleColor.read_start_needle(ui)
        self.stop_needle = NeedleColor.read_stop_needle(ui)
        self.alignment = self.read_alignment(ui)
        self.auto_mirror = ui.auto_mirror_checkbox.isChecked()
        self.continuous_reporting = ui.continuous_reporting_checkbox.isChecked(
        )

    def read_start_row(self, ui):
        return int(ui.start_row_edit.value()) - 1

    def read_alignment(self, ui):
        return Alignment(ui.alignment_combo_box.currentIndex())

    def validate(self):
        """Validate configuration options."""
        if self.start_needle and self.stop_needle:
            if self.start_needle > self.stop_needle:
                return False, "Invalid needle start and end."
        # else
        if self.portname == '':
            return False, "Please choose a valid port."
        # else
        if self.knit_mode == KnitMode.SINGLEBED \
                and self.num_colors >= 3:
            return False, "Singlebed knitting currently supports only 2 colors."
        # else
        if self.knit_mode == KnitMode.CIRCULAR_RIBBER \
                and self.num_colors >= 3:
            return False, "Circular knitting supports only 2 colors."
        # else
        return True, None


class Alignment(Enum):
    CENTER = 0
    LEFT = 1
    RIGHT = 2

    def add_items(box):
        """Add items to alignment combo box."""
        box.addItem(QCoreApplication.translate("Alignment", "Center"))
        box.addItem(QCoreApplication.translate("Alignment", "Left"))
        box.addItem(QCoreApplication.translate("Alignment", "Right"))


class NeedleColor(Enum):
    ORANGE = 0
    GREEN = 1

    def add_items(box):
        """Add items to needle color combo box."""
        box.addItem(QCoreApplication.translate("NeedleColor", "orange"))
        box.addItem(QCoreApplication.translate("NeedleColor", "green"))

    def read(self, needle):
        if self == NeedleColor.ORANGE:
            return Machine.WIDTH // 2 - int(needle)
        elif self == NeedleColor.GREEN:
            return Machine.WIDTH // 2 - 1 + int(needle)

    def read_start_needle(ui):
        '''Read the start needle prefs from UI and normalize'''
        start_needle_col = NeedleColor(ui.start_needle_color.currentIndex())
        start_needle_text = ui.start_needle_edit.value()
        return start_needle_col.read(start_needle_text)

    def read_stop_needle(ui):
        '''Read the stop needle prefs from UI and normalize'''
        stop_needle_col = NeedleColor(ui.stop_needle_color.currentIndex())
        stop_needle_text = ui.stop_needle_edit.value()
        return stop_needle_col.read(stop_needle_text)
