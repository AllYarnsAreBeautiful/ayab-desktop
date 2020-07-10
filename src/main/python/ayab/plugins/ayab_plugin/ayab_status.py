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

from bitarray import bitarray
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QWidget
from .ayab_status_gui import Ui_StatusWidget


class Status(object):
    """
    Data object for updating the status tab, progress bar, and knit progress window.

    @author Tom Price
    @date   July 2020
    """
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.active = False
        # data fields
        self.current_row = -1
        self.line_number = -1
        self.total_rows = -1
        self.repeats = -1
        self.color_symbol = ""
        self.color = -1
        self.alt_color = None
        self.bits = bitarray()
        # carriage info
        self.hall_l = 0
        self.hall_r = 0
        self.carriage_type = ""
        self.carriage_position = 0

    def copy(self, status):
        self.active = status.active
        self.current_row = status.current_row
        self.line_number = status.line_number
        self.total_rows = status.total_rows
        self.repeats = status.repeats
        self.color_symbol = status.color_symbol
        self.color = status.color
        self.alt_color = status.alt_color
        self.bits = status.bits
        self.hall_l = status.hall_l
        self.hall_r = status.hall_r
        self.carriage_type = status.carriage_type
        self.carriage_position = status.carriage_position

    def parse_carriage_info(self, msg):
        if not (self.active):
            return

        # else
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


# FIXME translations for UI
class StatusTab(Status, QWidget):
    """
    Class for the status tab of the dock widget, implemented as a subclass
    of `QWidget`.

    @author Tom Price
    @date   July 2020
    """
    def __init__(self):
        super().__init__()
        self.ui = Ui_StatusWidget()
        self.ui.setupUi(self)

    def refresh(self):
        pass  # TODO

    def write_carriage_info(self, status):
        if not (self.active):
            return
        # else
        self.ui.progress_hall_l.setValue(status.hall_l)
        self.ui.label_hall_l.setText(str(status.hall_l))
        self.ui.progress_hall_r.setValue(status.hall_r)
        self.ui.label_hall_r.setText(str(status.hall_r))
        self.ui.slider_position.setValue(status.carriage_position)
        self.ui.label_carriage.setText(status.carriage_type)
