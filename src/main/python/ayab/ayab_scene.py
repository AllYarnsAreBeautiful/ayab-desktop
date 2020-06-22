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

import weakref
import logging
from math import ceil

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

from PIL import Image
from DAKimport import DAKimport

from .ayab_transforms import Transformable, Mirrors

MACHINE_WIDTH = 200


class Scene (object):
    """Graphics scene object for UI.

    @author Tom Price
    @date   June 2020
    """

    BAR_HEIGHT = 5.0
    LIMIT_BAR_WIDTH = 0.5

    def __init__(self, parent):
        self.__parent = parent  # weakref.ref(parent)
        self.image = None
        self.imageAlignment = parent.prefs.settings.value("default_alignment")
        self.start_needle = 80
        self.stop_needle = 119
        self.var_progress = 0
        self.zoomlevel = 3

    def refresh(self):
        '''Updates the graphics scene'''
        width, height = self.image.size

        data = self.image.convert("RGBA").tobytes("raw", "RGBA")
        qim = QtGui.QImage(data,
                           self.image.size[0],
                           self.image.size[1],
                           QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(qim)

        # Set dimensions on GUI
        text = "{} x {}".format(width, height)
        self.__parent.ui.label_notifications.setText("Image Dimensions: " + text)

        qscene = QtWidgets.QGraphicsScene()

        # add pattern and move accordingly to alignment
        pattern = qscene.addPixmap(pixmap)
        if self.imageAlignment == 'left':
            pos = self.start_needle - MACHINE_WIDTH / 2
        elif self.imageAlignment == 'center':
            pos = (self.start_needle + self.stop_needle - pixmap.width() - MACHINE_WIDTH) / 2
        elif self.imageAlignment == 'right':
            pos = self.stop_needle - pixmap.width() - MACHINE_WIDTH / 2
        else:
            logging.warning("invalid alignment")
            return
        pattern.setPos(pos, 0)

        # Draw "machine"
        rect_orange = QtWidgets.QGraphicsRectItem(
            -(MACHINE_WIDTH / 2.0),
            -self.BAR_HEIGHT,
            (MACHINE_WIDTH / 2.0),
            self.BAR_HEIGHT)
        rect_orange.setBrush(QtGui.QBrush(QtGui.QColor("orange")))
        rect_green = QtWidgets.QGraphicsRectItem(
            0.0,
            -self.BAR_HEIGHT,
            (MACHINE_WIDTH / 2.0),
            self.BAR_HEIGHT)
        rect_green.setBrush(QtGui.QBrush(QtGui.QColor("green")))

        qscene.addItem(rect_orange)
        qscene.addItem(rect_green)

        # Draw limiting lines (start/stop needle)
        qscene.addItem(
            QtWidgets.QGraphicsRectItem(self.start_needle - 1 - MACHINE_WIDTH / 2,
                                        -self.BAR_HEIGHT,
                                        self.LIMIT_BAR_WIDTH,
                                        pixmap.height() + 2 * self.BAR_HEIGHT))
        qscene.addItem(
            QtWidgets.QGraphicsRectItem(self.stop_needle - MACHINE_WIDTH / 2,
                                        -self.BAR_HEIGHT,
                                        self.LIMIT_BAR_WIDTH,
                                        pixmap.height() + 2 * self.BAR_HEIGHT))

        # Draw knitting progress
        qscene.addItem(
            QtWidgets.QGraphicsRectItem(- MACHINE_WIDTH / 2,
                                        pixmap.height() - self.var_progress,
                                        MACHINE_WIDTH,
                                        self.LIMIT_BAR_WIDTH))

        qv = self.__parent.ui.image_pattern_view
        qv.resetTransform()
        qv.scale(self.zoomlevel, self.zoomlevel)
        qv.setScene(qscene)

    def load_image_file(self, image_str):
        # check for DAK files
        image_str_suffix = image_str[-4:].lower()
        if (image_str_suffix == ".pat" or image_str_suffix == ".stp"):
            # convert DAK file
            dakfile_processor = DAKimport.Importer()
            if (image_str_suffix == ".pat"):
                self.image = dakfile_processor.pat2im(image_str)
            elif (image_str_suffix == ".stp"):
                self.image = dakfile_processor.stp2im(image_str)
            else:
                raise RuntimeError("Unrecognized file suffix")
        else:
            self.image = Image.open(image_str)
        self.image = self.image.convert("RGBA")

    def updateNeedles(self, start_needle, stop_needle):
        '''Updates the position of the start/stop needle visualisation'''
        self.start_needle = start_needle
        self.stop_needle = stop_needle
        self.refresh()

    def updateAlignment(self, alignment):
        '''Updates the alignment of the image between start/stop needle'''
        self.imageAlignment = alignment
        self.refresh()

    def zoom(self, event):
        '''Using mouse wheel events to zoom the pattern view'''
        if self.image is not None:
            # angleDelta.y is 120 or -120 when scrolling
            zoom = event.angleDelta().y() / 120
            self.zoomlevel += zoom
            self.zoomlevel = max(1, self.zoomlevel)
            self.zoomlevel = min(5, self.zoomlevel)
            self.refresh()

    def invert_image(self):
        '''Public invert current Image function.'''
        self.apply_image_transform("invert")

    def repeat_image(self):
        '''Public repeat current Image function.'''
        v = QtWidgets.QInputDialog.getInt(
            self,
            "Repeat",
            "Vertical",
            value=1,
            min=1
        )
        h = QtWidgets.QInputDialog.getInt(
            self,
            "Repeat",
            "Horizontal",
            value=1,
            min=1,
            max=ceil(MACHINE_WIDTH / self.image.size[0])
        )
        self.apply_image_transform("repeat", v[0], h[0])

    def stretch_image(self):
        '''Public stretch current Image function.'''
        v = QtWidgets.QInputDialog.getInt(
            self,
            "Stretch",
            "Vertical",
            value=1,
            min=1
        )
        h = QtWidgets.QInputDialog.getInt(
            self,
            "Stretch",
            "Horizontal",
            value=1,
            min=1,
            max=ceil(MACHINE_WIDTH / self.image.size[0])
        )
        self.apply_image_transform("stretch", v[0], h[0])

    def reflect_image(self):
        '''Public reflect current Image function.'''
        m = Mirrors()
        if (m.result == QtWidgets.QDialog.Accepted):
            self.apply_image_transform("reflect", m.mirrors)

    def hflip_image(self):
        '''Public horizontal flip current Image function.'''
        self.apply_image_transform("hflip")

    def vflip_image(self):
        '''Public vertical flip current Image function.'''
        self.apply_image_transform("vflip")

    def rotate_left(self):
        '''Public rotate left current Image function.'''
        self.apply_image_transform("rotate", 90.0)

    def rotate_right(self):
        '''Public rotate right current Image function.'''
        self.apply_image_transform("rotate", -90.0)

    def apply_image_transform(self, method, *args):
        '''Executes an image transform specified by key and args.

        Calls a transform function, forwarding args and the image,
        and replaces the QtImage on scene.
        '''
        transform = getattr(Transformable, method)
        try:
            image = transform(self.image, args)
        except:
            logging.error("Error on executing transform")
        if not image:
            return

        # Transition to NOT_CONFIGURED state
        self.__parent.signalImageTransformed.emit()

        # Update the view
        self.image = image

        # Update maximum values
        width, height = self.image.size
        self.__parent.plugin.setImageDimensions(width, height)

        # Draw canvas
        self.refresh()

