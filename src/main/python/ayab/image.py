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
from math import ceil

from PIL import Image
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QInputDialog, QDialog, QFileDialog

from .transforms import Transform, Mirrors
from .signal_sender import SignalSender
from .utils import display_blocking_popup
from .machine import Machine
from .pattern_import import PatPatternConverter, StpPatternConverter, CutPatternConverter


class AyabImage(SignalSender):
    """
    Image object with public methods for performing image actions from menu.
    Implemented as a subclass of SignalSender.

    @author Tom Price
    @date   July 2020
    """
    def __init__(self, parent):
        super().__init__(parent.signal_receiver)
        self.__parent = parent
        self.image = None
        self.filename = None
        self.filename_input = self.__parent.ui.filename_lineedit

    def select_file(self):
        filename = self.filename_input.text()
        if filename == '':
            filepath = self.__parent.app_context.get_resource("patterns")
        else:
            filepath = filename
        selected_file, _ = QFileDialog.getOpenFileName(
            self.__parent, "Open file", filepath,
            'Images (*.png *.PNG *.jpg *.JPG *.jpeg *.JPEG *.bmp *.BMP *.gif *.GIF *.tiff *.TIFF *.tif *.TIF *.Pat *.pat *.PAT *.Stp *.stp *.STP *.Cut *.cut *.CUT)'
        )
        if selected_file:
            self.filename = selected_file
            self.filename_input.setText(selected_file)
            self.__load(str(selected_file))

    def __load(self, filename):
        '''Load an image into the graphics scene.'''
        # TODO Check maximum width of image
        try:
            self.__open(filename)
        except (OSError, FileNotFoundError):
            display_blocking_popup(
                QCoreApplication.translate("Image", "Unable to load image file"),
                "error")  # FIXME translate
            logging.error("Unable to load " + str(filename))
        except Exception as e:
            display_blocking_popup(
                QCoreApplication.translate("Image", "Error loading image file"),
                "error")  # FIXME translate
            logging.error("Error loading image: " + str(e))
            raise
        else:
            # self.emit_statusbar_updater(filename, True)
            self.__parent.scene.row_progress = 0
            self.__parent.engine.config.refresh()

    def __open(self, filename):
        # check for files that need conversion
        suffix = filename[-4:].lower()
        if (suffix == ".pat"):
            self.image = PatPatternConverter().pattern2im(filename)
        elif (suffix == ".stp"):
            self.image = StpPatternConverter().pattern2im(filename)
        elif (suffix == ".cut"):
            self.image = CutPatternConverter().pattern2im(filename)
        else:
            self.image = Image.open(filename)
        self.image = self.image.convert("RGBA")
        self.emit_got_image_flag()
        self.emit_image_resizer()

    def invert(self):
        self.apply_transform(Transform.invert)

    def repeat(self):
        machine_width = Machine(self.__parent.prefs.value("machine")).width
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
                                max=ceil(machine_width / self.image.width))
        self.apply_transform(Transform.repeat, v[0], h[0])

    def stretch(self):
        machine_width = Machine(self.__parent.prefs.value("machine")).width
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
                                max=ceil(machine_width / self.image.width))
        self.apply_transform(Transform.stretch, v[0], h[0])

    def reflect(self):
        m = Mirrors()
        if (m.result == QDialog.Accepted):
            self.apply_transform(Transform.reflect, m.mirrors)

    def hflip(self):
        self.apply_transform(Transform.hflip)

    def vflip(self):
        self.apply_transform(Transform.vflip)

    def rotate_left(self):
        self.apply_transform(Transform.rotate_left)

    def rotate_right(self):
        self.apply_transform(Transform.rotate_right)

    def zoom_in(self):
        self.__parent.scene.set_zoom(+1)

    def zoom_out(self):
        self.__parent.scene.set_zoom(-1)

    def apply_transform(self, transform, *args):
        """Executes an image transform specified by function and args."""
        self.image = transform(self.image, args)
        try:
            pass #self.image = transform(self.image, args)
        except Exception as e:
            logging.error("Error while executing image transform: " + repr(e))

        # Update the view
        self.emit_image_resizer()

        # Transition to NOT_CONFIGURED state
        self.emit_new_image_flag()
