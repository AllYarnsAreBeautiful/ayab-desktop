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
#    Copyright 2014 Sebastian Oliva, Christian Obersteiner,
#       Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop
"""Provides conveniency functions to aproximately resize an image
(using a rational continued fraction aproximation.)"""

from __future__ import annotations
from typing import Any, Generator
from PIL import Image
from math import floor


def resize_image(
    image: Image.Image, width_proportion: float, height_proportion: float
) -> Image.Image:
    width, height = image.size
    resized_image = image.transform(
        (int(width_proportion * width), int(height_proportion * height)),
        Image.AFFINE,
        (1.0 / width_proportion, 0, 0, 0, 1.0 / height_proportion, 0),
        Image.NEAREST,
    )
    return resized_image


#  Based on code from:
#  https://groups.yahoo.com/neo/groups/tuning-math/conversations/topics/14958


def contfrac(a: int) -> list[int]:
    """Returns a list of terms for a continuated fraction."""
    terms = []
    count = 0
    b = 1
    while (b != 0) and (count < 7):  # 5 times, emprical accuracy measurement
        # limit
        terms.append(floor(a / (b + 0.0)))
        a, b = b, a % b
        count = count + 1
    return terms


def ra(
    x: int,
) -> Generator[tuple[int, int], int, Any]:  # 'rational approximation', or convergent
    """Generator for rational aproximation tuples of the float provided."""
    numerators = [0, 1]
    denominators = [1, 0]
    expansion = contfrac(x)  # call the contfrac function
    for num in expansion:  # [-1] and [-2] index 'previous'
        # and 'previous-previous'
        numerators.append((num * numerators[-1]) + numerators[-2])
        denominators.append((num * denominators[-1]) + denominators[-2])

    for index in range(len(numerators)):
        yield (numerators[index], denominators[index])
        # print "%i/%i" % (numerators[index], denominators[index])


def get_rational_ratios(ratio: int) -> list[tuple[int, int]]:
    ratios_list = list(ra(ratio))
    return ratios_list[2::]
