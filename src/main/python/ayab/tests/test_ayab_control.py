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
from ayab.plugins.ayab_plugin.ayab_control import AYABControl, KnittingMode
from ayab.plugins.ayab_plugin.ayab_image import ayabImage
from PIL import Image
from bitarray import bitarray

MACHINE_WIDTH = 200

class TestAYABControl(unittest.TestCase):
    def setUp(self):
        pass

    def test__singlebed(self):
        ayab_control = AYABControl()
        ayab_control.setImage(ayabImage(Image.new('P', (1, 3)), 2))
        ayab_control.setStartLine(0)
        ayab_control.setInfRepeat(False)
        assert ayab_control._singlebed(0) == (0, 0, False, False)
        assert ayab_control._singlebed(1) == (0, 2, False, False)
        assert ayab_control._singlebed(2) == (0, 4, False, True )
        ayab_control.setInfRepeat(True)
        assert ayab_control._singlebed(3) == (0, 0, False, False)
        assert ayab_control._singlebed(4) == (0, 2, False, False)
        ayab_control.setStartLine(1)
        assert ayab_control._singlebed(2) == (0, 0, False, False)

    def test__classic_ribber_2col(self):
        ayab_control = AYABControl()
        ayab_control.setImage(ayabImage(Image.new('P', (1, 5)), 2))
        ayab_control.setStartLine(0)
        ayab_control.setInfRepeat(False)
        assert ayab_control._classic_ribber_2col( 0) == (0, 0, False, False)
        assert ayab_control._classic_ribber_2col( 1) == (1, 1, False, False)
        assert ayab_control._classic_ribber_2col( 2) == (1, 3, False, False)
        assert ayab_control._classic_ribber_2col( 3) == (0, 2, False, False)
        assert ayab_control._classic_ribber_2col( 4) == (0, 4, False, False)
        assert ayab_control._classic_ribber_2col( 5) == (1, 5, False, False)
        assert ayab_control._classic_ribber_2col( 6) == (1, 7, False, False)
        assert ayab_control._classic_ribber_2col( 7) == (0, 6, False, False)
        assert ayab_control._classic_ribber_2col( 8) == (0, 8, False, False)
        assert ayab_control._classic_ribber_2col( 9) == (1, 9, False, True )
        ayab_control.setInfRepeat(True)
        assert ayab_control._classic_ribber_2col(10) == (1, 1, False, False)
        assert ayab_control._classic_ribber_2col(11) == (0, 0, False, False)
        assert ayab_control._classic_ribber_2col(12) == (0, 2, False, False)
        assert ayab_control._classic_ribber_2col(13) == (1, 3, False, False)
        ayab_control.setStartLine(1)
        assert ayab_control._classic_ribber_2col( 8) == (1, 1, False, False)

    def test__classic_ribber_multicol(self):
        ayab_control = AYABControl()
        ayab_control.setImage(ayabImage(Image.new('P', (1, 3)), 3))
        ayab_control.setNumColors(3)
        ayab_control.setStartLine(0)
        ayab_control.setInfRepeat(False)
        assert ayab_control._classic_ribber_multicol( 0) == (0, 0, False, False)
        assert ayab_control._classic_ribber_multicol( 1) == (0, 0, True , False)
        assert ayab_control._classic_ribber_multicol( 2) == (1, 1, False, False)
        assert ayab_control._classic_ribber_multicol( 3) == (1, 1, True , False)
        assert ayab_control._classic_ribber_multicol( 4) == (2, 2, False, False)
        assert ayab_control._classic_ribber_multicol( 5) == (2, 2, True , False)
        assert ayab_control._classic_ribber_multicol( 6) == (0, 3, False, False)
        assert ayab_control._classic_ribber_multicol( 7) == (0, 3, True , False)
        assert ayab_control._classic_ribber_multicol( 8) == (1, 4, False, False)
        assert ayab_control._classic_ribber_multicol( 9) == (1, 4, True , False)
        assert ayab_control._classic_ribber_multicol(10) == (2, 5, False, False)
        assert ayab_control._classic_ribber_multicol(11) == (2, 5, True , False)
        assert ayab_control._classic_ribber_multicol(12) == (0, 6, False, False)
        assert ayab_control._classic_ribber_multicol(13) == (0, 6, True , False)
        assert ayab_control._classic_ribber_multicol(14) == (1, 7, False, False)
        assert ayab_control._classic_ribber_multicol(15) == (1, 7, True , False)
        assert ayab_control._classic_ribber_multicol(16) == (2, 8, False, False)
        assert ayab_control._classic_ribber_multicol(17) == (2, 8, True , True )
        ayab_control.setInfRepeat(True)
        assert ayab_control._classic_ribber_multicol(18) == (0, 0, False, False)
        ayab_control.setStartLine(1)
        assert ayab_control._classic_ribber_multicol(12) == (0, 0, False, False)

    def test__middlecolorstwice_ribber(self):
        ayab_control = AYABControl()
        ayab_control.setImage(ayabImage(Image.new('P', (1, 5)), 3))
        ayab_control.setKnittingMode(KnittingMode.MIDDLECOLORSTWICE_RIBBER.value)
        ayab_control.setNumColors(3)
        ayab_control.setStartLine(0)
        ayab_control.setInfRepeat(False)
        ayab_control._get_knit_func()
        assert ayab_control._middlecolorstwice_ribber( 0) == (0,  0, False, False)
        assert ayab_control._middlecolorstwice_ribber( 1) == (2,  2, True , False)
        assert ayab_control._middlecolorstwice_ribber( 2) == (2,  2, False, False)
        assert ayab_control._middlecolorstwice_ribber( 3) == (1,  1, False, False)
        assert ayab_control._middlecolorstwice_ribber( 4) == (1,  4, False, False)
        assert ayab_control._middlecolorstwice_ribber( 5) == (2,  5, True , False)
        assert ayab_control._middlecolorstwice_ribber( 6) == (2,  5, False, False)
        assert ayab_control._middlecolorstwice_ribber( 7) == (0,  3, False, False)
        assert ayab_control._middlecolorstwice_ribber( 8) == (0,  6, False, False)
        assert ayab_control._middlecolorstwice_ribber( 9) == (2,  8, True , False)
        assert ayab_control._middlecolorstwice_ribber(10) == (2,  8, False, False)
        assert ayab_control._middlecolorstwice_ribber(11) == (1,  7, False, False)
        assert ayab_control._middlecolorstwice_ribber(12) == (1, 10, False, False)
        assert ayab_control._middlecolorstwice_ribber(13) == (2, 11, True , False)
        assert ayab_control._middlecolorstwice_ribber(14) == (2, 11, False, False)
        assert ayab_control._middlecolorstwice_ribber(15) == (0,  9, False, False)
        assert ayab_control._middlecolorstwice_ribber(16) == (0, 12, False, False)
        assert ayab_control._middlecolorstwice_ribber(17) == (2, 14, True , False)
        assert ayab_control._middlecolorstwice_ribber(18) == (2, 14, False, False)
        assert ayab_control._middlecolorstwice_ribber(19) == (1, 13, False, True )
        ayab_control.setInfRepeat(True)
        assert ayab_control._middlecolorstwice_ribber(20) == (1, 1, False, False)
        assert ayab_control._middlecolorstwice_ribber(21) == (2, 2, True , False)
        assert ayab_control._middlecolorstwice_ribber(22) == (2, 2, False, False)
        assert ayab_control._middlecolorstwice_ribber(23) == (0, 0, False, False)
        assert ayab_control._middlecolorstwice_ribber(24) == (0, 3, False, False)
        ayab_control.setStartLine(1)
        assert ayab_control._middlecolorstwice_ribber(16) == (1, 1, False, False)

    def test__heartofpluto_ribber(self):
        ayab_control = AYABControl()
        ayab_control.setImage(ayabImage(Image.new('P', (1, 5)), 3))
        ayab_control.setKnittingMode(KnittingMode.HEARTOFPLUTO_RIBBER.value)
        ayab_control.setNumColors(3)
        ayab_control.setStartLine(0)
        ayab_control.setInfRepeat(False)
        ayab_control._get_knit_func()
        assert ayab_control._heartofpluto_ribber( 0) == (2,  2, False, False)
        assert ayab_control._heartofpluto_ribber( 1) == (1,  1, False, False)
        assert ayab_control._heartofpluto_ribber( 2) == (1,  1, True , False)
        assert ayab_control._heartofpluto_ribber( 3) == (0,  0, False, False)
        assert ayab_control._heartofpluto_ribber( 4) == (0,  3, False, False)
        assert ayab_control._heartofpluto_ribber( 5) == (2,  5, False, False)
        assert ayab_control._heartofpluto_ribber( 6) == (2,  5, True , False)
        assert ayab_control._heartofpluto_ribber( 7) == (1,  4, False, False)
        assert ayab_control._heartofpluto_ribber( 8) == (1,  7, False, False)
        assert ayab_control._heartofpluto_ribber( 9) == (0,  6, False, False)
        assert ayab_control._heartofpluto_ribber(10) == (0,  6, True , False)
        assert ayab_control._heartofpluto_ribber(11) == (2,  8, False, False)
        assert ayab_control._heartofpluto_ribber(12) == (2, 11, False, False)
        assert ayab_control._heartofpluto_ribber(13) == (1, 10, False, False)
        assert ayab_control._heartofpluto_ribber(14) == (1, 10, True , False)
        assert ayab_control._heartofpluto_ribber(15) == (0,  9, False, False)
        assert ayab_control._heartofpluto_ribber(16) == (0, 12, False, False)
        assert ayab_control._heartofpluto_ribber(17) == (2, 14, False, False)
        assert ayab_control._heartofpluto_ribber(18) == (2, 14, True , False)
        assert ayab_control._heartofpluto_ribber(19) == (1, 13, False, True )
        ayab_control.setInfRepeat(True)
        assert ayab_control._heartofpluto_ribber(20) == (1,  1, False, False)
        assert ayab_control._heartofpluto_ribber(21) == (0,  0, False, False)
        assert ayab_control._heartofpluto_ribber(22) == (0,  0, True , False)
        assert ayab_control._heartofpluto_ribber(23) == (2,  2, False, False)
        assert ayab_control._heartofpluto_ribber(24) == (2,  5, False, False)
        ayab_control.setStartLine(1)
        assert ayab_control._heartofpluto_ribber(16) == (1,  1, False, False)

    def test__circular_ribber(self):
        ayab_control = AYABControl()
        ayab_control.setImage(ayabImage(Image.new('P', (1, 3)), 3))
        ayab_control.setNumColors(3)
        ayab_control.setStartLine(0)
        ayab_control.setInfRepeat(False)
        assert ayab_control._circular_ribber( 0) == (0, 0, False, False)
        assert ayab_control._circular_ribber( 1) == (0, 0, True , False)
        assert ayab_control._circular_ribber( 2) == (1, 1, False, False)
        assert ayab_control._circular_ribber( 3) == (1, 1, True , False)
        assert ayab_control._circular_ribber( 4) == (2, 2, False, False)
        assert ayab_control._circular_ribber( 5) == (2, 2, True , False)
        assert ayab_control._circular_ribber( 6) == (0, 3, False, False)
        assert ayab_control._circular_ribber( 7) == (0, 3, True , False)
        assert ayab_control._circular_ribber( 8) == (1, 4, False, False)
        assert ayab_control._circular_ribber( 9) == (1, 4, True , False)
        assert ayab_control._circular_ribber(10) == (2, 5, False, False)
        assert ayab_control._circular_ribber(11) == (2, 5, True , False)
        assert ayab_control._circular_ribber(12) == (0, 6, False, False)
        assert ayab_control._circular_ribber(13) == (0, 6, True , False)
        assert ayab_control._circular_ribber(14) == (1, 7, False, False)
        assert ayab_control._circular_ribber(15) == (1, 7, True , False)
        assert ayab_control._circular_ribber(16) == (2, 8, False, False)
        assert ayab_control._circular_ribber(17) == (2, 8, True , True )
        ayab_control.setInfRepeat(True)
        assert ayab_control._circular_ribber(18) == (0, 0, False, False)
        ayab_control.setStartLine(1)
        assert ayab_control._circular_ribber(12) == (0, 0, False, False)

    def test__select_needles(self):
        ayab_control = AYABControl()
        ayab_control.setNumColors(2)
        ayab_control.setStartLine(0)
        
        # 40 pixel image set to the center
        ayab_control.setKnittingMode(KnittingMode.CIRCULAR_RIBBER.value)
        im = ayabImage(Image.new('P', (40, 1)), 2)
        im.setImagePosition('left')
        ayab_control.setImage(im)
        bits0 = bitarray()
        bits0.frombytes(b'\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        assert ayab_control._select_needles(0, 0, False) == bits0
        
        # 40 pixel image set to the center
        im.setImagePosition('center')
        ayab_control.setImage(im)
        bits1 = bitarray()
        bits1.frombytes(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        assert ayab_control._select_needles(0, 0, False) == bits1
        
        # 40 pixel image set in the center
        # blank line so central 40 pixels unset
        # flanking pixels set (2 different options)
        ayab_control.setKnittingMode(KnittingMode.CLASSIC_RIBBER.value)
        assert ayab_control._select_needles(0, 0, True) == ~bits1
        ayab_control.setKnittingMode(KnittingMode.HEARTOFPLUTO_RIBBER.value)
        assert ayab_control._select_needles(0, 0, True) == ~bits1
        
        # image is wider than machine width
        # all pixels set
        ayab_control.setImage(ayabImage(Image.new('P', (202, 1)), 2))
        ayab_control.setKnittingMode(KnittingMode.MIDDLECOLORSTWICE_RIBBER.value)
        assert ayab_control._select_needles(0, 0, False) == bitarray([True] * MACHINE_WIDTH)
        
    def test_row_multiplier(self):
        assert KnittingMode(KnittingMode.SINGLEBED.value).row_multiplier(2) == 1
        assert KnittingMode(KnittingMode.CLASSIC_RIBBER.value).row_multiplier(2) == 2
        assert KnittingMode(KnittingMode.CLASSIC_RIBBER.value).row_multiplier(3) == 6
        assert KnittingMode(KnittingMode.MIDDLECOLORSTWICE_RIBBER.value).row_multiplier(3) == 4
        assert KnittingMode(KnittingMode.HEARTOFPLUTO_RIBBER.value).row_multiplier(4) == 6
        assert KnittingMode(KnittingMode.CIRCULAR_RIBBER.value).row_multiplier(2) == 4
        
    def test_good_ncolors(self):
        assert KnittingMode(KnittingMode.SINGLEBED.value).good_ncolors(2)
        assert not KnittingMode(KnittingMode.SINGLEBED.value).good_ncolors(3)
        assert KnittingMode(KnittingMode.CLASSIC_RIBBER.value).good_ncolors(2)
        assert KnittingMode(KnittingMode.CLASSIC_RIBBER.value).good_ncolors(3)
        assert KnittingMode(KnittingMode.MIDDLECOLORSTWICE_RIBBER.value).good_ncolors(2)
        assert KnittingMode(KnittingMode.MIDDLECOLORSTWICE_RIBBER.value).good_ncolors(3)
        assert KnittingMode(KnittingMode.HEARTOFPLUTO_RIBBER.value).good_ncolors(2)
        assert KnittingMode(KnittingMode.HEARTOFPLUTO_RIBBER.value).good_ncolors(3)
        assert KnittingMode(KnittingMode.CIRCULAR_RIBBER.value).good_ncolors(2)
        assert not KnittingMode(KnittingMode.CIRCULAR_RIBBER.value).good_ncolors(3)
        
    def test_knit_func(self):
        assert KnittingMode(KnittingMode.SINGLEBED.value).knit_func(2) == "_singlebed"
        assert KnittingMode(KnittingMode.CLASSIC_RIBBER.value).knit_func(2) == "_classic_ribber_2col"
        assert KnittingMode(KnittingMode.CLASSIC_RIBBER.value).knit_func(3) == "_classic_ribber_multicol"
        assert KnittingMode(KnittingMode.MIDDLECOLORSTWICE_RIBBER.value).knit_func(3) == "_middlecolorstwice_ribber"
        assert KnittingMode(KnittingMode.HEARTOFPLUTO_RIBBER.value).knit_func(4) == "_heartofpluto_ribber"
        assert KnittingMode(KnittingMode.CIRCULAR_RIBBER.value).knit_func(2) == "_circular_ribber"
        
    def test_flanking_needles(self):
        assert KnittingMode(KnittingMode.SINGLEBED.value).flanking_needles(0, 2)
        assert not KnittingMode(KnittingMode.SINGLEBED.value).flanking_needles(1, 2)
        assert KnittingMode(KnittingMode.CLASSIC_RIBBER.value).flanking_needles(0, 2)
        assert not KnittingMode(KnittingMode.CLASSIC_RIBBER.value).flanking_needles(1, 2)
        assert KnittingMode(KnittingMode.CLASSIC_RIBBER.value).flanking_needles(0, 3)
        assert not KnittingMode(KnittingMode.CLASSIC_RIBBER.value).flanking_needles(1, 3)
        assert not KnittingMode(KnittingMode.CLASSIC_RIBBER.value).flanking_needles(2, 3)
        assert KnittingMode(KnittingMode.MIDDLECOLORSTWICE_RIBBER.value).flanking_needles(0, 3)
        assert not KnittingMode(KnittingMode.MIDDLECOLORSTWICE_RIBBER.value).flanking_needles(1, 3)
        assert not KnittingMode(KnittingMode.MIDDLECOLORSTWICE_RIBBER.value).flanking_needles(2, 3)
        assert KnittingMode(KnittingMode.HEARTOFPLUTO_RIBBER.value).flanking_needles(0, 3)
        assert not KnittingMode(KnittingMode.HEARTOFPLUTO_RIBBER.value).flanking_needles(1, 3)
        assert not KnittingMode(KnittingMode.HEARTOFPLUTO_RIBBER.value).flanking_needles(2, 3)
        assert not KnittingMode(KnittingMode.CIRCULAR_RIBBER.value).flanking_needles(0, 2)
        assert not KnittingMode(KnittingMode.CIRCULAR_RIBBER.value).flanking_needles(1, 2)
