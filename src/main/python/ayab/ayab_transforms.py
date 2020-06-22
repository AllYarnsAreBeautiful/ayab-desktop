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

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PIL import Image, ImageOps
import logging


class Transformable(Image.Image):
    """Image transforms for AYAB GUI.

    @author Tom Price
    @date   June 2020
    """

    def rotate(self, args):
        # TODO crop width if it exceeds the maximum after transform
        if not args:
            logging.debug("image not altered on _rotate_image.")
        logging.debug("rotating image")
        return Image.Image.rotate(self, args[0], expand=1)

    def invert(self, args=None):
        if self.mode == 'RGBA':
            r, g, b, a = self.split()
            rgb_image = Image.merge('RGB', (r, g, b))
            return ImageOps.invert(rgb_image)
        else:
            return ImageOps.invert(self)

    def hflip(self, args=None):
        return ImageOps.mirror(self)

    def vflip(self, args=None):
        return ImageOps.flip(self)

    def repeat(self, args):
        # TODO crop width if it exceeds the maximum after transform
        """
        Repeat image.
        Repeat pHorizontal times horizontally, pVertical times vertically
        Sturla Lange 2017-12-30
        """
        old_h = self.size[1]
        old_w = self.size[0]
        new_h = old_h * args[0] # pVertical
        new_w = old_w * args[1] # pHorizontal
        new_im = Image.new('RGB', (new_w, new_h))
        for h in range(0, new_h, old_h):
            for w in range(0, new_w, old_w):
                new_im.paste(self, (w, h))
        return new_im

    def reflect(self, args):
        # TODO crop width if it exceeds the maximum after transform
        """
        Reflect image.
        Mirrors Left, Right, Top, Bottom
        Tom Price 2020-06-01
        """
        mirrors = args[0]
        w = self.size[0]
        h = self.size[1]
        w0 = mirrors[0]
        h0 = mirrors[2]
        w1 = 1 + mirrors[0] + mirrors[1]
        h1 = 1 + mirrors[2] + mirrors[3]
        if w1 > 1:
            im = self
            self = Transformable.hflip(self)
            self = Transformable.repeat(self, (1, w1))
            for i in range(w0, w1, 2):
                self.paste(im, (i * w, 0))
        if h1 > 1:
            im = self
            self = Transformable.vflip(self)
            self = Transformable.repeat(self, (h1, 1))
            for i in range(h0, h1, 2):
                self.paste(im, (0, i * h))
        return self

    def stretch(self, args):
        # TODO crop width if it exceeds the maximum after transform
        """
        Stretch image.
        Stretch pHorizontal times horizontally, pVertical times vertically
        Tom Price 2020-05-30
        """
        old_h = self.size[1]
        old_w = self.size[0]
        new_h = old_h * args[0] # pVertical
        new_w = old_w * args[1] # pHorizontal
        return self.resize((new_w, new_h), Image.BOX)


class Mirrors:
    '''Image relection options and GUI methods'''

    def __init__(self):
        self.mirrors = [False, False, False, False]
        self.dialog = QtWidgets.QDialog()
        self.result = self.reflectDialog()

    def __toggled(self, box):
        self.mirrors[box] = not self.mirrors[box]

    def __toggled0(self):
        self.__toggled(0)

    def __toggled1(self):
        self.__toggled(1)

    def __toggled2(self):
        self.__toggled(2)

    def __toggled3(self):
        self.__toggled(3)

    def reflectDialog(self):
        self.dialog.setWindowTitle("Reflect image")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(200, 200)
        group = QtWidgets.QGroupBox("Add mirrors")
        group.setFlat(True)
        check0 = QtWidgets.QCheckBox("Left")
        check1 = QtWidgets.QCheckBox("Right")
        check2 = QtWidgets.QCheckBox("Top")
        check3 = QtWidgets.QCheckBox("Bottom")
        check0.toggled.connect(self.__toggled0)
        check1.toggled.connect(self.__toggled1)
        check2.toggled.connect(self.__toggled2)
        check3.toggled.connect(self.__toggled3)
        enter = QtWidgets.QPushButton("OK")
        enter.clicked.connect(self.dialog.accept)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(check0)
        layout.addWidget(check1)
        layout.addWidget(check2)
        layout.addWidget(check3)
        group.setLayout(layout)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(group)
        vbox.addWidget(enter)
        self.dialog.setLayout(vbox)
        return self.dialog.exec_()

