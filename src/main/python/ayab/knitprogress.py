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
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QSizePolicy, QAbstractItemView, QWidget, QHBoxLayout, QHeaderView
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
        self.setGeometry(QRect(0, 0, 700, 220))
        self.setContentsMargins(1, 1, 1, 1)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().setVisible(False)
        self.blank = QTableWidgetItem()
        self.blank.setSizeHint(QSize(0, 0))
        self.setColumnCount(6)
        for r in range(6):
            self.setHorizontalHeaderItem(r, self.blank)
        self.previousStatus = None
        self.scene = parent.scene

    def start(self):
        self.clearContents()
        self.clearSelection()
        self.setRowCount(0)
        self.horizontalHeader().setSectionHidden(5, False)
        self.row = -1
        self.color = True

    def uiStateChanged(self, status):
        if not self.previousStatus:
            return True

        if status == self.previousStatus:
            return False

        if (status.line_number != self.previousStatus.line_number or
            status.current_row != self.previousStatus.current_row or
            status.color_symbol != self.previousStatus.color_symbol or
            status.carriage_type != self.previousStatus.carriage_type or
            status.carriage_direction != self.previousStatus.carriage_direction or
            status.bits != self.previousStatus.bits or
            status.alt_color != self.previousStatus.alt_color):
            return True

        return False


    def update(self, status, row_multiplier, midline, auto_mirror):
        # FIXME auto_mirror not used

        if not self.uiStateChanged(status):
            return

        if status.current_row < 0:
            return
        # else
        tr_ = QCoreApplication.translate
        row, swipe = divmod(status.line_number, row_multiplier)

        columns = []

        # row
        columns.append(tr_("KnitProgress", "Row") + " " + str(status.current_row))

        # pass
        columns.append(tr_("KnitProgress", "Pass") + " " + str(swipe + 1))

        # color
        if status.color_symbol == "":
            self.color = False
        else:
            self.color = True
            coltext = tr_("KnitProgress", "Color") + " " + status.color_symbol
            columns.append(coltext)

        carriage = status.carriage_type
        direction = status.carriage_direction
        columns.append(carriage.symbol + " " + direction.symbol)

        # graph line of stitches
        status.bits.reverse()
        midline = len(status.bits) - midline

        table_text = "<table style='cell-spacing: 1; cell-padding: 1; background-color: #{:06x};'><tr>".format(
            self.orange)
        for c in range(0, midline):
            table_text += self.__stitch(status.color, status.bits[c],
                                        status.alt_color)
        table_text += "</tr></table>"
        left_side = QLabel(table_text)

        table_text = "<table style='cell-spacing: 1; cell-padding: 1; background-color: #{:06x};'><tr>".format(
            self.green)
        for c in range(midline, len(status.bits)):
            table_text += self.__stitch(status.color, status.bits[c],
                                        status.alt_color)
        table_text += "</tr></table>"
        right_side = QLabel(table_text)

        self.insertRow(0)
        for i, col in enumerate(columns):
            self.setItem(0, i, self.__item(col))
        n_cols = len(columns)
        self.setCellWidget(0, n_cols, left_side)
        self.setCellWidget(0, n_cols + 1, right_side)
        if row_multiplier == 1:
            self.hideColumn(1)
        if n_cols < 4:
            self.hideColumn(5)
        self.resizeColumnsToContents()

        self.previousStatus = status

        # update bar in Scene
        self.scene.row_progress = status.current_row

    def __item(self, text):
        item = QTableWidgetItem(text)
        return item

    def __stitch(self, color, bit, alt_color=None):
        # FIXME: borders are not visible
        text = "<td width='12' style='border: 1 black "
        if bit:
            text += "solid; background-color: #{:06x};".format(
                color)
        elif alt_color is not None:
            text += "solid; background-color: #{:06x};".format(
                alt_color)
        else:
            text += "dotted;"
        return text + "'/>"
