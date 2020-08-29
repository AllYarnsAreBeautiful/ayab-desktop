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

from PyQt5.QtCore import Qt, QCoreApplication, QRect, QSize
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QSizePolicy, QAbstractItemView, QWidget, QHBoxLayout
from bitarray import bitarray

from . import utils
from .engine.status import Direction


class KnitProgress(QTableWidget):
    """
    Class for the knit progress window, implemented as a subclass of `QScrollArea`.

    @author Tom Price
    @date   June 2020
    """
    green = 0xBBCCBB
    orange = 0xEECC99

    def __init__(self, parent):
        super().__init__(parent.ui.graphics_splitter)
        self.clear()
        self.setRowCount(0)
        self.setStyleSheet("border-width: 0;")
        self.setGeometry(QRect(0, 0, 700, 220))
        self.setContentsMargins(1, 1, 1, 1)
        self.verticalHeader().setDefaultSectionSize(16)
        self.blank = QTableWidgetItem()
        self.blank.setSizeHint(QSize(0, 0))
        self.setColumnCount(6)
        for r in range(6):
            self.setHorizontalHeaderItem(r, self.blank)

    def start(self):
        self.clearContents()
        self.clearSelection()
        self.setRowCount(0)
        self.row = -1
        self.color = True

    def update(self, status, row_multiplier, midline, auto_mirror):
        if status.current_row < 0:
            return
        # else
        tr_ = QCoreApplication.translate
        row, swipe = divmod(status.line_number, row_multiplier)

        # row
        w0 = self.__item(tr_("KnitProgress", "Row") + " " + str(status.current_row))

        # pass
        w1 = self.__item(tr_("KnitProgress", "Pass") + " " + str(swipe + 1))

        # color
        if status.color_symbol == "":
            self.color = False
            self.setColumnHidden(2, True)
        else:
            coltext = tr_("KnitProgress", "Color") + " " + status.color_symbol
            w2 = self.__item(coltext)

        # carriage and direction
        try:
            carriage = status.carriage[0] + status.carriage[2] + " "
        except Exception:
            carriage = ""
        # direction = status.direction
        if status.line_number % 2 == 0:
            direction = Direction.LEFT_TO_RIGHT
        else:
            direction = Direction.RIGHT_TO_LEFT
        w3 = self.__item(carriage + direction.symbol)

        # graph line of stitches
        status.bits.reverse()
        midline = len(status.bits) - midline

        table_text = "<table style='cell-spacing: 1; cell-padding: 1; background-color: #{:06x};'><tr> ".format(self.orange)
        for c in range(0, midline):
            table_text += self.__stitch(status.color, status.bits[c], status.alt_color)
        table_text += "</tr></table>"
        # FIXME: align label right
        # w4 = QWidget()
        # w4a = QHBoxLayout()
        # w4b = QLabel(table_text)
        # w4a.setAlignment(Qt.AlignRight)
        # w4a.addWidget(w4b)
        # w4.setLayout(w4a)
        w4 = QLabel(table_text)

        table_text = "<table style='cell-spacing: 1; cell-padding: 1; background-color: #{:06x};'><tr> ".format(self.green)
        for c in range(midline, len(status.bits)):
            table_text += self.__stitch(status.color, status.bits[c], status.alt_color)
        table_text += "</tr></table>"
        # FIXME: align label left
        # w5 = QWidget()
        # w5a = QHBoxLayout()
        # w5b = QLabel(table_text)
        # w5a.setAlignment(Qt.AlignLeft)
        # w5a.addWidget(w5b)
        # w5.setLayout(w5a)
        w5 = QLabel(table_text)

        self.insertRow(0)
        self.setItem(0, 0, w0)
        self.setItem(0, 1, w1)
        if self.color:
            self.setItem(0, 2, w2)
        self.setItem(0, 3, w3)
        self.setCellWidget(0, 4, w4)
        self.setCellWidget(0, 5, w5)
        blank = QTableWidgetItem()
        blank.setSizeHint(QSize(0, 0))
        self.setVerticalHeaderItem(0, blank)
        self.resizeColumnsToContents()
        # self.ensureWidgetVisible(w0)

    def __item(self, text):
        table = "<table><tr><td>" + text + "</td></tr></table>"
        item = QTableWidgetItem(text)
        return item

    def __stitch(self, color, bit, alt_color=None):
        # FIXME: borders are not visible
        text = "<td width='12' style='"
        if bit:
            text += "border: 1 solid black; background-color: #{:06x};".format(color)
        elif alt_color is not None:
            text += "border: 1 solid black; background-color: #{:06x};".format(alt_color)
        else:
            text += "border: 1 dotted black;"
        text += "'/>"
        return text
