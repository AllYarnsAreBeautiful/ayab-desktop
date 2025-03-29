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

from __future__ import annotations
from typing import cast
from bitarray import bitarray
import numpy as np
import numpy.typing as npt
from PIL import Image
from .options import Alignment, OptionsTab
from .mode import Mode
from ..machine import Machine


class Pattern(object):
    def __init__(self, image: Image.Image, config: OptionsTab, num_colors: int = 2):
        self.__pattern = (
            image.transpose(Image.FLIP_LEFT_RIGHT) if config.auto_mirror else image
        )
        self.__num_colors = num_colors
        self.__alignment = Alignment.CENTER
        self.__pat_start_needle: int = -1
        self.__pat_end_needle: int = -1
        self.__knit_start_needle: int = 0
        self.__mode: Mode = config.mode
        self.__knit_end_needle: int = config.machine.width
        self.__update_pattern_data()

    def __update_pattern_data(self) -> None:
        self.__pat_width = self.__pattern.width
        self.__pat_height = self.__pattern.height
        self.__convert()
        self.__calc_pat_start_end_needles()

    def __convert(self) -> None:
        # num_colors = self.__num_colors
        # pat_width = self.__pat_width
        # pat_height = self.__pat_height

        self.__pattern_intern = [
            [0 for i in range(self.__pat_width)] for j in range(self.__pat_height)
        ]
        self.__pattern_colors = [
            [0 for i in range(self.__num_colors)] for j in range(self.__pat_height)
        ]  # unused
        self.__pattern_expanded = [
            bitarray(self.__pat_width)
            for j in range(self.__num_colors * self.__pat_height)
        ]

        # Limit number of colors in pattern
        # self.__pattern = self.__pattern.quantize(num_colors, dither=None)
        self.__pattern = self.__pattern.quantize(self.__num_colors)

        # Order colors most-frequent first
        # NB previously they were ordered lightest-first
        histogram = self.__pattern.histogram()
        if self.__mode != Mode.SINGLEBED:
            dest_map = list(np.argsort(histogram[0 : self.__num_colors]))
        else:
            # For single bed, leave the colors as is but
            # map them down to [0:__num_colors]
            # https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.remap_palette
            # `list(range(256))` is the identity tranform
            dest_map = list(range(self.__num_colors))

        # reverse it to get to zero as the first color
        dest_map.reverse()
        self.__pattern = self.__pattern.remap_palette(dest_map)

        # reduce number of colors if necessary
        actual_num_colors = sum(map(lambda x: x > 0, self.__pattern.histogram()))
        if actual_num_colors < self.__num_colors:
            # TODO: issue warning if number of colors is less than expected
            # TODO: reduce number of colors
            # self.__num_colors = num_colors = actual_num_colors
            # TODO: reduce number of colors in configuration box
            pass

        # get palette
        rgb = self.__pattern.getpalette()[
            slice(0, 3 * self.__num_colors)
        ]  # type: ignore
        col_array = cast(npt.NDArray[np.int_], np.reshape(rgb, (self.__num_colors, 3)))
        self.palette = list(map(self.array2rgb, col_array))

        # Make internal representations of pattern
        for row in range(self.__pat_height):
            for col in range(self.__pat_width):
                pxl = self.__pattern.getpixel((col, row))
                for color in range(self.__num_colors):
                    if pxl == color:
                        # color map
                        self.__pattern_intern[row][col] = color
                        # amount of bits per color per line
                        self.__pattern_colors[row][color] += 1
                        # colors separated per line
                        self.__pattern_expanded[(self.__num_colors * row) + color][
                            col
                        ] = True

    def __calc_pat_start_end_needles(self) -> bool:
        if self.__alignment == Alignment.CENTER:
            needle_width = self.__knit_end_needle - self.__knit_start_needle
            self.__pat_start_needle = (
                self.__knit_start_needle + (needle_width - self.pat_width + 1) // 2
            )
            self.__pat_end_needle = self.__pat_start_needle + self.__pat_width
        elif self.__alignment == Alignment.LEFT:
            self.__pat_start_needle = self.__knit_start_needle
            self.__pat_end_needle = self.__pat_start_needle + self.__pat_width
        elif self.__alignment == Alignment.RIGHT:
            self.__pat_end_needle = self.__knit_end_needle
            self.__pat_start_needle = self.__pat_end_needle - self.__pat_width
        else:
            return False
        return True

    def set_knit_needles(
        self, knit_start: int, knit_stop: int, machine: Machine
    ) -> None:
        """
        set the start and stop needle
        """
        if knit_start < knit_stop and knit_start >= 0 and knit_stop < machine.width:
            self.__knit_start_needle = knit_start
            self.__knit_end_needle = knit_stop + 1
        self.__update_pattern_data()

    @property
    def num_colors(self) -> int:
        return self.__num_colors

    @num_colors.setter
    def num_colors(self, num_colors: int) -> None:
        """
        sets the number of colors used for knitting
        """
        # TODO use preferences or other options to set maximum number of colors
        if num_colors > 1 and num_colors < 7:
            self.__num_colors = num_colors
            self.__update_pattern_data()

    @property
    def alignment(self) -> Alignment:
        return self.__alignment

    @alignment.setter
    def alignment(self, alignment: Alignment) -> None:
        """
        set the position of the pattern
        """
        self.__alignment = alignment
        self.__update_pattern_data()

    @property
    def pat_start_needle(self) -> int:
        return self.__pat_start_needle

    @property
    def pat_end_needle(self) -> int:
        return self.__pat_end_needle

    @property
    def knit_start_needle(self) -> int:
        return self.__knit_start_needle

    @property
    def knit_end_needle(self) -> int:
        return self.__knit_end_needle

    @property
    def pat_height(self) -> int:
        return self.__pat_height

    @property
    def pat_width(self) -> int:
        return self.__pat_width

    @property
    def pattern_expanded(self) -> list[bitarray]:
        return self.__pattern_expanded

    def array2rgb(self, a: list[int]) -> int:
        return (a[0] & 0xFF) * 0x10000 + (a[1] & 0xFF) * 0x100 + (a[2] & 0xFF)
