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
from PySide6.QtCore import QCoreApplication, QRect, Qt
from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)
from PySide6.QtGui import QBrush, QColor
from typing import TYPE_CHECKING, Optional, cast, List
from math import floor

if TYPE_CHECKING:
    from .ayab import GuiMain
    from .preferences import Preferences
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
        self.__prefs: Preferences = parent.prefs
        self.__progbar = parent.progbar
        self.setGeometry(QRect(0, 0, 700, 220))
        self.setContentsMargins(1, 1, 1, 1)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setSectionsClickable(False)
        self.horizontalHeader().setMinimumSectionSize(0)
        self.horizontalHeader().setDefaultSectionSize(
            self.__prefs.value("lower_display_stitch_width")
        )
        self.horizontalHeader().setSectionsClickable(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.previousStatus: Optional[Status] = None
        self.scene = parent.scene
        self.currentItemChanged.connect(self.onStitchSelect)

    def start(self) -> None:
        self.clearContents()
        self.clearSelection()
        self.setRowCount(0)
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
            or status.knit_start_needle != self.previousStatus.knit_start_needle
            or status.machine_width != self.previousStatus.machine_width
            or status.passes_per_row != self.previousStatus.passes_per_row
        ):
            return True

        return False

    def update_progress(self, status: Status) -> None:
        if not self.uiStateChanged(status):
            return

        if status.current_row < 0:
            return

        columns: List[QTableWidgetItem] = []
        if status.color_symbol == "":
            self.color = False
        else:
            self.color = True

        self.load_columns_from_status(status, columns)

        # For the top row (row idx 0), we show the row header as "To Be Selected",
        # When we show a new row, we recover the header info and recombine it
        # with its row (now row idx 2)
        self.make_row_with_spacer()

        if self.columnCount() != len(columns):
            self.setColumnCount(len(columns))
        n_cols = len(columns)
        if n_cols < 4:
            self.hideColumn(5)
        self.instantiate_row_from_columns(status, columns)

        self.previousStatus = status

        # update bar in Scene
        self.scene.row_progress = status.current_row

    def load_columns_from_status(
        self, status: Status, columns: List[QTableWidgetItem]
    ) -> None:
        for c in range(0, len(status.bits)):
            needle = status.knit_start_needle + c
            needle_number_from_r1 = needle - status.machine_width // 2
            if needle_number_from_r1 < 0:
                color = self.__alternate_bg_colors(needle_number_from_r1, self.orange)
            else:
                color = self.__alternate_bg_colors(needle_number_from_r1, self.green)
            columns.append(
                self.__stitch(
                    status.color, cast(bool, status.bits[c]), status.alt_color, color
                )
            )

    def instantiate_row_from_columns(
        self, status: Status, columns: List[QTableWidgetItem]
    ) -> None:
        self.setVerticalHeaderItem(
            0,
            QTableWidgetItem(
                QCoreApplication.translate("KnitProgress", "To Be Selected")
            ),
        )
        for i, col in enumerate(columns):
            self.setItem(0, i, col)
            self.setColumnWidth(i, self.__prefs.value("lower_display_stitch_width"))
            # when width is under 20, the column numbers are unreadable.
            if self.columnWidth(i) < 20:
                self.horizontalHeader().setVisible(False)
            else:
                self.horizontalHeader().setVisible(True)
            needle = status.knit_start_needle + i
            needle_number_from_r1 = needle - status.machine_width // 2
            if needle_number_from_r1 < 0:
                header = QTableWidgetItem(f"{-needle_number_from_r1}")
                header.font().setBold(True)
                header.setForeground(QBrush(QColor(f"#{self.orange:06x}")))
                header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setHorizontalHeaderItem(i, header)
            else:
                header = QTableWidgetItem(f"{1 + needle_number_from_r1}")
                header.setForeground(QBrush(QColor(f"#{self.green:06x}")))
                header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setHorizontalHeaderItem(i, header)

    def make_row_with_spacer(self) -> None:
        self.removeRow(1)
        self.insertRow(0)
        self.insertRow(1)
        self.setVerticalHeaderItem(1, QTableWidgetItem(""))
        if self.rowCount() > 2:
            self.setVerticalHeaderItem(
                2,
                self.format_row_header_text(self.previousStatus),
            )
        self.verticalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setMinimumSectionSize(0)
        self.verticalHeader().resizeSection(1, 5)

    def format_row_header_text(self, status: Optional[Status]) -> QTableWidgetItem:
        if status is None:
            return QTableWidgetItem("")
        tr_ = QCoreApplication.translate
        info_header = QTableWidgetItem()
        info_text = ""
        swipe = status.line_number % status.passes_per_row
        # row "Row [1]"
        info_text = tr_("KnitProgress", "Row") + " " + str(status.current_row)

        # pass, see Mode object. "Pass [1,2,3]"
        if status.passes_per_row > 1:
            info_text = info_text + (
                f' {tr_("KnitProgress", "Pass")} {swipe + 1}/{status.passes_per_row}'
            )

        # color "Color [A,B,C,D]"
        if self.color is True:
            info_text = (
                info_text
                + " "
                + tr_("KnitProgress", "Color")
                + " "
                + status.color_symbol
            )
            background_color = QColor(f"#{status.color:06x}")
            # Ensure text is readable
            if background_color.lightness() > 128:
                background_color.setHsl(
                    background_color.hslHue(), background_color.hslSaturation(), 128
                )
            info_header.setForeground(QBrush(background_color))

        # Carriage & Direction "[K,L,G] [<-,->]"
        carriage = status.carriage_type
        direction = status.carriage_direction
        info_text = info_text + (" " + carriage.symbol + " " + direction.symbol)
        info_header.setText(info_text)
        return info_header

    def __alternate_bg_colors(
        self, position: int, color: int, frequency: int = 10
    ) -> QColor:
        background_color = QColor(f"#{color:06x}")
        bg_color_alternate = (position // frequency) % 2
        if bg_color_alternate > 0:
            background_color.setHsl(
                floor(background_color.hslHue() * 0.85),
                floor(background_color.hslSaturation() * 0.85),
                background_color.lightness(),
            )
        return background_color

    def __stitch(
        self,
        color: int,
        bit: bool,
        alt_color: Optional[int] = None,
        bg_color: Optional[QColor] = None,
    ) -> QTableWidgetItem:
        stitch = QTableWidgetItem()
        if bit:
            background_color = QColor(f"#{color:06x}")
            stitch.setBackground(background_color)
        elif alt_color is not None:
            stitch.setBackground(QBrush(QColor(f"#{alt_color:06x}")))
        else:
            if bg_color is not None:
                stitch.setBackground(QBrush(bg_color))
        return stitch

    def onStitchSelect(self, current: QTableWidgetItem | None) -> None:
        if current is None:
            self.__progbar.set_selection_label("")
            return
        header = self.horizontalHeaderItem(current.column())
        if header is not None and header.foreground().color().red() == 187:
            side = "Right"
        else:
            side = "Left"
        selection_string = f"""Selection: {
            self.verticalHeaderItem(current.row()).text()} stitch {side}-{
            header.text() if header else ''}"""
        self.__progbar.set_selection_label(selection_string)
