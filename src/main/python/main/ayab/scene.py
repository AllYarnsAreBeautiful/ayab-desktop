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
from __future__ import annotations

import logging
from enum import Enum

from PySide6.QtCore import QRect
from PySide6.QtGui import QImage, QPixmap, QPen, QBrush, QColor, QWheelEvent, QTransform
from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsRectItem,
    QGraphicsView,
    QComboBox,
)

from .image import AyabImage
from .engine.options import Alignment
from .machine import Machine
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ayab import GuiMain


class AspectRatio(Enum):
    DEFAULT = 0
    FAIRISLE = 1

    @staticmethod
    def add_items(box: QComboBox) -> None:
        box.addItem("1:1")
        box.addItem("4:5")


class Scene(QGraphicsView):
    """Graphics scene object for UI.

    @author Tom Price
    @date   June 2020
    """

    def __init__(self, parent: GuiMain):
        super().__init__(parent.ui.graphics_splitter)
        self.setGeometry(QRect(0, 0, 700, 686))
        self.ayabimage: AyabImage = AyabImage(parent)
        self.__prefs = parent.prefs
        default = self.__prefs.value("default_alignment")
        self.__alignment: Alignment = Alignment(default)
        machine_width: int = Machine(self.__prefs.value("machine")).width
        self.__start_needle: int = (machine_width // 2) - 20
        self.__stop_needle: int = (machine_width - 1) // 2 + 20
        self.__row_progress: int = 0
        self.image_reversed = False

        # zoom behavior
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.__zoom: float = 3

        self.refresh()

    def set_image_reversed(self, image_reversed: bool) -> None:
        """Sets the image reversed flag"""
        self.image_reversed = image_reversed

        self.refresh()

    def refresh(self) -> None:
        """Updates the graphics scene"""
        qscene = QGraphicsScene()

        machine_width = Machine(self.__prefs.value("machine")).width

        # draw "machine"
        rect_orange = QGraphicsRectItem(
            -machine_width / 2 - 0.5, -5.5, machine_width / 2 + 0.5, 5
        )
        rect_orange.setBrush(QBrush(QColor("orange")))
        rect_green = QGraphicsRectItem(0, -5.5, machine_width / 2 + 0.5, 5)
        rect_green.setBrush(QBrush(QColor("green")))

        qscene.addItem(rect_orange)
        qscene.addItem(rect_green)

        if self.ayabimage.image is not None:
            width, height = self.ayabimage.image.size
            data = self.ayabimage.image.convert("RGBA").tobytes("raw", "RGBA")
            qim = QImage(data, width, height, QImage.Format.Format_RGBA8888)
            if self.image_reversed:
                qim = qim.transformed(QTransform.fromScale(-1, 1))
            pixmap = QPixmap.fromImage(qim)

            # add pattern and locate according to alignment
            pattern = qscene.addPixmap(pixmap)
            if self.__alignment == Alignment.LEFT:
                pos = self.__start_needle - machine_width / 2
            elif self.__alignment == Alignment.CENTER:
                pos = (
                    self.__start_needle
                    + self.__stop_needle
                    + 1
                    - pixmap.width()
                    - machine_width
                ) / 2
            elif self.__alignment == Alignment.RIGHT:
                pos = self.__stop_needle + 1 - machine_width / 2 - pixmap.width()
            else:
                logging.warning("invalid alignment")
                return
            pattern.setPos(pos, 0)

            # draw limiting lines (start/stop needle)
            qscene.addItem(
                QGraphicsRectItem(
                    self.__start_needle - machine_width / 2 - 0.5,
                    -5.5,
                    0,
                    pixmap.height() + 5.5,
                )
            )
            qscene.addItem(
                QGraphicsRectItem(
                    self.__stop_needle - machine_width / 2 + 1.5,
                    -5.5,
                    0,
                    pixmap.height() + 5.5,
                )
            )

            # Draw knitting progress
            qscene.addItem(
                QGraphicsRectItem(
                    -machine_width / 2 - 1,
                    pixmap.height() - self.__row_progress - 0.5,
                    self.__start_needle,
                    0,
                )
            )
            qscene.addItem(
                QGraphicsRectItem(
                    self.__stop_needle - machine_width / 2 + 1,
                    pixmap.height() - self.__row_progress - 0.5,
                    machine_width - self.__stop_needle,
                    0,
                )
            )
            grey = QGraphicsRectItem(
                self.__start_needle - machine_width / 2,
                pixmap.height(),
                self.__stop_needle - self.__start_needle + 1,
                -self.__row_progress,
            )
            grey.setPen(QPen(QColor(127, 127, 127, 127), 0))
            grey.setBrush(QBrush(QColor(127, 127, 127, 127)))
            qscene.addItem(grey)

        self.resetTransform()
        self.scale(
            self.zoom, self.zoom * (1.0 - 0.2 * self.__prefs.value("aspect_ratio"))
        )
        self.setScene(qscene)

    @property
    def row_progress(self) -> int:
        return self.__row_progress

    @row_progress.setter
    def row_progress(self, row_progress: int) -> None:
        self.__row_progress = row_progress
        self.refresh()

    def update_needles(self, start_needle: int, stop_needle: int) -> None:
        """Update the position of the start/stop needle visualization"""
        self.__start_needle = start_needle
        self.__stop_needle = stop_needle
        self.refresh()

    @property
    def our_alignment(self) -> Alignment:
        return self.__alignment

    def update_alignment(self, alignment: Alignment) -> None:
        """Update the alignment of the image between start/stop needle"""
        self.__alignment = Alignment(alignment)
        self.refresh()

    def wheelEvent(self, event: QWheelEvent) -> None:
        """Zoom the pattern upon mouse wheel event"""
        self.zoom = event  # type: ignore

    @property
    def zoom(self) -> float:
        return self.__zoom

    @zoom.setter
    def zoom(self, event: QWheelEvent) -> None:
        """Use mouse wheel events to zoom the graphical image"""
        # angleDelta.y is 120 or -120 when scrolling
        self.set_zoom(event.angleDelta().y() / 120)

    def set_zoom(self, zoom: float) -> None:
        self.__zoom += zoom * 0.5
        self.__zoom = max(1, self.__zoom)
        self.__zoom = min(7, self.__zoom)
        self.refresh()
