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
from PySide6.QtCore import QCoreApplication, QRect, QSize, Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QHeaderView
from PySide6.QtGui import QBrush, QColor
from typing import TYPE_CHECKING, Optional, cast, List

if TYPE_CHECKING:
    from .ayab import GuiMain
    from .engine.status import Status


class KnitProgress(QTableWidget):
    """
    Class for the knit progress window, implemented as a subclass of `QScrollArea`.

    @author Tom Price
    @date   June 2020
    """

    green = 0xBBCCBB
    orange = 0xEECC99

    def __init__(self, parent: GuiMain):
        super().__init__(parent.ui.graphics_splitter)
        self.clear()
        self.setRowCount(0)
        self.setGeometry(QRect(0, 0, 700, 220))
        self.setContentsMargins(1, 1, 1, 1)
        self.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        # self.verticalHeader().setVisible(False)
        self.setColumnCount(6)
        for r in range(6):
            blank = QTableWidgetItem()
            blank.setSizeHint(QSize(0, 0))
            self.setHorizontalHeaderItem(r, blank)
        self.previousStatus: Optional[Status] = None
        self.scene = parent.scene

    def start(self) -> None:
        self.clearContents()
        self.clearSelection()
        self.setRowCount(0)
        # self.horizontalHeader().setSectionHidden(5, False)
        self.setCurrentCell(-1, -1)
        self.color = True

    def uiStateChanged(self, status: Status) -> bool:
        if not self.previousStatus:
            return True

        if status == self.previousStatus:
            return False

        if (
            status.line_number != self.previousStatus.line_number
            or status.current_row != self.previousStatus.current_row
            or status.color_symbol != self.previousStatus.color_symbol
            or status.carriage_type != self.previousStatus.carriage_type
            or status.carriage_direction != self.previousStatus.carriage_direction
            or status.bits != self.previousStatus.bits
            or status.alt_color != self.previousStatus.alt_color
        ):
            return True

        return False

    def update_progress(
        self, status: Status, row_multiplier: int, midline: int, auto_mirror: bool
    ) -> None:
        # FIXME auto_mirror not used

        if not self.uiStateChanged(status):
            return

        if status.current_row < 0:
            return
        # else
        tr_ = QCoreApplication.translate
        row, swipe = divmod(status.line_number, row_multiplier)

        columns: List[QTableWidgetItem] = []
        info_text = ""
        info_header = QTableWidgetItem()
        # row "Row [1]"
        info_text= (tr_("KnitProgress", "Row") + " " + str(status.current_row))

        # pass, see Mode object. "Pass [1,2,3]"
        if row_multiplier == 1:
            info_text= info_text+(" "+tr_("KnitProgress", "Pass") + " " + str(swipe + 1))

        # color "Color [A,B,C,D]" 
        if status.color_symbol == "":
            self.color = False
        else:
            self.color = True
            info_text = info_text + " " + tr_("KnitProgress", "Color") + " " + status.color_symbol
            bgColor = QColor(f"#{status.color:06x}")
            # Ensure text is readable
            if bgColor.lightness() > 128:
                bgColor.setHsl(bgColor.hslHue(),bgColor.hslSaturation(),128)
            info_header.setForeground(QBrush(bgColor))

        # Carriage & Direction "[K,L,G] [<-,->]"
        carriage = status.carriage_type
        direction = status.carriage_direction
        info_text= info_text +(" "+carriage.symbol + " " + direction.symbol)

        print(info_text)
        info_header.setText(info_text)

        # graph line of stitches
        midline = len(status.bits) - midline

        for c in range(0, midline):
            columns.append(self.__stitch(
                status.color, cast(bool, status.bits[c]), status.alt_color, self.orange
            ))

        # if we are only working on the right side, midline is negative.
        green_start= midline
        if green_start < 0: 
            green_start=0
        for c in range(green_start, len(status.bits)):
            columns.append(self.__stitch(
                status.color, cast(bool, status.bits[c]), status.alt_color, self.green
            ))

        self.insertRow(0)
        if self.columnCount() != len(columns):
            self.setColumnCount(len(columns))
        self.setVerticalHeaderItem(0,info_header)
        for i, col in enumerate(columns):
            self.setItem(0, i, col)
            if i < midline:
                header = QTableWidgetItem(f"{(midline)-(i)}")
                header.font().setBold(True)
                header.setForeground(QBrush(QColor(f"#{self.orange:06x}")))
                header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setHorizontalHeaderItem(i,header)
            else:
                header = QTableWidgetItem(f"{(i+1)-(midline)}")
                header.setForeground(QBrush(QColor(f"#{self.green:06x}")))
                header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setHorizontalHeaderItem(i,header)
                # self.horizontalHeaderItem(i).setText((i)-(midline+info_columns))
        n_cols = len(columns)
        print(n_cols)
        if n_cols < 4:
            self.hideColumn(5)
        self.resizeColumnsToContents()

        self.previousStatus = status

        # update bar in Scene
        self.scene.row_progress = status.current_row

    def __item(self, text: str) -> QTableWidgetItem:
        item = QTableWidgetItem(text)
        return item

    def __stitch(self, color: int, bit: bool, alt_color: Optional[int] = None, bg_color: Optional[int] = None) -> QTableWidgetItem:
        stitch = QTableWidgetItem()
        if bit:
            bgColor = QColor(f"#{color:06x}")
            stitch.setBackground(bgColor)
        elif alt_color is not None:
            stitch.setBackground(QBrush(QColor(f"#{alt_color:06x}")))
        else:
            if bg_color is not None:
                stitch.setBackground(QBrush(QColor(f"#{bg_color:06x}")))
            # text += "dotted;"
        return stitch
