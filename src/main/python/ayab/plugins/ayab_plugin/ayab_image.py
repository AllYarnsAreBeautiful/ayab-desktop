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
#    Copyright 2013-2020 Christian Obersteiner, Andreas Müller,
#    Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

from bitarray import bitarray
import numpy as np
from .ayab_options import Alignment
from .machine import Machine

class AyabImage (object):

    def __init__(self, image, num_colors=2):
        self.__image = image
        self.__num_colors = num_colors
        self.__alignment = Alignment.CENTER
        self.__img_start_needle = -1
        self.__img_stop_needle = -1
        self.__knit_start_needle = 0
        self.__knit_stop_needle = Machine.WIDTH - 1
        self.__update_image_data()
        return

    def __update_image_data(self):
        self.__img_width = self.__image.size[0]
        self.__img_height = self.__image.size[1]
        self.__convert()
        self.__calc_img_start_stop_needles()
        return

    def __convert(self):
        num_colors = self.__num_colors
        img_width = self.__img_width
        img_height = self.__img_height

        self.__image_intern = \
            [[0 for i in range(img_width)] for j in range(img_height)]
        self.__image_colors = \
            [[0 for i in range(num_colors)] for j in range(img_height)]  # unused?
        self.__image_expanded = \
            [bitarray([False] * img_width) for j in range(num_colors * img_height)]

        # Limit number of colors in image
        # self.image = self.image.quantize(num_colors, dither=None)
        self.__image = self.__image.quantize(num_colors)

        # Order colors most-frequent first
        # NB previously they were ordered lightest-first
        histogram = self.__image.histogram()
        dest_map = list(np.argsort(histogram[0:num_colors]))
        dest_map.reverse()
        self.__image = self.__image.remap_palette(dest_map)

        # reduce number of colors if necessary
        actual_num_colors = sum(map(lambda x: x > 0, self.__image.histogram()))
        if actual_num_colors < num_colors:
            # TODO: issue warning if number of colors is less than expected
            # TODO: reduce number of colors
            # self.num_colors = num_colors = actual_num_colors
            # TODO: reduce number of colors in configuration box
            pass

        # get palette
        rgb = self.__image.getpalette()[slice(0, 3 * num_colors)]
        col_array = np.reshape(rgb, (num_colors, 3))
        self.palette = list(map(self.array2rgb, col_array))

        # Make internal representations of image
        for row in range(img_height):
            for col in range(img_width):
                pxl = self.__image.getpixel((col, row))
                for color in range(num_colors):
                    if pxl == color:
                        # color map
                        self.__image_intern[row][col] = color
                        # amount of bits per color per line
                        self.__image_colors[row][color] += 1
                        # colors separated per line
                        self.__image_expanded[(num_colors * row)+color][col] = True
        return

    def __calc_img_start_stop_needles(self):
        if self.__alignment == Alignment.CENTER:
            needle_width = self.__knit_stop_needle - self.__knit_start_needle + 1
            self.__img_start_needle = int((self.__knit_start_needle + needle_width / 2) - self.img_width / 2)
            self.__img_stop_needle = self.__img_start_needle + self.__img_width - 1
        elif self.__alignment == Alignment.LEFT:
            self.__img_start_needle = self.__knit_start_needle
            self.__img_stop_needle = self.__img_start_needle + self.__img_width - 1
        elif self.__alignment == Alignment.RIGHT:
            self.__img_stop_needle = self.__knit_stop_needle
            self.__img_start_needle = self.__img_stop_needle - self.__img_width + 1
        # elif int(self.__alignment) > 0 and int(self.__alignment) < Machine.WIDTH:
        #     self.__img_start_needle = int(self.__alignment)
        #     self.__img_stop_needle = self.__img_start_needle + self.__img_width - 1
        else:
            return False
        return True

    def set_knit_needles(self, knit_start, knit_stop):
        """
        set the start and stop needle
        """
        if (knit_start < knit_stop) and knit_start >= 0 and knit_stop < Machine.WIDTH:
            self.__knit_start_needle = knit_start
            self.__knit_stop_needle = knit_stop
        self.__update_image_data()

    @property
    def num_colors(self):
        return self.__num_colors

    @num_colors.setter
    def num_colors(self, num_colors):
        """
        sets the number of colors used for knitting
        """
        # TODO use preferences or other options to set maximum number of colors
        if num_colors > 1 and num_colors < 7:
            self.__num_colors = num_colors
            self.__update_image_data()

    @property
    def alignment(self):
        return self.__alignment

    @alignment.setter
    def alignment(self, alignment):
        """
        set the position of the pattern
        """
        self.__alignment = alignment
        self.__update_image_data()

    @property
    def img_start_needle(self):
        return self.__img_start_needle

    @property
    def img_stop_needle(self):
        return self.__img_stop_needle

    @property
    def knit_start_needle(self):
        return self.__knit_start_needle

    @property
    def knit_stop_needle(self):
        return self.__knit_stop_needle

    @property
    def img_height(self):
        return self.__img_height

    @property
    def img_width(self):
        return self.__img_width

    @property
    def image_expanded(self):
        return self.__image_expanded

    def array2rgb(self, a):
        return (a[0] & 0xFF) * 0x10000 + (a[1] & 0xFF) * 0x100 + (a[2] & 0xFF)

    # def invert_image(self):
    #     """
    #     invert the pixels of the image
    #     """
    #     self.__image = self.__image.invert()
    #     return

    # def rotate_image(self):
    #     """
    #     rotate the image 90 degrees clockwise
    #     """
    #     self.__image = self.__image.rotate(-90)
    #     self.__update_image_data()
    #     return

    # def resize_image(self, new_width):
    #     """
    #     resize the image to a given width, keeping the aspect ratio
    #     """
    #     wpercent = (new_width / float(self.__image.size[0]))
    #     hsize = int((float(self.__image.size[1]) * float(wpercent)))
    #     self.__image = self.__image.resize((new_width, hsize), Image.ANTIALIAS)
    #     self.__update_image_data()
 
    # def repeat_image(self, horizontal=1, vertical=1):
    #     """
    #     Repeat image.
    #     Repeat pHorizontal times horizontally, pVertical times vertically
    #     Sturla Lange 2017-12-30
    #     """
    #     old_h = self.__image.size[1]
    #     old_w = self.__image.size[0]
    #     new_h = old_h * vertical
    #     new_w = old_w * horizontal
    #     new_im = Image.new('P', (new_w, new_h))
    #     for h in range(0, new_h, old_h):
    #         for w in range(0, new_w, old_w):
    #             new_im.paste(self.__image, (w, h))
    #     self.__image = new_im
    #     self.__update_image_data()

