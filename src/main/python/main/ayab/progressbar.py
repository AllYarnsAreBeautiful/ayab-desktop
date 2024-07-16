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
#    Copyright 2014 Sebastian Oliva, Christian Obersteiner,
#       Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

from __future__ import annotations
from typing import TYPE_CHECKING
from PySide6.QtGui import QColor

if TYPE_CHECKING:
    from .ayab import GuiMain
    from .engine.status import Status


class ProgressBar(object):
    """Methods for the progress bar."""

    def __init__(self, parent: GuiMain):
        self.__row_label = parent.ui.label_current_row
        self.__color_label = parent.ui.label_current_color
        self.__status_label = parent.engine.status.ui.label_progress
        self.__selection_label = parent.ui.label_selection
        self.reset()

    def reset(self) -> None:
        self.row = -1
        self.total = -1
        self.repeats = -1
        self.color = ""
        self.background_color = 0xFFFFFF
        self.__row_label.setText("")
        self.__color_label.setText("")
        self.__status_label.setText("")
        self.__selection_label.setText("")

    def update(
        self,
        status: Status
    ) -> bool:
        if status.current_row < 0:
            return False
        self.row = status.current_row
        self.total = status.total_rows
        self.repeats = status.repeats
        self.color = status.color_symbol
        self.background_color = status.color
        self.refresh()
        return True

    def setSelectionLabel(self, text: str) -> None:
        self.__selection_label.setText(text)

    def refresh(self) -> None:
        """Updates the color and row in progress bar"""
        if self.row < 0 or self.total < 0:
            return

        if self.color == "":
            color_text = ""
        else:
            color_text = "Color " + self.color
            bg_color = QColor.fromRgb(self.background_color)
            if bg_color.lightness() < 128:
                fg_color = 0xffffff
            else: fg_color = 0x000000
            self.__color_label.setStyleSheet("QLabel {background-color: "+f"#{self.background_color:06x}"+f";color:#{fg_color:06x}"+";}")

        self.__color_label.setText(color_text)

        # Update labels
        if self.total == 0:
            row_text = ""
        else:
            row_text = f"Row {self.row}/{self.total}"
            if self.repeats >= 0:
                row_text += f" ({self.repeats} repeats completed)"
        self.__row_label.setText(row_text)
        self.__status_label.setText(f"{self.row}/{self.total}")
