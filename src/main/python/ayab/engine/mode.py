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
#    Copyright 2013-2020 Sebastian Oliva, Christian Obersteiner,
#    Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

from __future__ import annotations

from enum import Enum

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QComboBox

from ..utils import odd, even
from typing import TYPE_CHECKING, Callable, TypeAlias

if TYPE_CHECKING:
    from .control import Control


class Mode(Enum):
    SINGLEBED = 0
    CLASSIC_RIBBER = 1
    MIDDLECOLORSTWICE_RIBBER = 2
    HEARTOFPLUTO_RIBBER = 3
    CIRCULAR_RIBBER = 4

    def row_multiplier(self, ncolors: int) -> int:
        if self.name == "SINGLEBED":
            return 1
        if (
            self.name == "CLASSIC_RIBBER" and ncolors > 2
        ) or self.name == "CIRCULAR_RIBBER":
            # every second line is blank
            return 2 * ncolors
        if (
            self.name == "MIDDLECOLORSTWICE_RIBBER"
            or self.name == "HEARTOFPLUTO_RIBBER"
        ):
            # only middle lines doubled
            return 2 * ncolors - 2
        else:
            # one line per color
            return ncolors

    def good_ncolors(self, ncolors: int) -> int:
        if self.name == "SINGLEBED" or self.name == "CIRCULAR_RIBBER":
            return ncolors == 2
        else:
            # no maximum
            return ncolors >= 2

    def knit_func(self, ncolors: int) -> str:
        method = "_" + self.name.lower()
        if self.name == "CLASSIC_RIBBER":
            method += ["_2col", "_multicol"][ncolors > 2]
        return method

    # FIXME this function is supposed to select needles
    # to knit the background color alongside the pattern
    def flanking_needles(self, color: int, ncolors: int) -> bool:
        # return (color == 0 and self.name == "CLASSIC_RIBBER") \
        #     or (color == ncolors - 1
        #         and (self.name == "MIDDLECOLORSTWICE_RIBBER"
        #             or self.name == "HEARTOFPLUTO_RIBBER"))
        return color == 0  # and self.name != "CIRCULAR_RIBBER"

    @staticmethod
    def add_items(box: QComboBox) -> None:
        tr_ = QCoreApplication.translate
        box.addItem(tr_("KnitMode", "Singlebed"))
        box.addItem(tr_("KnitMode", "Ribber: Classic"))
        box.addItem(tr_("KnitMode", "Ribber: Middle-Colors-Twice"))
        box.addItem(tr_("KnitMode", "Ribber: Heart of Pluto"))
        box.addItem(tr_("KnitMode", "Ribber: Circular"))


if TYPE_CHECKING:
    ModeTuple: TypeAlias = tuple[int, int, bool, bool]
    ModeFuncType: TypeAlias = Callable[[Control, int], ModeTuple]


