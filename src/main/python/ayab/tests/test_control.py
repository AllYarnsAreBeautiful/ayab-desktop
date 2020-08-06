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
#    Copyright 2020 Sebastian Oliva, Christian Obersteiner,
#    Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

import pytest
import unittest
from PIL import Image
from bitarray import bitarray

from ayab.engine.control import Control
from ayab.engine.options import Alignment
from ayab.engine.mode import Mode, ModeFunc
from ayab.engine.pattern import Pattern
from ayab.engine.status import Status
from ayab.machine import Machine


class Parent(object):
    def __init__(self):
        self.status = Status()


class TestControl(unittest.TestCase):
    def setUp(self):
        self.parent = Parent()

    def test__singlebed(self):
        control = Control(self.parent)
        control.pattern = Pattern(Image.new('P', (1, 3)), Machine(0), 2)
        control.num_colors = 2
        control.start_row = 0
        control.inf_repeat = False
        control.pat_height = control.pattern.pat_height
        control.func = getattr(ModeFunc, "_singlebed")
        assert control.func(control, 0) == (0, 0, False, False)
        assert control.func(control, 1) == (0, 2, False, False)
        assert control.func(control, 2) == (0, 4, False, True)
        control.inf_repeat = True
        assert control.func(control, 3) == (0, 0, False, False)
        assert control.func(control, 4) == (0, 2, False, False)
        control.start_row = 1
        assert control.func(control, 2) == (0, 0, False, False)

    def test__classic_ribber_2col(self):
        control = Control(self.parent)
        control.pattern = Pattern(Image.new('P', (1, 5)), Machine(0), 2)
        control.num_colors = 2
        control.start_row = 0
        control.inf_repeat = False
        control.pat_height = control.pattern.pat_height
        control.len_pat_expanded = control.pat_height * control.num_colors
        control.func = getattr(ModeFunc, "_classic_ribber_2col")
        assert control.func(control, 0) == (0, 0, False, False)
        assert control.func(control, 1) == (1, 1, False, False)
        assert control.func(control, 2) == (1, 3, False, False)
        assert control.func(control, 3) == (0, 2, False, False)
        assert control.func(control, 4) == (0, 4, False, False)
        assert control.func(control, 5) == (1, 5, False, False)
        assert control.func(control, 6) == (1, 7, False, False)
        assert control.func(control, 7) == (0, 6, False, False)
        assert control.func(control, 8) == (0, 8, False, False)
        assert control.func(control, 9) == (1, 9, False, True)
        control.inf_repeat = True
        assert control.func(control, 10) == (1, 1, False, False)
        assert control.func(control, 11) == (0, 0, False, False)
        assert control.func(control, 12) == (0, 2, False, False)
        assert control.func(control, 13) == (1, 3, False, False)
        control.start_row = 1
        assert control.func(control, 8) == (1, 1, False, False)

    def test__classic_ribber_multicol(self):
        control = Control(self.parent)
        control.pattern = Pattern(Image.new('P', (1, 3)), Machine(0), 3)
        control.num_colors = 3
        control.start_row = 0
        control.inf_repeat = False
        control.pat_height = control.pattern.pat_height
        control.len_pat_expanded = control.pat_height * control.num_colors
        control.func = getattr(ModeFunc, "_classic_ribber_multicol")
        assert control.func(control, 0) == (0, 0, False, False)
        assert control.func(control, 1) == (0, 0, True, False)
        assert control.func(control, 2) == (1, 1, False, False)
        assert control.func(control, 3) == (1, 1, True, False)
        assert control.func(control, 4) == (2, 2, False, False)
        assert control.func(control, 5) == (2, 2, True, False)
        assert control.func(control, 6) == (0, 3, False, False)
        assert control.func(control, 7) == (0, 3, True, False)
        assert control.func(control, 8) == (1, 4, False, False)
        assert control.func(control, 9) == (1, 4, True, False)
        assert control.func(control, 10) == (2, 5, False, False)
        assert control.func(control, 11) == (2, 5, True, False)
        assert control.func(control, 12) == (0, 6, False, False)
        assert control.func(control, 13) == (0, 6, True, False)
        assert control.func(control, 14) == (1, 7, False, False)
        assert control.func(control, 15) == (1, 7, True, False)
        assert control.func(control, 16) == (2, 8, False, False)
        assert control.func(control, 17) == (2, 8, True, True)
        control.inf_repeat = True
        assert control.func(control, 18) == (0, 0, False, False)
        control.start_row = 1
        assert control.func(control, 12) == (0, 0, False, False)

    def test__middlecolorstwice_ribber(self):
        control = Control(self.parent)
        control.pattern = Pattern(Image.new('P', (1, 5)), Machine(0), 3)
        control.mode = Mode.MIDDLECOLORSTWICE_RIBBER
        control.num_colors = 3
        control.start_row = 0
        control.inf_repeat = False
        control.pat_height = control.pattern.pat_height
        control.len_pat_expanded = control.pat_height * control.num_colors
        control.passes_per_row = control.mode.row_multiplier(
            control.num_colors)
        control.func = getattr(ModeFunc, "_middlecolorstwice_ribber")
        assert control.func(control, 0) == (0, 0, False, False)
        assert control.func(control, 1) == (2, 2, True, False)
        assert control.func(control, 2) == (2, 2, False, False)
        assert control.func(control, 3) == (1, 1, False, False)
        assert control.func(control, 4) == (1, 4, False, False)
        assert control.func(control, 5) == (2, 5, True, False)
        assert control.func(control, 6) == (2, 5, False, False)
        assert control.func(control, 7) == (0, 3, False, False)
        assert control.func(control, 8) == (0, 6, False, False)
        assert control.func(control, 9) == (2, 8, True, False)
        assert control.func(control, 10) == (2, 8, False, False)
        assert control.func(control, 11) == (1, 7, False, False)
        assert control.func(control, 12) == (1, 10, False, False)
        assert control.func(control, 13) == (2, 11, True, False)
        assert control.func(control, 14) == (2, 11, False, False)
        assert control.func(control, 15) == (0, 9, False, False)
        assert control.func(control, 16) == (0, 12, False, False)
        assert control.func(control, 17) == (2, 14, True, False)
        assert control.func(control, 18) == (2, 14, False, False)
        assert control.func(control, 19) == (1, 13, False, True)
        control.inf_repeat = True
        assert control.func(control, 20) == (1, 1, False, False)
        assert control.func(control, 21) == (2, 2, True, False)
        assert control.func(control, 22) == (2, 2, False, False)
        assert control.func(control, 23) == (0, 0, False, False)
        assert control.func(control, 24) == (0, 3, False, False)
        control.start_row = 1
        assert control.func(control, 16) == (1, 1, False, False)

    def test__heartofpluto_ribber(self):
        control = Control(self.parent)
        control.pattern = Pattern(Image.new('P', (1, 5)), Machine(0), 3)
        control.mode = Mode.HEARTOFPLUTO_RIBBER
        control.num_colors = 3
        control.start_row = 0
        control.inf_repeat = False
        control.pat_height = control.pattern.pat_height
        control.len_pat_expanded = control.pat_height * control.num_colors
        control.passes_per_row = control.mode.row_multiplier(
            control.num_colors)
        control.func = getattr(ModeFunc, "_heartofpluto_ribber")
        assert control.func(control, 0) == (2, 2, False, False)
        assert control.func(control, 1) == (1, 1, False, False)
        assert control.func(control, 2) == (1, 1, True, False)
        assert control.func(control, 3) == (0, 0, False, False)
        assert control.func(control, 4) == (0, 3, False, False)
        assert control.func(control, 5) == (2, 5, False, False)
        assert control.func(control, 6) == (2, 5, True, False)
        assert control.func(control, 7) == (1, 4, False, False)
        assert control.func(control, 8) == (1, 7, False, False)
        assert control.func(control, 9) == (0, 6, False, False)
        assert control.func(control, 10) == (0, 6, True, False)
        assert control.func(control, 11) == (2, 8, False, False)
        assert control.func(control, 12) == (2, 11, False, False)
        assert control.func(control, 13) == (1, 10, False, False)
        assert control.func(control, 14) == (1, 10, True, False)
        assert control.func(control, 15) == (0, 9, False, False)
        assert control.func(control, 16) == (0, 12, False, False)
        assert control.func(control, 17) == (2, 14, False, False)
        assert control.func(control, 18) == (2, 14, True, False)
        assert control.func(control, 19) == (1, 13, False, True)
        control.inf_repeat = True
        assert control.func(control, 20) == (1, 1, False, False)
        assert control.func(control, 21) == (0, 0, False, False)
        assert control.func(control, 22) == (0, 0, True, False)
        assert control.func(control, 23) == (2, 2, False, False)
        assert control.func(control, 24) == (2, 5, False, False)
        control.start_row = 1
        assert control.func(control, 16) == (1, 1, False, False)

    def test__circular_ribber(self):
        control = Control(self.parent)
        control.pattern = Pattern(Image.new('P', (1, 3)), Machine(0), 3)
        control.num_colors = 3
        control.start_row = 0
        control.inf_repeat = False
        control.pat_height = control.pattern.pat_height
        control.len_pat_expanded = control.pat_height * control.num_colors
        control.func = getattr(ModeFunc, "_circular_ribber")
        assert control.func(control, 0) == (0, 0, False, False)
        assert control.func(control, 1) == (0, 0, True, False)
        assert control.func(control, 2) == (1, 1, False, False)
        assert control.func(control, 3) == (1, 1, True, False)
        assert control.func(control, 4) == (2, 2, False, False)
        assert control.func(control, 5) == (2, 2, True, False)
        assert control.func(control, 6) == (0, 3, False, False)
        assert control.func(control, 7) == (0, 3, True, False)
        assert control.func(control, 8) == (1, 4, False, False)
        assert control.func(control, 9) == (1, 4, True, False)
        assert control.func(control, 10) == (2, 5, False, False)
        assert control.func(control, 11) == (2, 5, True, False)
        assert control.func(control, 12) == (0, 6, False, False)
        assert control.func(control, 13) == (0, 6, True, False)
        assert control.func(control, 14) == (1, 7, False, False)
        assert control.func(control, 15) == (1, 7, True, False)
        assert control.func(control, 16) == (2, 8, False, False)
        assert control.func(control, 17) == (2, 8, True, True)
        control.inf_repeat = True
        assert control.func(control, 18) == (0, 0, False, False)
        control.start_row = 1
        assert control.func(control, 12) == (0, 0, False, False)

    def test_select_needles_API6(self):
        control = Control(self.parent)
        control.machine = Machine(0)
        control.num_colors = 2
        control.start_row = 0

        # 40 pixel image set to the left
        control.mode = Mode.SINGLEBED
        im = Image.new('P', (40, 3), 0)
        im1 = Image.new('P', (40, 1), 1)
        im.paste(im1, (0, 0))
        pattern = Pattern(im, Machine(0), 2)
        pattern.alignment = Alignment.LEFT
        control.pattern = pattern
        assert pattern.pat_start_needle == 0
        assert pattern.pat_stop_needle == 39
        bits0 = bitarray()
        bits0.frombytes(
            b'\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
        )
        assert control.select_needles_API6(0, 0, False) == bits0

        # 40 pixel image set to the center
        pattern.alignment = Alignment.CENTER
        control.pattern = pattern
        bits1 = bitarray()
        bits1.frombytes(
            b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
        )
        assert control.select_needles_API6(0, 0, False) == bits1

        # 40 pixel image set in the center
        # blank line so central 40 pixels unset
        # flanking pixels set (2 different options)
        control.mode = Mode.CLASSIC_RIBBER
        assert control.select_needles_API6(2, 1, False) == ~bits1
        control.mode = Mode.MIDDLECOLORSTWICE_RIBBER
        assert control.select_needles_API6(2, 1, False) == ~bits1

        # image is wider than machine width
        # all pixels set
        control.pattern = Pattern(Image.new('P', (202, 1)), Machine(0), 2)
        assert control.select_needles_API6(0, 0, False) == bitarray(
            [True] * Machine(0).width)

    def test_row_multiplier(self):
        assert Mode.SINGLEBED.row_multiplier(2) == 1
        assert Mode.CLASSIC_RIBBER.row_multiplier(2) == 2
        assert Mode.CLASSIC_RIBBER.row_multiplier(3) == 6
        assert Mode.MIDDLECOLORSTWICE_RIBBER.row_multiplier(3) == 4
        assert Mode.HEARTOFPLUTO_RIBBER.row_multiplier(4) == 6
        assert Mode.CIRCULAR_RIBBER.row_multiplier(2) == 4

    def test_good_ncolors(self):
        assert Mode.SINGLEBED.good_ncolors(2)
        assert not Mode.SINGLEBED.good_ncolors(3)
        assert Mode.CLASSIC_RIBBER.good_ncolors(2)
        assert Mode.CLASSIC_RIBBER.good_ncolors(3)
        assert Mode.MIDDLECOLORSTWICE_RIBBER.good_ncolors(2)
        assert Mode.MIDDLECOLORSTWICE_RIBBER.good_ncolors(3)
        assert Mode.HEARTOFPLUTO_RIBBER.good_ncolors(2)
        assert Mode.HEARTOFPLUTO_RIBBER.good_ncolors(3)
        assert Mode.CIRCULAR_RIBBER.good_ncolors(2)
        assert not Mode.CIRCULAR_RIBBER.good_ncolors(3)

    def test_knit_func(self):
        assert Mode.SINGLEBED.knit_func(2) == "_singlebed"
        assert Mode.CLASSIC_RIBBER.knit_func(2) == "_classic_ribber_2col"
        assert Mode.CLASSIC_RIBBER.knit_func(3) == "_classic_ribber_multicol"
        assert Mode.MIDDLECOLORSTWICE_RIBBER.knit_func(
            3) == "_middlecolorstwice_ribber"
        assert Mode.HEARTOFPLUTO_RIBBER.knit_func(4) == "_heartofpluto_ribber"
        assert Mode.CIRCULAR_RIBBER.knit_func(2) == "_circular_ribber"

    def test_flanking_needles(self):
        assert Mode.SINGLEBED.flanking_needles(0, 2)
        assert not Mode.SINGLEBED.flanking_needles(1, 2)
        assert Mode.CLASSIC_RIBBER.flanking_needles(0, 2)
        assert not Mode.CLASSIC_RIBBER.flanking_needles(1, 2)
        assert Mode.CLASSIC_RIBBER.flanking_needles(0, 3)
        assert not Mode.CLASSIC_RIBBER.flanking_needles(1, 3)
        assert not Mode.CLASSIC_RIBBER.flanking_needles(2, 3)
        assert Mode.MIDDLECOLORSTWICE_RIBBER.flanking_needles(0, 3)
        assert not Mode.MIDDLECOLORSTWICE_RIBBER.flanking_needles(1, 3)
        assert not Mode.MIDDLECOLORSTWICE_RIBBER.flanking_needles(2, 3)
        assert Mode.HEARTOFPLUTO_RIBBER.flanking_needles(0, 3)
        assert not Mode.HEARTOFPLUTO_RIBBER.flanking_needles(1, 3)
        assert not Mode.HEARTOFPLUTO_RIBBER.flanking_needles(2, 3)
        assert Mode.CIRCULAR_RIBBER.flanking_needles(0, 2)
        assert not Mode.CIRCULAR_RIBBER.flanking_needles(1, 2)
