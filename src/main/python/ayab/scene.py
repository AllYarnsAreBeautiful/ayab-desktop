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

import logging

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QImage, QPixmap, QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsView

from .image import AyabImage
from .engine.options import Alignment
from .machine import Machine


class Scene(QGraphicsView):
    """Graphics scene object for UI.

    @author Tom Price
    @date   June 2020
    """

    def __init__(self, parent):
        super().__init__(parent.ui.graphics_splitter)
        self.setGeometry(QRect(0, 0, 700, 686))
        self.ayabimage = AyabImage(parent)
        self.__prefs = parent.prefs
        default = self.__prefs.value("default_alignment")
        self.__alignment = Alignment(default)
        machine_width = Machine(self.__prefs.value("machine")).width
        self.__start_needle = (machine_width // 2) - 20
        self.__stop_needle = (machine_width - 1) // 2 + 20
        self.__row_progress = 0

        # zoom behavior
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.__zoom = 3

    def refresh(self):
        '''Updates the graphics scene'''
        qscene = QGraphicsScene()

        width, height = self.ayabimage.image.size
        data = self.ayabimage.image.convert("RGBA").tobytes("raw", "RGBA")
        qim = QImage(data, width, height, QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(qim)

        # add pattern and locate according to alignment
        pattern = qscene.addPixmap(pixmap)
        machine_width = Machine(self.__prefs.value("machine")).width
        if self.__alignment == Alignment.LEFT:
            pos = self.__start_needle - machine_width / 2
        elif self.__alignment == Alignment.CENTER:
            pos = (self.__start_needle + self.__stop_needle + 1 - pixmap.width() - machine_width) / 2
        elif self.__alignment == Alignment.RIGHT:
            pos = self.__stop_needle + 1 - machine_width / 2 - pixmap.width()
        else:
            logging.warning("invalid alignment")
            return
        pattern.setPos(pos, 0)

        # draw "machine"
        rect_orange = QGraphicsRectItem(
            -machine_width / 2 - 0.5,
            -5.5,
            machine_width / 2 + 0.5,
            5)
        rect_orange.setBrush(QBrush(QColor("orange")))
        rect_green = QGraphicsRectItem(
            0,
            -5.5,
            machine_width / 2 + 0.5,
            5)
        rect_green.setBrush(QBrush(QColor("green")))

        qscene.addItem(rect_orange)
        qscene.addItem(rect_green)

        # draw limiting lines (start/stop needle)
        qscene.addItem(
            QGraphicsRectItem(
                self.__start_needle - machine_width / 2 - 0.5,
                -5.5,
                0,
                pixmap.height() + 5.5))
        qscene.addItem(
            QGraphicsRectItem(
                self.__stop_needle - machine_width / 2 + 1.5,
                -5.5,
                0,
                pixmap.height() + 5.5))
        qscene.addItem(
            QGraphicsRectItem(
                self.__start_needle - machine_width / 2 - 1,
                pixmap.height() + 0.5,
                self.__stop_needle - self.__start_needle + 3,
                0))

        # Draw knitting progress
        grey = QGraphicsRectItem(
            self.__start_needle - machine_width / 2,
            pixmap.height(),
            self.__stop_needle - self.__start_needle + 1,
            -self.__row_progress)
        grey.setPen(QPen(QColor(127, 127, 127, 127), 0))
        grey.setBrush(QBrush(QColor(127, 127, 127, 127)))
        qscene.addItem(grey)

        self.resetTransform()
        self.scale(self.zoom, self.zoom)
        self.setScene(qscene)

    @property
    def row_progress(self):
        return self.__row_progress

    @row_progress.setter
    def row_progress(self, row_progress):
        self.__row_progress = row_progress
        self.refresh()

    def update_needles(self, start_needle, stop_needle):
        '''Update the position of the start/stop needle visualization'''
        self.__start_needle = start_needle
        self.__stop_needle = stop_needle
        self.refresh()

    @property
    def alignment(self):
        return self.__alignment

    def update_alignment(self, alignment):
        '''Update the alignment of the image between start/stop needle'''
        self.__alignment = Alignment(alignment)
        self.refresh()

    def wheelEvent(self, event):
        '''Zoom the pattern upon mouse wheel event'''
        self.zoom = event

    @property
    def zoom(self):
        return self.__zoom

    @zoom.setter
    def zoom(self, event):
        '''Use mouse wheel events to zoom the graphical image'''
        if self.ayabimage.image is not None:
            # angleDelta.y is 120 or -120 when scrolling
            zoom = event.angleDelta().y() / 120
            self.__zoom += zoom
            self.__zoom = max(1, self.__zoom)
            self.__zoom = min(5, self.__zoom)
            self.refresh()