class ModeFunc(object):
    """
    Methods available to `AyabControl.func_selector()`.

    @author Tom Price
    @date   June 2020
    """

    # singlebed, 2 color
    @staticmethod
    def _singlebed(control: Control, line_number: int) -> ModeTuple:
        line_number += control.start_row

        # when knitting infinitely, keep the requested
        # line_number in its limits
        if control.inf_repeat:
            line_number %= control.pat_height
        control.pat_row = line_number

        # 0   1   2   3   4 .. (pat_row)
        # |   |   |   |   |
        # 0 1 2 3 4 5 6 7 8 .. (row_index)

        # color is always 0 in singlebed,
        # because both colors are knitted at once
        color = 0

        row_index = 2 * control.pat_row

        blank_line = False

        # Check if the last line of the pattern was requested
        last_line = control.pat_row == control.pat_height - 1

        return color, row_index, blank_line, last_line

    # doublebed, 2 color
    @staticmethod
    def _classic_ribber_2col(control: Control, line_number: int) -> ModeTuple:
        line_number += 2 * control.start_row

        # calculate line number index for colors
        i = line_number % 4

        # when knitting infinitely, keep the requested
        # line_number in its limits
        if control.inf_repeat:
            line_number %= control.len_pat_expanded

        control.pat_row = line_number // 2

        # 0 0 1 1 2 2 3 3 4 4 .. (pat_row)
        # 0 1 2 3 4 5 6 7 8 9 .. (line_number)
        # | |  X  | |  X  | |
        # 0 1 3 2 4 5 7 6 8 9 .. (row_index)
        # A B B A A B B A A B .. (color)

        color = [0, 1, 1, 0][i]  # 0 = A, 1 = B

        row_index = (line_number + [0, 0, 1, -1][i]) % control.len_pat_expanded

        blank_line = False

        last_line = (control.pat_row == control.pat_height - 1) and (i == 1 or i == 3)

        return color, row_index, blank_line, last_line

    # doublebed, multicolor
    @staticmethod
    def _classic_ribber_multicol(control: Control, line_number: int) -> ModeTuple:

        # halve line_number because every second line is BLANK
        blank_line = odd(line_number)
        h = line_number // 2

        h += control.num_colors * control.start_row

        # when knitting infinitely, keep the
        # half line_number within its limits
        if control.inf_repeat:
            h %= control.len_pat_expanded

        control.pat_row, color = divmod(h, control.num_colors)

        row_index = control.pat_row * control.num_colors + color

        last_line = (row_index == control.len_pat_expanded - 1) and blank_line

        if not blank_line:
            control.logger.debug("COLOR " + str(color))

        return color, row_index, blank_line, last_line

    # Ribber, Middle-Colors-Twice
    @staticmethod
    def _middlecolorstwice_ribber(control: Control, line_number: int) -> ModeTuple:

        # doublebed middle-colors-twice multicolor
        # 0-00 1-11 2-22 3-33 4-44 5-55 .. (pat_row)
        # 0123 4567 8911 1111 1111 2222 .. (line_number)
        #             01 2345 6789 0123
        #
        # 0-21 4-53 6-87 1-19 1-11 1-11 .. (row_index)
        #                0 1  2 43 6 75
        #
        # A-CB B-CA A-CB B-CA A-CB B-CA .. (color)

        line_number += control.passes_per_row * control.start_row

        control.pat_row, r = divmod(line_number, control.passes_per_row)

        first_col = r == 0
        last_col = r == control.passes_per_row - 1

        if first_col or last_col:
            color = (last_col + control.pat_row) % 2
        else:
            color = (r + 3) // 2

        if control.inf_repeat:
            control.pat_row %= control.pat_height

        row_index = control.num_colors * control.pat_row + color

        blank_line = not first_col and not last_col and odd(line_number)

        last_line = (control.pat_row == control.pat_height - 1) and last_col

        return color, row_index, blank_line, last_line

    # doublebed, multicolor <3 of pluto
    # rotates middle colors
    @staticmethod
    def _heartofpluto_ribber(control: Control, line_number: int) -> ModeTuple:

        # doublebed <3 of pluto multicolor
        # 0000 1111 2222 3333 4444 5555 .. (pat_row)
        # 0123 4567 8911 1111 1111 2222 .. (line_number)
        #             01 2345 6789 0123
        #
        # 02-1 35-4 76-8 11-9 11-1 11-1 .. (row_index)
        #                10   24 3 65 7
        #
        # CB-A AC-B BA-C CB-A AC-B BA-C .. (color)

        line_number += control.passes_per_row * control.start_row

        control.pat_row, r = divmod(line_number, control.passes_per_row)

        if control.inf_repeat:
            control.pat_row %= control.pat_height

        first_col = r == 0
        last_col = r == control.passes_per_row - 1

        color = (
            control.num_colors - 1 - ((line_number + 1) % (2 * control.num_colors)) // 2
        )

        row_index = control.num_colors * control.pat_row + color

        blank_line = not first_col and not last_col and even(line_number)

        last_line = (control.pat_row == control.pat_height - 1) and last_col

        return color, row_index, blank_line, last_line

    # Ribber, Circular
    # not restricted to 2 colors
    @staticmethod
    def _circular_ribber(control: Control, line_number: int) -> ModeTuple:

        # A B  A B  A B  .. (color)
        # 0-0- 1-1- 2-2- .. (pat_row)
        # 0 1  2 3  4 5  .. (row_index)
        # 0123 4567 8911 .. (line_number)
        #             01

        # halve line_number because every second line is BLANK
        blank_line = odd(line_number)
        h = line_number // 2

        h += control.num_colors * control.start_row

        if control.inf_repeat:
            h %= control.len_pat_expanded

        control.pat_row, color = divmod(h, control.num_colors)

        row_index = h

        last_line = (row_index == control.len_pat_expanded - 1) and blank_line

        return color, row_index, blank_line, last_line
