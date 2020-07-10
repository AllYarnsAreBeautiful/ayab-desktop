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
from PyQt5.QtGui import QImage, QPixmap, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsView

from .ayab_image import AyabImage
from .plugins.ayab_plugin.ayab_options import Alignment
from .plugins.ayab_plugin.machine import Machine


class Scene(QGraphicsView):
    """Graphics scene object for UI.

    @author Tom Price
    @date   June 2020
    """

    BAR_HEIGHT = 5.0
    LIMIT_BAR_WIDTH = 0.5

    def __init__(self, parent):
        super().__init__(parent.ui.graphics_splitter)
        self.setGeometry(QRect(0, 0, 700, 686))
        self.ayabimage = AyabImage(parent)
        default = parent.prefs.settings.value("default_alignment")
        self.__alignment = Alignment(default)
        self.__start_needle = 80
        self.__stop_needle = 119
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

        # Add pattern and move accordingly to alignment
        pattern = qscene.addPixmap(pixmap)
        if self.__alignment == Alignment.LEFT:
            pos = self.__start_needle - Machine.WIDTH / 2
        elif self.__alignment == Alignment.CENTER:
            pos = (self.__start_needle + self.__stop_needle - pixmap.width() -
                   Machine.WIDTH) / 2
        elif self.__alignment == Alignment.RIGHT:
            pos = self.__stop_needle - pixmap.width() - Machine.WIDTH / 2
        else:
            logging.warning("invalid alignment")
            return
        pattern.setPos(pos, 0)

        # Draw "machine"
        rect_orange = QGraphicsRectItem(-Machine.WIDTH / 2.0, -self.BAR_HEIGHT,
                                        Machine.WIDTH / 2.0, self.BAR_HEIGHT)
        rect_orange.setBrush(QBrush(QColor("orange")))
        rect_green = QGraphicsRectItem(0.0, -self.BAR_HEIGHT,
                                       Machine.WIDTH / 2.0, self.BAR_HEIGHT)
        rect_green.setBrush(QBrush(QColor("green")))

        qscene.addItem(rect_orange)
        qscene.addItem(rect_green)

        # Draw limiting lines (start/stop needle)
        qscene.addItem(
            QGraphicsRectItem(self.__start_needle - 1 - Machine.WIDTH / 2,
                              -self.BAR_HEIGHT, self.LIMIT_BAR_WIDTH,
                              pixmap.height() + 2 * self.BAR_HEIGHT))
        qscene.addItem(
            QGraphicsRectItem(self.__stop_needle - Machine.WIDTH / 2,
                              -self.BAR_HEIGHT, self.LIMIT_BAR_WIDTH,
                              pixmap.height() + 2 * self.BAR_HEIGHT))

        # Draw knitting progress
        qscene.addItem(
            QGraphicsRectItem(-Machine.WIDTH / 2,
                              pixmap.height() - self.__row_progress,
                              Machine.WIDTH, self.LIMIT_BAR_WIDTH))

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

    @property
    def zoom(self):
        return self.__zoom

    @zoom.setter
    def zoom(self, event):
        '''Use mouse wheel events to zoom the pattern view'''
        if self.ayabimage.image is not None:
            # angleDelta.y is 120 or -120 when scrolling
            zoom = event.angleDelta().y() / 120
            self.__zoom += zoom
            self.__zoom = max(1, self.__zoom)
            self.__zoom = min(5, self.__zoom)
            self.refresh()
