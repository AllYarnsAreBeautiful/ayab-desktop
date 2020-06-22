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

from PIL import Image
from bitarray import bitarray
import numpy as np

MACHINE_WIDTH = 200


def array2rgb(a):
    return (a[0] & 0xFF) * 0x10000 + (a[1] & 0xFF) * 0x100 + (a[2] & 0xFF)


class ayabImage(object):
    def __init__(self, image, pNumColors=2):
        self.__numColors = pNumColors
        self.__imgPosition = 'center'
        self.__imgStartNeedle = 0
        self.__imgStopNeedle = 0
        self.__knitStartNeedle = 0
        self.__knitStopNeedle = MACHINE_WIDTH - 1
        self.__startLine = 0
        self.__image = image
        self.__updateImageData()
        return

    def imageIntern(self):
        return self.__imageIntern

    def imageExpanded(self):
        return self.__imageExpanded

    def imgWidth(self):
        return self.__imgWidth

    def imgHeight(self):
        return self.__imgHeight

    def knitStartNeedle(self):
        return self.__knitStartNeedle

    def knitStopNeedle(self):
        return self.__knitStopNeedle

    def imgStartNeedle(self):
        return self.__imgStartNeedle

    def imgStopNeedle(self):
        return self.__imgStopNeedle

    def imgPosition(self):
        return self.__imgPosition

    def startLine(self):
        return self.__startLine

    def numColors(self):
        return self.__numColors

    def __updateImageData(self):
        self.__imgWidth = self.__image.size[0]
        self.__imgHeight = self.__image.size[1]
        self.__convertImgToIntern()
        self.__calcImgStartStopNeedles()
        return

    def __convertImgToIntern(self):
        num_colors = self.__numColors
        imgWidth = self.__imgWidth
        imgHeight = self.__imgHeight

        self.__imageIntern = \
            [[0 for i in range(imgWidth)] for j in range(imgHeight)]
        self.__imageColors = \
            [[0 for i in range(num_colors)] for j in range(imgHeight)]  # unused?
        self.__imageExpanded = \
            [bitarray([False] * imgWidth) for j in range(num_colors * imgHeight)]

        # Limit number of colors in image
        # self.__image = self.__image.quantize(num_colors, dither=None)
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
            # self.__numColors = num_colors = actual_num_colors
            # TODO: reduce number of colors in configuration box
            pass

        # get palette
        rgb = self.__image.getpalette()[slice(0, 3 * num_colors)]
        col_array = np.reshape(rgb, (num_colors, 3))
        self.palette = list(map(array2rgb, col_array))

        # Make internal representations of image
        for row in range(imgHeight):
            for col in range(imgWidth):
                pxl = self.__image.getpixel((col, row))
                for color in range(num_colors):
                    if pxl == color:
                        # color map
                        self.__imageIntern[row][col] = color
                        # amount of bits per color per line
                        self.__imageColors[row][color] += 1
                        # colors separated per line
                        self.__imageExpanded[(num_colors * row)+color][col] = True
        return

    def __calcImgStartStopNeedles(self):
        if self.__imgPosition == 'center':
            needleWidth = self.__knitStopNeedle - self.__knitStartNeedle + 1
            self.__imgStartNeedle = int((self.__knitStartNeedle + needleWidth / 2) - self.__imgWidth / 2)
            self.__imgStopNeedle = self.__imgStartNeedle + self.__imgWidth - 1
        elif self.__imgPosition == 'left':
            self.__imgStartNeedle = self.__knitStartNeedle
            self.__imgStopNeedle = self.__imgStartNeedle + self.__imgWidth - 1
        elif self.__imgPosition == 'right':
            self.__imgStopNeedle = self.__knitStopNeedle
            self.__imgStartNeedle = self.__imgStopNeedle - self.__imgWidth + 1
        elif int(self.__imgPosition) > 0 and int(self.__imgPosition) < MACHINE_WIDTH:
            self.__imgStartNeedle = int(self.__imgPosition)
            self.__imgStopNeedle = self.__imgStartNeedle + self.__imgWidth - 1
        else:
            return False
        return True

    def setNumColors(self, pNumColors):
        """
        sets the number of colors the be used for knitting
        """
        # TODO use preferences or other options to set maximum number of colors
        if pNumColors > 1 and pNumColors < 7:
            self.__numColors = pNumColors
            self.__updateImageData()
        return

    def invertImage(self):
        """
        invert the pixels of the image
        """
        self.__image = self.__image.invert()
        return

    def rotateImage(self):
        """
        rotate the image 90 degrees clockwise
        """
        self.__image = self.__image.rotate(-90)
        self.__updateImageData()
        return

    def resizeImage(self, pNewWidth):
        """
        resize the image to a given width, keeping the aspect ratio
        """
        wpercent = (pNewWidth / float(self.__image.size[0]))
        hsize = int((float(self.__image.size[1]) * float(wpercent)))
        self.__image = self.__image.resize((pNewWidth, hsize), Image.ANTIALIAS)
        self.__updateImageData()
        return

    def repeatImage(self, pHorizontal=1, pVertical=1):
        """
        Repeat image.
        Repeat pHorizontal times horizontally, pVertical times vertically
        Sturla Lange 2017-12-30
        """
        old_h = self.__image.size[1]
        old_w = self.__image.size[0]
        new_h = old_h * pVertical
        new_w = old_w * pHorizontal
        new_im = Image.new('P', (new_w, new_h))
        for h in range(0, new_h, old_h):
            for w in range(0, new_w, old_w):
                new_im.paste(self.__image, (w, h))
        self.__image = new_im
        self.__updateImageData()
        return

    def setKnitNeedles(self, pKnitStart, pKnitStop):
        """
        set the start and stop needle
        """
        if (pKnitStart < pKnitStop) and pKnitStart >= 0 and pKnitStop < MACHINE_WIDTH:
            self.__knitStartNeedle = pKnitStart
            self.__knitStopNeedle = pKnitStop
        self.__updateImageData()
        return

    def setImagePosition(self, pImgPosition):
        """
        set the position of the pattern
        """
        if pImgPosition == 'left' or pImgPosition == 'center' or pImgPosition == 'right' \
            or (int(pImgPosition) >= 0 and int(pImgPosition) < MACHINE_WIDTH):
            self.__imgPosition = pImgPosition
            self.__updateImageData()
        return

    def setStartLine(self, pStartLine):
        """
        set the line where to start knitting
        """
        # Check if StartLine is in valid range (picture height)
        if pStartLine >= 0 and pStartLine < self.__image.size[1]:
            self.__startLine = pStartLine
        return
