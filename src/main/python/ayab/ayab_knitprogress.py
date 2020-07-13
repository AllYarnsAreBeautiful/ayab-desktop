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

from PyQt5.QtCore import Qt, QCoreApplication, QRect
from PyQt5.QtWidgets import QScrollArea, QGridLayout, QLayout, QLabel, QWidget
from bitarray import bitarray
from .plugins.ayab_plugin import utils


class KnitProgress(QScrollArea):
    """
    Class for the knit progress window, implemented as a subclass of
    `QScrollArea`.

    @author Tom Price
    @date   June 2020
    """
    def __init__(self, parent):
        super().__init__(parent.ui.graphics_splitter)
        self.setGeometry(QRect(0, 0, 700, 220))
        self.setContentsMargins(1, 1, 1, 1)

    def reset(self):
        self.container = QWidget()
        self.container.setMinimumSize(100, 100)
        self.grid = QGridLayout(self.container)
        self.grid.setContentsMargins(1, 1, 1, 1)
        self.grid.setSpacing(0)
        self.grid.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.setWidget(self.container)
        self.row = -1

    def update(self, status, row_multiplier):
        if status.current_row < 0:
            return
        # else
        tr_ = QCoreApplication.translate
        row, swipe = divmod(status.line_number, row_multiplier)
        direction = status.line_number % 2
        # row
        w0 = self.__label(tr_("KnitProgress", "Row"))
        self.grid.addWidget(w0, status.line_number, 0)
        w1 = self.__label(str(status.current_row))
        self.grid.addWidget(w1, status.line_number, 1, 1, 1, Qt.AlignRight)
        # pass
        w2 = self.__label(tr_("KnitProgress", "Pass") + " " + str(swipe + 1))
        self.grid.addWidget(w2, status.line_number, 2)
        # color
        if status.color_symbol == "":
            coltext = ""
        else:
            coltext = tr_("KnitProgress", "Color") + " " + status.color_symbol
        w3 = self.__label(coltext)
        self.grid.addWidget(w3, status.line_number, 3)
        # carriage and direction
        try:
            carriage = status.carriage[0] + status.carriage[2] + " "
        except Exception:
            carriage = ""
        w4 = self.__label(carriage + ["\u2192 ", "\u2190 "][direction])
        self.grid.addWidget(w4, status.line_number, 4)
        # TODO: hints, notes, memos
        w0.show()
        w1.show()
        w2.show()
        w3.show()
        w4.show()
        self.ensureWidgetVisible(w0)
        # graph line of stitches
        for c in range(len(status.bits)):
            wc = self.__stitch(status.color, status.bits[c], status.alt_color)
            self.grid.addWidget(wc, status.line_number, 6 + c)

    def __label(self, text):
        table = "<table><tbody><tr height='12'><td style='font-weight: normal;'>" + text + "</td></tr></tbody></table>"
        label = QLabel()
        label.setText(table)
        label.setTextFormat(Qt.RichText)
        return label

    def __stitch(self, color, bit, alt_color=None, symbol=0x20):
        table = "<table style='font-weight: normal;'><tbody><tr height='12'><td width='12' align='center' "
        if bit:
            table = table + "style='border: 1 solid black; color: #{:06x}; background-color: #{:06x};'>".format(
                utils.contrast_color(color), color) + chr(symbol)
        elif alt_color is not None:
            table = table + "style='border: 1 solid black; color: #{:06x}; background-color: #{:06x};'>".format(
                utils.contrast_color(alt_color), alt_color) + chr(symbol)
        else:
            table = table + "style='border: 1 dotted black;'>"
        table = table + "</td></tr></tbody></table>"
        label = QLabel()
        label.setText(table)
        label.setTextFormat(Qt.RichText)
        return label
