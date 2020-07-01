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

# import weakref
import logging
from math import ceil

from PyQt5.QtGui import QImage, QPixmap, QBrush, QColor
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QInputDialog, QDialog

from PIL import Image
from DAKimport import DAKimport

from .ayab_transforms import Transformable, Mirrors
from .plugins.ayab_plugin.ayab_options import Alignment
from .plugins.ayab_plugin.machine import Machine


class Scene(object):
    """Graphics scene object for UI.

    @author Tom Price
    @date   June 2020
    """

    BAR_HEIGHT = 5.0
    LIMIT_BAR_WIDTH = 0.5

    def __init__(self, parent):
        self.__parent = parent  # weakref.ref(parent)
        self.__image = None
        default = parent.prefs.settings.value("default_alignment")
        self.__alignment = Alignment(default)
        self.__start_needle = 80
        self.__stop_needle = 119
        self.__zoom = 3
        self.row_progress = 0

    def refresh(self):
        '''Updates the graphics scene'''
        width, height = self.__image.size

        data = self.__image.convert("RGBA").tobytes("raw", "RGBA")
        qim = QImage(data, self.__image.size[0], self.__image.size[1],
                     QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(qim)

        # Set dimensions on GUI
        text = "{} x {}".format(width, height)
        self.__parent.ui.label_notifications.setText(
            QCoreApplication.translate("Scene", "Image dimensions") + ": " +
            text)

        qscene = QGraphicsScene()

        # add pattern and move accordingly to alignment
        pattern = qscene.addPixmap(pixmap)
        if self.__alignment.name == 'LEFT':
            pos = self.__start_needle - Machine.WIDTH / 2
        elif self.__alignment.name == 'CENTER':
            pos = (self.__start_needle + self.__stop_needle - pixmap.width() -
                   Machine.WIDTH) / 2
        elif self.__alignment.name == 'RIGHT':
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
                              pixmap.height() - self.row_progress,
                              Machine.WIDTH, self.LIMIT_BAR_WIDTH))

        qv = self.__parent.ui.image_pattern_view
        qv.resetTransform()
        qv.scale(self.zoom, self.zoom)
        qv.setScene(qscene)

    def load_image_file(self, image_str):
        # check for DAK files
        image_str_suffix = image_str[-4:].lower()
        if (image_str_suffix == ".pat" or image_str_suffix == ".stp"):
            # convert DAK file
            dakfile_processor = DAKimport.Importer()
            if (image_str_suffix == ".pat"):
                self.__image = dakfile_processor.pat2im(image_str)
            elif (image_str_suffix == ".stp"):
                self.__image = dakfile_processor.stp2im(image_str)
            else:
                raise RuntimeError("Unrecognized file suffix")
        else:
            self.__image = Image.open(image_str)
        self.__image = self.__image.convert("RGBA")

    def update_needles(self, start_needle, stop_needle):
        '''Updates the position of the start/stop needle visualisation'''
        self.__start_needle = start_needle
        self.__stop_needle = stop_needle
        self.refresh()

    @property
    def image(self):
        return self.__image

    @property
    def alignment(self):
        return self.__alignment

    def update_alignment(self, alignment):
        '''Updates the alignment of the image between start/stop needle'''
        self.__alignment = Alignment(alignment)
        self.refresh()

    @property
    def zoom(self):
        return self.__zoom

    @zoom.setter
    def zoom(self, event):
        '''Using mouse wheel events to zoom the pattern view'''
        if self.__image is not None:
            # angleDelta.y is 120 or -120 when scrolling
            zoom = event.angleDelta().y() / 120
            self.__zoom += zoom
            self.__zoom = max(1, self.__zoom)
            self.__zoom = min(5, self.__zoom)
            self.refresh()

    def invert_image(self):
        '''Public invert current Image function.'''
        self.apply_image_transform("invert")

    def repeat_image(self):
        '''Public repeat current Image function.'''
        v = QInputDialog.getInt(self.__parent,
                                "Repeat",
                                "Vertical",
                                value=1,
                                min=1)
        h = QInputDialog.getInt(self.__parent,
                                "Repeat",
                                "Horizontal",
                                value=1,
                                min=1,
                                max=ceil(Machine.WIDTH / self.__image.size[0]))
        self.apply_image_transform("repeat", v[0], h[0])

    def stretch_image(self):
        '''Public stretch current Image function.'''
        v = QInputDialog.getInt(self.__parent,
                                "Stretch",
                                "Vertical",
                                value=1,
                                min=1)
        h = QInputDialog.getInt(self.__parent,
                                "Stretch",
                                "Horizontal",
                                value=1,
                                min=1,
                                max=ceil(Machine.WIDTH / self.__image.size[0]))
        self.apply_image_transform("stretch", v[0], h[0])

    def reflect_image(self):
        '''Public reflect current Image function.'''
        m = Mirrors()
        if (m.result == QDialog.Accepted):
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
            image = transform(self.__image, args)
        except:
            logging.error("Error while executing image transform")
        if not image:
            return

        # Transition to NOT_CONFIGURED state
        self.__parent.signal_image_transformed.emit()

        # Update the view
        self.__image = image

        # Update maximum values
        width, height = self.__image.size
        self.__parent.plugin.set_image_dimensions(width, height)

        # Draw canvas
        self.refresh()
