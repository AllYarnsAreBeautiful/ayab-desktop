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

from enum import Enum
from bitarray import bitarray

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QWidget

from .status_gui import Ui_StatusTab


class Direction(Enum):
    Unknown = 0
    Left = 1
    Right = 2

    def reverse(self):
        if self == Direction.Left:
            return Direction.Right
        # else
        if self == Direction.Right:
            return Direction.Left
        # else
        return Direction.Unknown

    @property
    def symbol(self):
        if self == Direction.Left:
            return "\u2190"
        # else
        if self == Direction.Right:
            return "\u2192"
        # else
        return ""

    @property
    def text(self):
        if self == Direction.Left:
            return "Left"
        # else
        if self == Direction.Right:
            return "Right"
        # else
        return ""


class Carriage(Enum):
    Unknown = 0
    Knit = 1
    Lace = 2
    Garter = 3

    @property
    def symbol(self):
        if self == Carriage.Knit:
            return "K"
        elif self == Carriage.Lace:
            return "L"
        elif self == Carriage.Garter:
            return "G"
        else:
            return ""

    @property
    def text(self):
        if self == Carriage.Knit:
            text = "Knit"
        elif self == Carriage.Lace:
            text = "Lace"
        elif self == Carriage.Garter:
            text = "Garter"
        else:
            return ""
        text += " " + QCoreApplication.translate("Progress", "Carriage")
        return text


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
        self.active = True
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
        self.carriage_type = Carriage.Unknown
        self.carriage_position = -1
        self.carriage_direction = Direction.Unknown

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
        self.carriage_direction = status.carriage_direction

    def parse_device_state_API6(self, state, msg):
        if not (self.active):
            return

        # else
        fsm_state = msg[2] # ignored for now, but could be useful in debugging

        hall_l = int((msg[3] << 8) + msg[4])
        hall_r = int((msg[5] << 8) + msg[6])

        if msg[7] == 0:
            carriage_type = Carriage.Knit
        elif msg[7] == 1:
            carriage_type = Carriage.Lace
        elif msg[7] == 2:
            carriage_type = Carriage.Garter
        else:
            carriage_type = Carriage.Unknown

        carriage_position = int(msg[8])

        if msg[9] == 0:
            carriage_direction = Direction.Left
        elif msg[9] == 1:
            carriage_direction = Direction.Right
        else:
            carriage_direction = Direction.Unknown

        self.hall_l = hall_l
        self.hall_r = hall_r
        self.carriage_type = carriage_type
        self.carriage_position = carriage_position
        self.carriage_direction = carriage_direction
        print(carriage_type)
        print(carriage_direction)


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
        self.ui.label_carriage.setText(status.carriage_type.text)
        self.ui.label_direction.setText(status.carriage_direction.text)
