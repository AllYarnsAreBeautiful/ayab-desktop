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

from enum import Enum, auto
from bitarray import bitarray

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QWidget

from .status_gui import Ui_StatusTab


class Direction(Enum):
    UNKNOWN = auto()
    LEFT_TO_RIGHT = auto()
    RIGHT_TO_LEFT = auto()

    @property
    def symbol(self):
        if self == Direction.LEFT_TO_RIGHT:
            return "\u2192 "
        # else
        if self == Direction.RIGHT_TO_LEFT:
            return "\u2190 "
        # else
        return "  "

    @property
    def text(self):
        if self == Direction.LEFT_TO_RIGHT:
            return "Left to Right"
        # else
        if self == Direction.RIGHT_TO_LEFT:
            return "Right to Left"
        # else
        return ""


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
        self.mirror = False
        # carriage info
        self.hall_l = 0
        self.hall_r = 0
        self.carriage_type = ""
        self.carriage_position = 0
        self.direction = Direction.UNKNOWN

    def copy(self, status):
        self.active = status.active
        self.current_row = status.current_row
        self.line_number = status.line_number
        self.repeats = status.repeats
        self.color_symbol = status.color_symbol
        self.color = status.color
        self.alt_color = status.alt_color
        self.bits = status.bits
        self.hall_l = status.hall_l
        self.hall_r = status.hall_r
        self.carriage_type = status.carriage_type
        self.carriage_position = status.carriage_position
        self.direction = status.direction

    def parse_device_state_API6(self, state, msg):
        if not (self.active):
            return

        # else
        # TODO: if state != 1 report error and return

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

        # TODO: get carriage direction


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
        self.ui = Ui_StatusTab()
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
        self.ui.label_direction.setText(status.direction.text)
