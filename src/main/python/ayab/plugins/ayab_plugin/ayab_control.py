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

import logging
from enum import Enum
from bitarray import bitarray
from PyQt5.QtCore import QCoreApplication
from . import ayab_image
from .ayab_progress import Progress
from .ayab_communication import AyabCommunication
from .ayab_communication_mockup import AyabCommunicationMockup
from .ayab_options import KnittingMode, Alignment
from .machine import Machine


class KnittingState(Enum):
    NONE = 0
    SETUP = 1
    INIT = 2
    WAIT_FOR_INIT = 3
    START = 4
    OPERATE = 5
    FINISHED = 6


class AyabControlKnitResult(Enum):
    NONE = 0
    ERROR_INVALID_SETTINGS = 1
    ERROR_SERIAL_PORT = 2
    CONNECTING_TO_MACHINE = 3
    WAIT_FOR_INIT = 4
    ERROR_WRONG_API = 5
    PLEASE_KNIT = 6
    DEVICE_NOT_READY = 7
    FINISHED = 8


def even(x):
    return x % 2 == 0

def odd(x):
    return x % 2 == 1


class AyabControl(object):
    BLOCK_LENGTH = 256
    COLOR_SYMBOLS = "A", "B", "C", "D"
    API_VERSION = 0x05
    FLANKING_NEEDLES = True

    def __init__(self):
        self.__logger = logging.getLogger(type(self).__name__)
        self.__progress = Progress()
        self.__current_state = KnittingState.SETUP

    def reset(self):
        self.__current_state = KnittingState.SETUP
        self.__former_request = 0
        self.__line_block = 0
        self.__img_row = 0
        self.__inf_repeat_repeats = 0
        self.__progress.reset()

    @property
    def progress(self):
        return self.__progress

    def close(self):
        self.__com.close_serial()
        self.reset()

    def get_row_multiplier(self):
        return self.knitting_mode.row_multiplier(self.num_colors)

    def get_knit_func(self):
        '''Select function that decides which line of data to send according to the machine type and number of colors'''
        if not self.knitting_mode.good_ncolors(self.num_colors):
            self.__logger.error("Wrong number of colours for the knitting mode")
            return False
        # else
        func_name = self.knitting_mode.knit_func(self.num_colors)
        if not hasattr(AyabControl, func_name):
            self.__logger.error("Unrecognized value returned from KnittingMode.knit_func()")
            return False
        # else
        self.__knit_func = getattr(AyabControl, func_name)
        self.__passes_per_row = self.knitting_mode.row_multiplier(self.num_colors)
        return True

    def check_serial(self):
        msg, token, param = self.__com.update()
        if token == "cnfInfo":
            self.__log_cnfInfo(msg)
        elif token == "indState":
            self.__progress.get_carriage_info(msg)
        return token, param

    def __log_cnfInfo(self, msg):
        api = msg[1]
        log = "API v" + str(api)
        if api >= 5:
            log += ", FW v" + str(msg[2]) + "." + str(msg[3])
        self.__logger.info(log)
        return

    def __cnfLine(self, line_number):
        if line_number < self.BLOCK_LENGTH:
            # TODO some better algorithm for block wrapping
            if self.__former_request == self.BLOCK_LENGTH - 1 and line_number == 0:
                # wrap to next block of lines
                self.__line_block += 1

            # store requested line number for next request
            self.__former_request = line_number
            requested_line = line_number

            # adjust line_number with current block
            line_number += self.BLOCK_LENGTH * self.__line_block

            # get data for next line of knitting
            color, row_index, blank_line, last_line = self.__knit_func(self, line_number)
            bits = self.select_needles(color, row_index, blank_line)

            # send line to machine
            self.__com.cnf_line(requested_line, bits.tobytes(), last_line and not self.inf_repeat)

            # screen output
            msg = str(self.__line_block) + " " + str(line_number) + " reqLine: " + \
                str(requested_line) + " img_row: " + str(self.__img_row)
            if blank_line:
                msg += " BLANK LINE"
            else:
                msg += " row_index: " + str(row_index)
                msg += " color: " + str(self.COLOR_SYMBOLS[color])
            self.__logger.debug(msg)

            # get line progress to send to GUI
            self.__get_progress(line_number, color, bits)

        else:
            self.__logger.error("Requested line number out of range")
            return True # stop knitting

        if not last_line:
            return False # keep knitting
        elif self.inf_repeat:
            self.__inf_repeat_repeats += 1
            return False # keep knitting
        else:
            return True  # image finished

    def __get_progress(self, line_number, color, bits):
        self.__progress.current_row = self.__img_row + 1
        self.__progress.total_rows = self.image.img_height
        self.__progress.line_number = line_number
        if self.inf_repeat:
            self.__progress.repeats = self.__inf_repeat_repeats
        if self.knitting_mode == KnittingMode.SINGLEBED:
            self.__progress.alt_color = self.image.palette[1]
            self.__progress.color_symbol = "A/B"
        else:
            self.__progress.alt_color = None
            self.__progress.color_symbol = self.COLOR_SYMBOLS[color]
        self.__progress.color = self.image.palette[color]
        if self.FLANKING_NEEDLES:
            self.__progress.bits = bits[self.image.knit_start_needle:self.image.knit_stop_needle + 1]
        else:
            self.__progress.bits = bits[self.__first_needle:self.__last_needle]

    def select_needles(self, color, row_index, blank_line):
        bits = bitarray([False] * Machine.WIDTH, endian="little")
        first_needle = max(0, self.image.img_start_needle)
        last_needle = min(self.image.img_width + self.image.img_start_needle, Machine.WIDTH)

        # select needles flanking the image if necessary to knit the background color
        if self.knitting_mode.flanking_needles(color, self.num_colors):
            bits[0:first_needle] = True
            bits[last_needle:Machine.WIDTH] = True

        if not blank_line:
            first_pixel = first_needle - self.image.img_start_needle
            last_pixel = last_needle - self.image.img_start_needle
            bits[first_needle:last_needle] = (self.image.image_expanded)[row_index][first_pixel:last_pixel]

        self.__first_needle = first_needle
        self.__last_needle = last_needle
        return bits
    
    # singlebed, 2 color
    def _singlebed(self, line_number):
        img_height = self.image.img_height
        line_number += self.start_row

        # when knitting infinitely, keep the requested
        # line_number in its limits
        if self.inf_repeat:
            line_number %= img_height
        self.__img_row = line_number

        # 0   1   2   3   4 .. (img_row)
        # |   |   |   |   |
        # 0 1 2 3 4 5 6 7 8 .. (row_index)

        # color is always 0 in singlebed,
        # because both colors are knitted at once
        color = 0

        row_index = 2 * self.__img_row

        blank_line = False

        # Check if the last line of the image was requested
        last_line = (self.__img_row == img_height - 1)

        return color, row_index, blank_line, last_line

    # doublebed, 2 color
    def _classic_ribber_2col(self, line_number):
        img_height = self.image.img_height
        len_img_expanded = 2 * img_height
        
        line_number += 2 * self.start_row

        # calculate line number index for colors
        i = line_number % 4

        # when knitting infinitely, keep the requested
        # line_number in its limits
        if self.inf_repeat:
            line_number %= len_img_expanded

        self.__img_row = line_number // 2

        # 0 0 1 1 2 2 3 3 4 4 .. (img_row)
        # 0 1 2 3 4 5 6 7 8 9 .. (line_number)
        # | |  X  | |  X  | |
        # 0 1 3 2 4 5 7 6 8 9 .. (row_index)
        # A B B A A B B A A B .. (color)

        color = [0, 1, 1, 0][i] # 0 = A, 1 = B

        row_index = (line_number + [0, 0, 1, -1][i]) % len_img_expanded

        blank_line = False

        last_line = (self.__img_row == img_height - 1) and (i == 1 or i == 3)

        return color, row_index, blank_line, last_line

    # doublebed, multicolor
    def _classic_ribber_multicol(self, line_number):
        len_img_expanded = self.num_colors * self.image.img_height
        
        # halve line_number because every second line is BLANK
        blank_line = odd(line_number)
        h = line_number // 2

        h += self.num_colors * self.start_row

        # when knitting infinitely, keep the
        # half line_number within its limits
        if self.inf_repeat:
            h %= len_img_expanded

        self.__img_row, color = divmod(h, self.num_colors)

        row_index = self.__img_row * self.num_colors + color

        last_line = (row_index == len_img_expanded - 1) and blank_line

        if not blank_line:
            self.__logger.debug("COLOR " + str(color))

        return color, row_index, blank_line, last_line

    # Ribber, Middle-Colors-Twice
    def _middlecolorstwice_ribber(self, line_number):
        img_height = self.image.img_height

        # doublebed middle-colors-twice multicolor
        # 0-00 1-11 2-22 3-33 4-44 5-55 .. (img_row)
        # 0123 4567 8911 1111 1111 2222 .. (line_number)
        #             01 2345 6789 0123
        #
        # 0-21 4-53 6-87 1-19 1-11 1-11 .. (row_index)
        #                0 1  2 43 6 75
        #
        # A-CB B-CA A-CB B-CA A-CB B-CA .. (color)

        line_number += self.__passes_per_row * self.start_row

        self.__img_row, r = divmod(line_number, self.__passes_per_row)

        first_col = (r == 0)
        last_col = (r == self.__passes_per_row - 1)

        if first_col or last_col:
            color = (last_col + self.__img_row) % 2
        else:
            color = (r + 3) // 2

        if self.inf_repeat:
            self.__img_row %= img_height

        row_index = self.num_colors * self.__img_row + color

        blank_line = not first_col and not last_col and odd(line_number)

        last_line = (self.__img_row == img_height - 1) and last_col

        return color, row_index, blank_line, last_line

    # doublebed, multicolor <3 of pluto
    # rotates middle colors
    def _heartofpluto_ribber(self, line_number):
        img_height = self.image.img_height
        
        # doublebed <3 of pluto multicolor
        # 0000 1111 2222 3333 4444 5555 .. (img_row)
        # 0123 4567 8911 1111 1111 2222 .. (line_number)
        #             01 2345 6789 0123
        #
        # 02-1 35-4 76-8 11-9 11-1 11-1 .. (row_index)
        #                10   24 3 65 7
        #
        # CB-A AC-B BA-C CB-A AC-B BA-C .. (color)

        line_number += self.__passes_per_row * self.start_row

        self.__img_row, r = divmod(line_number, self.__passes_per_row)

        if self.inf_repeat:
            self.__img_row %= img_height

        first_col = (r == 0)
        last_col = (r == self.__passes_per_row - 1)

        color = self.num_colors - 1 - ((line_number + 1) % (2 * self.num_colors)) // 2

        row_index = self.num_colors * self.__img_row + color

        blank_line = not first_col and not last_col and even(line_number)

        last_line = (self.__img_row == img_height - 1) and last_col

        return color, row_index, blank_line, last_line

    # Ribber, Circular
    # not restricted to 2 colors
    def _circular_ribber(self, line_number):
        len_img_expanded = self.num_colors * self.image.img_height
        
        # A B  A B  A B  .. (color)
        # 0-0- 1-1- 2-2- .. (img_row)
        # 0 1  2 3  4 5  .. (row_index)
        # 0123 4567 8911 .. (line_number)
        #             01

        # halve line_number because every second line is BLANK
        blank_line = odd(line_number)
        h = line_number // 2

        h += self.num_colors * self.start_row

        if self.inf_repeat:
            h %= len_img_expanded

        self.__img_row, color = divmod(h, self.num_colors)

        row_index = h

        last_line = (row_index == len_img_expanded - 1) and blank_line

        return color, row_index, blank_line, last_line

    def knit(self, image, options):
        '''Finite State Machine governing serial communication'''
        result = AyabControlKnitResult.NONE

        if self.__current_state != KnittingState.SETUP:
            rcvMsg, rcvParam = self.check_serial()

        if self.__current_state == KnittingState.SETUP:
            self.reset()
            self.image = image
            self.start_row = options.start_row
            self.num_colors = options.num_colors
            self.knitting_mode = options.knitting_mode
            self.inf_repeat = options.inf_repeat

            if not self.get_knit_func():
                result = AyabControlKnitResult.ERROR_INVALID_SETTINGS
            else:
                if options.portname == QCoreApplication.translate("AyabPlugin", "Simulation"):
                    self.__com = AyabCommunicationMockup()
                else:
                    self.__com = AyabCommunication()
 
                if not self.__com.open_serial(options.portname):
                    self.__logger.error("Could not open serial port")
                    result = AyabControlKnitResult.ERROR_SERIAL_PORT
 
                self.__current_state = KnittingState.INIT

        elif self.__current_state == KnittingState.INIT:
            if rcvMsg == 'cnfInfo':
                if rcvParam == self.API_VERSION:
                    self.__current_state = KnittingState.WAIT_FOR_INIT
                    result = AyabControlKnitResult.WAIT_FOR_INIT
                else:
                    self.__logger.error("wrong API version: " + str(rcvParam) + ", " +
                                        "expected: " + str(self.API_VERSION))
                    result = AyabControlKnitResult.ERROR_WRONG_API
            else:
                self.__com.req_info()
                result = AyabControlKnitResult.CONNECTING_TO_MACHINE

        elif self.__current_state == KnittingState.WAIT_FOR_INIT:
            if rcvMsg == "indState":
                if rcvParam == 1:
                    self.__com.req_start(self.image.knit_start_needle,
                                         self.image.knit_stop_needle,
                                         options.continuous_reporting)
                    self.__current_state = KnittingState.START
                else:
                    self.__logger.debug("init failed")

        elif self.__current_state == KnittingState.START:
            if rcvMsg == 'cnfStart':
                if rcvParam == 1:
                    self.__current_state = KnittingState.OPERATE
                    result = AyabControlKnitResult.PLEASE_KNIT
                else:
                    self.__logger.error("device not ready")
                    result = AyabControlKnitResult.DEVICE_NOT_READY

        elif self.__current_state == KnittingState.OPERATE:
            if rcvMsg == 'reqLine':
                imageFinished = self.__cnfLine(rcvParam)
                if imageFinished:
                    self.__current_state = KnittingState.SETUP
                    result = AyabControlKnitResult.FINISHED

        return result
