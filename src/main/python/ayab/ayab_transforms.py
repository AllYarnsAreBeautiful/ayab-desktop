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

import logging
from PyQt5.QtWidgets import QDialog
from PIL import Image, ImageOps
from .ayab_mirrors import Ui_MirrorDialog


class Transform(Image.Image):
    """Image transforms for AYAB GUI.

    @author Tom Price
    @date   June 2020
    """
    def rotate_left(self, args=None):
        # TODO crop width if it exceeds the maximum after transform
        return self.transpose(Image.ROTATE_90)

    def rotate_right(self, args=None):
        # TODO crop width if it exceeds the maximum after transform
        return self.transpose(Image.ROTATE_270)

    def invert(self, args=None):
        if self.mode == 'RGBA':
            r, g, b, a = self.split()
            rgb_image = Image.merge('RGB', (r, g, b))
            return ImageOps.invert(rgb_image)
        else:
            return ImageOps.invert(self)

    def hflip(self, args=None):
        return self.transpose(Image.FLIP_LEFT_RIGHT)

    def vflip(self, args=None):
        return self.transpose(Image.FLIP_TOP_BOTTOM)

    def repeat(self, args):
        # TODO crop width if it exceeds the maximum after transform
        """
        Repeat image.
        Repeat `horizontal` times horizontally, `vertical` times vertically
        Sturla Lange 2017-12-30
        """
        old_h = self.size[1]
        old_w = self.size[0]
        new_h = old_h * args[0]  # pVertical
        new_w = old_w * args[1]  # pHorizontal
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
            self = self.Transform.hflip()
            self = self.Transform.repeat((1, w1))
            for i in range(w0, w1, 2):
                self.paste(im, (i * w, 0))
        if h1 > 1:
            im = self
            self = self.Transform.vflip()
            self = self.Transform.repeat((h1, 1))
            for i in range(h0, h1, 2):
                self.paste(im, (0, i * h))
        return self

    def stretch(self, args):
        # TODO crop width if it exceeds the maximum after transform
        """
        Stretch image.
        Repeat `horizontal` times horizontally, `vertical` times vertically
        Tom Price 2020-05-30
        """
        old_h = self.size[1]
        old_w = self.size[0]
        new_h = old_h * args[0]  # vertical
        new_w = old_w * args[1]  # horizontal
        return self.resize((new_w, new_h), Image.BOX)


class Mirrors:
    '''Image relection options and GUI methods'''
    def __init__(self):
        self.mirrors = [False, False, False, False]
        self.result = MirrorDialog(self).exec_()

    def toggled(self, box):
        self.mirrors[box] = not self.mirrors[box]


class MirrorDialog(QDialog):
    '''GUI to choose reflection options'''
    def __init__(self, parent):
        super(MirrorDialog, self).__init__(None)
        self.__ui = Ui_MirrorDialog()
        self.__ui.setupUi(self)
        self.__ui.check0.toggled.connect(lambda: parent.toggled(0))
        self.__ui.check1.toggled.connect(lambda: parent.toggled(1))
        self.__ui.check2.toggled.connect(lambda: parent.toggled(2))
        self.__ui.check3.toggled.connect(lambda: parent.toggled(3))
        self.__ui.enter.clicked.connect(self.accept)
