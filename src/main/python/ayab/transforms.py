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
from PIL import Image, ImageOps

from PyQt5.QtWidgets import QDialog

from .mirrors_gui import Ui_Mirrors


class Transform(Image.Image):
    """
    Image transforms for AYAB GUI called by `AyabImage.apply_transform()`

    @author Tom Price
    @date   June 2020
    """
    def rotate_left(image, args=None):
        # TODO crop width if it exceeds the maximum after transform
        return image.transpose(Image.ROTATE_90)

    def rotate_right(image, args=None):
        # TODO crop width if it exceeds the maximum after transform
        return image.transpose(Image.ROTATE_270)

    def invert(image, args=None):
        if image.mode == 'RGBA':
            r, g, b, a = image.split()
            rgb_image = Image.merge('RGB', (r, g, b))
            return ImageOps.invert(rgb_image)
        else:
            return ImageOps.invert(image)

    def hflip(image, args=None):
        return image.transpose(Image.FLIP_LEFT_RIGHT)

    def vflip(image, args=None):
        return image.transpose(Image.FLIP_TOP_BOTTOM)

    def repeat(image, args):
        # TODO crop width if it exceeds the maximum after transform
        """
        Repeat image.
        Repeat `args[1]` times horizontally, `args[0]` times vertically
        Sturla Lange 2017-12-30
        """
        old_w, old_h = image.size
        new_h = old_h * args[0]  # Vertical
        new_w = old_w * args[1]  # Horizontal
        new_im = Image.new('RGB', (new_w, new_h))
        for h in range(0, new_h, old_h):
            for w in range(0, new_w, old_w):
                new_im.paste(image, (w, h))
        return new_im

    def reflect(image, args):
        # TODO crop width if it exceeds the maximum after transform
        """
        Reflect image: Mirrors Left, Right, Top, Bottom.

        @author Tom Price
        @date   June 2020
        """
        mirrors = args[0]
        w, h = image.size
        w0, w_, h0, h_ = mirrors
        w1 = 1 + w0 + w_
        h1 = 1 + h0 + h_
        if w1 > 1:
            im = image
            image = Transform.hflip(image)
            image = Transform.repeat(image, (1, w1))
            for i in range(w0, w1, 2):
                image.paste(im, (i * w, 0))
        if h1 > 1:
            im = image
            image = Transform.vflip(image)
            image = Transform.repeat(image, (h1, 1))
            for i in range(h0, h1, 2):
                image.paste(im, (0, i * h))
        return image

    def stretch(image, args):
        # TODO crop width if it exceeds the maximum after transform
        """
        Stretch image `args[1]` times horizontally, `args[0]` times vertically.

        @author Tom Price
        @date   May 2020
        """
        old_w, old_h = image.size
        new_h = old_h * args[0]  # vertical
        new_w = old_w * args[1]  # horizontal
        return image.resize((new_w, new_h), Image.BOX)


class Mirrors:
    '''
    Image relection options and GUI methods.

    @author Tom Price
    @date   June 2020
    '''
    def __init__(self):
        self.mirrors = [0, 0, 0, 0]
        self.result = MirrorDialog(self).exec_()

    def toggled(self, box):
        self.mirrors[box] = 1 - self.mirrors[box]


class MirrorDialog(QDialog):
    '''
    GUI to choose reflection options.

    @author Tom Price
    @date   June 2020
    '''
    def __init__(self, parent):
        super().__init__()  # FIXME set the parent widget as GuiMain
        self.__ui = Ui_Mirrors()
        self.__ui.setupUi(self)
        self.__ui.check0.toggled.connect(lambda: parent.toggled(0))
        self.__ui.check1.toggled.connect(lambda: parent.toggled(1))
        self.__ui.check2.toggled.connect(lambda: parent.toggled(2))
        self.__ui.check3.toggled.connect(lambda: parent.toggled(3))
        self.__ui.enter.clicked.connect(self.accept)
