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
from ayab.plugins.ayab_plugin.ayab_control import AYABControl
from ayab.plugins.ayab_plugin.ayab_image import ayabImage
from PIL import Image
from bitarray import bitarray

MACHINE_WIDTH = 200

class TestAYABControl(unittest.TestCase):
    def setUp(self):
        pass

    def test__singlebed_2col(self):
        ayab_control = AYABControl()
        ayab_control._startLine = 0
        ayab_control._infRepeat = False
        assert ayab_control._singlebed_2col(0, 3) == (0, 0, 0, False, False)
        assert ayab_control._singlebed_2col(1, 3) == (1, 0, 2, False, False)
        assert ayab_control._singlebed_2col(2, 3) == (2, 0, 4, False, True )
        ayab_control._infRepeat = True
        assert ayab_control._singlebed_2col(3, 3) == (0, 0, 0, False, False)
        assert ayab_control._singlebed_2col(4, 3) == (1, 0, 2, False, False)
        ayab_control._startLine = 1
        assert ayab_control._singlebed_2col(2, 3) == (0, 0, 0, False, False)

    def test__doublebed_2col(self):
        ayab_control = AYABControl()
        ayab_control._startLine = 0
        ayab_control._infRepeat = False
        assert ayab_control._doublebed_2col( 0, 5) == (0, 0, 0, False, False)
        assert ayab_control._doublebed_2col( 1, 5) == (0, 1, 1, False, False)
        assert ayab_control._doublebed_2col( 2, 5) == (1, 1, 3, False, False)
        assert ayab_control._doublebed_2col( 3, 5) == (1, 0, 2, False, False)
        assert ayab_control._doublebed_2col( 4, 5) == (2, 0, 4, False, False)
        assert ayab_control._doublebed_2col( 5, 5) == (2, 1, 5, False, False)
        assert ayab_control._doublebed_2col( 6, 5) == (3, 1, 7, False, False)
        assert ayab_control._doublebed_2col( 7, 5) == (3, 0, 6, False, False)
        assert ayab_control._doublebed_2col( 8, 5) == (4, 0, 8, False, False)
        assert ayab_control._doublebed_2col( 9, 5) == (4, 1, 9, False, True )
        ayab_control._infRepeat = True
        assert ayab_control._doublebed_2col(10, 5) == (0, 1, 1, False, False)
        assert ayab_control._doublebed_2col(11, 5) == (0, 0, 0, False, False)
        assert ayab_control._doublebed_2col(12, 5) == (1, 0, 2, False, False)
        assert ayab_control._doublebed_2col(13, 5) == (1, 1, 3, False, False)
        ayab_control._startLine = 1
        assert ayab_control._doublebed_2col( 8, 5) == (0, 1, 1, False, False)

    def test__doublebed_multicol(self):
        ayab_control = AYABControl()
        ayab_control._numColors = 3
        ayab_control._startLine = 0
        ayab_control._infRepeat = False
        assert ayab_control._doublebed_multicol( 0, 3) == (0, 0, 0, False, False)
        assert ayab_control._doublebed_multicol( 1, 3) == (0, 0, 0, True , False)
        assert ayab_control._doublebed_multicol( 2, 3) == (0, 1, 1, False, False)
        assert ayab_control._doublebed_multicol( 3, 3) == (0, 1, 1, True , False)
        assert ayab_control._doublebed_multicol( 4, 3) == (0, 2, 2, False, False)
        assert ayab_control._doublebed_multicol( 5, 3) == (0, 2, 2, True , False)
        assert ayab_control._doublebed_multicol( 6, 3) == (1, 0, 3, False, False)
        assert ayab_control._doublebed_multicol( 7, 3) == (1, 0, 3, True , False)
        assert ayab_control._doublebed_multicol( 8, 3) == (1, 1, 4, False, False)
        assert ayab_control._doublebed_multicol( 9, 3) == (1, 1, 4, True , False)
        assert ayab_control._doublebed_multicol(10, 3) == (1, 2, 5, False, False)
        assert ayab_control._doublebed_multicol(11, 3) == (1, 2, 5, True , False)
        assert ayab_control._doublebed_multicol(12, 3) == (2, 0, 6, False, False)
        assert ayab_control._doublebed_multicol(13, 3) == (2, 0, 6, True , False)
        assert ayab_control._doublebed_multicol(14, 3) == (2, 1, 7, False, False)
        assert ayab_control._doublebed_multicol(15, 3) == (2, 1, 7, True , False)
        assert ayab_control._doublebed_multicol(16, 3) == (2, 2, 8, False, False)
        assert ayab_control._doublebed_multicol(17, 3) == (2, 2, 8, True , True )
        ayab_control._infRepeat = True
        assert ayab_control._doublebed_multicol(18, 3) == (0, 0, 0, False, False)
        ayab_control._startLine = 1
        assert ayab_control._doublebed_multicol(12, 3) == (0, 0, 0, False, False)

    def test__middlecoltwice(self):
        ayab_control = AYABControl()
        ayab_control._numColors = 3
        ayab_control._startLine = 0
        ayab_control._infRepeat = False
        assert ayab_control._middlecoltwice( 0, 5) == (0, 0,  0, False, False)
        assert ayab_control._middlecoltwice( 1, 5) == (0, 2,  2, True , False)
        assert ayab_control._middlecoltwice( 2, 5) == (0, 2,  2, False, False)
        assert ayab_control._middlecoltwice( 3, 5) == (0, 1,  1, False, False)
        assert ayab_control._middlecoltwice( 4, 5) == (1, 1,  4, False, False)
        assert ayab_control._middlecoltwice( 5, 5) == (1, 2,  5, True , False)
        assert ayab_control._middlecoltwice( 6, 5) == (1, 2,  5, False, False)
        assert ayab_control._middlecoltwice( 7, 5) == (1, 0,  3, False, False)
        assert ayab_control._middlecoltwice( 8, 5) == (2, 0,  6, False, False)
        assert ayab_control._middlecoltwice( 9, 5) == (2, 2,  8, True , False)
        assert ayab_control._middlecoltwice(10, 5) == (2, 2,  8, False, False)
        assert ayab_control._middlecoltwice(11, 5) == (2, 1,  7, False, False)
        assert ayab_control._middlecoltwice(12, 5) == (3, 1, 10, False, False)
        assert ayab_control._middlecoltwice(13, 5) == (3, 2, 11, True , False)
        assert ayab_control._middlecoltwice(14, 5) == (3, 2, 11, False, False)
        assert ayab_control._middlecoltwice(15, 5) == (3, 0,  9, False, False)
        assert ayab_control._middlecoltwice(16, 5) == (4, 0, 12, False, False)
        assert ayab_control._middlecoltwice(17, 5) == (4, 2, 14, True , False)
        assert ayab_control._middlecoltwice(18, 5) == (4, 2, 14, False, False)
        assert ayab_control._middlecoltwice(19, 5) == (4, 1, 13, False, True )
        ayab_control._infRepeat = True
        assert ayab_control._middlecoltwice(20, 5) == (0, 1, 1, False, False)
        assert ayab_control._middlecoltwice(21, 5) == (0, 2, 2, True , False)
        assert ayab_control._middlecoltwice(22, 5) == (0, 2, 2, False, False)
        assert ayab_control._middlecoltwice(23, 5) == (0, 0, 0, False, False)
        assert ayab_control._middlecoltwice(24, 5) == (1, 0, 3, False, False)
        ayab_control._startLine = 1
        assert ayab_control._middlecoltwice(16, 5) == (0, 1, 1, False, False)

    def test__heartofpluto(self):
        ayab_control = AYABControl()
        ayab_control._numColors = 3
        ayab_control._startLine = 0
        ayab_control._infRepeat = False
        assert ayab_control._heartofpluto( 0, 5) == (0, 2,  2, False, False)
        assert ayab_control._heartofpluto( 1, 5) == (0, 1,  1, False, False)
        assert ayab_control._heartofpluto( 2, 5) == (0, 1,  1, True , False)
        assert ayab_control._heartofpluto( 3, 5) == (0, 0,  0, False, False)
        assert ayab_control._heartofpluto( 4, 5) == (1, 0,  3, False, False)
        assert ayab_control._heartofpluto( 5, 5) == (1, 2,  5, False, False)
        assert ayab_control._heartofpluto( 6, 5) == (1, 2,  5, True , False)
        assert ayab_control._heartofpluto( 7, 5) == (1, 1,  4, False, False)
        assert ayab_control._heartofpluto( 8, 5) == (2, 1,  7, False, False)
        assert ayab_control._heartofpluto( 9, 5) == (2, 0,  6, False, False)
        assert ayab_control._heartofpluto(10, 5) == (2, 0,  6, True , False)
        assert ayab_control._heartofpluto(11, 5) == (2, 2,  8, False, False)
        assert ayab_control._heartofpluto(12, 5) == (3, 2, 11, False, False)
        assert ayab_control._heartofpluto(13, 5) == (3, 1, 10, False, False)
        assert ayab_control._heartofpluto(14, 5) == (3, 1, 10, True , False)
        assert ayab_control._heartofpluto(15, 5) == (3, 0,  9, False, False)
        assert ayab_control._heartofpluto(16, 5) == (4, 0, 12, False, False)
        assert ayab_control._heartofpluto(17, 5) == (4, 2, 14, False, False)
        assert ayab_control._heartofpluto(18, 5) == (4, 2, 14, True , False)
        assert ayab_control._heartofpluto(19, 5) == (4, 1, 13, False, True )
        ayab_control._infRepeat = True
        assert ayab_control._heartofpluto(20, 5) == (0, 1,  1, False, False)
        assert ayab_control._heartofpluto(21, 5) == (0, 0,  0, False, False)
        assert ayab_control._heartofpluto(22, 5) == (0, 0,  0, True , False)
        assert ayab_control._heartofpluto(23, 5) == (0, 2,  2, False, False)
        assert ayab_control._heartofpluto(24, 5) == (1, 2,  5, False, False)
        ayab_control._startLine = 1
        assert ayab_control._heartofpluto(16,5) == (0,1, 1,False,False)

    def test__circular_ribber(self):
        ayab_control = AYABControl()
        ayab_control._numColors = 3
        ayab_control._startLine = 0
        ayab_control._infRepeat = False
        assert ayab_control._circular_ribber( 0, 3) == (0, 0, 0, False, False)
        assert ayab_control._circular_ribber( 1, 3) == (0, 0, 0, True , False)
        assert ayab_control._circular_ribber( 2, 3) == (0, 1, 1, False, False)
        assert ayab_control._circular_ribber( 3, 3) == (0, 1, 1, True , False)
        assert ayab_control._circular_ribber( 4, 3) == (0, 2, 2, False, False)
        assert ayab_control._circular_ribber( 5, 3) == (0, 2, 2, True , False)
        assert ayab_control._circular_ribber( 6, 3) == (1, 0, 3, False, False)
        assert ayab_control._circular_ribber( 7, 3) == (1, 0, 3, True , False)
        assert ayab_control._circular_ribber( 8, 3) == (1, 1, 4, False, False)
        assert ayab_control._circular_ribber( 9, 3) == (1, 1, 4, True , False)
        assert ayab_control._circular_ribber(10, 3) == (1, 2, 5, False, False)
        assert ayab_control._circular_ribber(11, 3) == (1, 2, 5, True , False)
        assert ayab_control._circular_ribber(12, 3) == (2, 0, 6, False, False)
        assert ayab_control._circular_ribber(13, 3) == (2, 0, 6, True , False)
        assert ayab_control._circular_ribber(14, 3) == (2, 1, 7, False, False)
        assert ayab_control._circular_ribber(15, 3) == (2, 1, 7, True , False)
        assert ayab_control._circular_ribber(16, 3) == (2, 2, 8, False, False)
        assert ayab_control._circular_ribber(17, 3) == (2, 2, 8, True , True )
        ayab_control._infRepeat = True
        assert ayab_control._circular_ribber(18, 3) == (0, 0, 0, False, False)
        ayab_control._startLine = 1
        assert ayab_control._circular_ribber(12, 3) == (0, 0, 0, False, False)

    def test__select_needles(self):
        ayab_control = AYABControl()
        ayab_control._numColors = 3
        ayab_control._startLine = 0
        ayab_control._knitting_mode = 0
        ayab_control._image = ayabImage(Image.new('P', (40,1)), 2) # one line of black, 40 pixels wide
        
        # 40 pixel image set to the left
        ayab_control._image.setImagePosition('left')
        bits0 = bitarray()
        bits0.frombytes(b'\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        assert ayab_control._select_needles(0, 0, False) == bits0
        
        # 40 pixel image set to the center
        ayab_control._image.setImagePosition('center')
        bits1 = bitarray()
        bits1.frombytes(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        assert ayab_control._select_needles(0, 0, False) == bits1
        
        # 40 pixel image set in the center
        # blank line so central 40 pixels unset
        # flanking pixels set (2 different options)
        ayab_control._knitting_mode = 1
        assert ayab_control._select_needles(0, 0, True) == ~bits1
        ayab_control._knitting_mode = 3
        assert ayab_control._select_needles(2, 0, True) == ~bits1
        
        # image is wider than machine width
        # all pixels set
        ayab_control._image = ayabImage(Image.new('P', (202,1)), 2)
        ayab_control._knitting_mode = 2
        assert ayab_control._select_needles(0, 0, False) == bitarray([True] * MACHINE_WIDTH)
        
