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
from .ayab_status import Status
from .ayab_communication import AyabCommunication, MessageToken
from .ayab_communication_mockup import AyabCommunicationMockup
from .ayab_options import Alignment
from .ayab_knit_mode import KnitMode, KnitModeFunc
from .ayab_knit_state import KnitState, KnitStateMachine
from .ayab_knit_output import KnitOutput
from .machine import Machine


class AyabControl(object):
    BLOCK_LENGTH = 256
    COLOR_SYMBOLS = "A", "B", "C", "D"
    API_VERSION = 0x05
    FLANKING_NEEDLES = True

    def __init__(self):
        self.logger = logging.getLogger(type(self).__name__)
        self.status = Status()
        self.state = KnitState.SETUP

    def close(self):
        try:
            self.com.close_serial()
        except Exception:
            pass
        self.state = KnitState.SETUP

    def row_multiplier(self):
        return self.knit_mode.row_multiplier(self.num_colors)

    def func_selector(self):
        '''Select function that decides which line of data to send according to the knitting mode and number of colors'''
        if not self.knit_mode.good_ncolors(self.num_colors):
            self.logger.error("Wrong number of colours for the knitting mode")
            return False
        # else
        func_name = self.knit_mode.knit_func(self.num_colors)
        if not hasattr(KnitModeFunc, func_name):
            self.logger.error(
                "Unrecognized value returned from KnitMode.knit_func()")
            return False
        # else
        self.knit_mode_func = getattr(KnitModeFunc, func_name)
        return True

    def check_serial(self):
        msg, token, param = self.com.update()
        if token == MessageToken.cnfInfo:
            self.__log_cnfInfo(msg)
        elif token == MessageToken.indState:
            self.status.get_carriage_info(msg)
        return token, param

    def __log_cnfInfo(self, msg):
        api = msg[1]
        log = "API v" + str(api)
        if api >= 5:
            log += ", FW v" + str(msg[2]) + "." + str(msg[3])
        self.logger.info(log)

    def cnf_line(self, line_number):
        if line_number < self.BLOCK_LENGTH:
            # TODO some better algorithm for block wrapping
            if self.former_request == self.BLOCK_LENGTH - 1 and line_number == 0:
                # wrap to next block of lines
                self.line_block += 1

            # store requested line number for next request
            self.former_request = line_number
            requested_line = line_number

            # adjust line_number with current block
            line_number += self.BLOCK_LENGTH * self.line_block

            # get data for next line of knitting
            color, row_index, blank_line, last_line = self.knit_mode_func(
                self, line_number)
            bits = self.select_needles(color, row_index, blank_line)

            # send line to machine
            self.com.cnf_line(requested_line, bits.tobytes(), last_line
                              and not self.inf_repeat)

            # screen output
            msg = str(self.line_block) + " " + str(line_number) + " reqLine: " + \
                str(requested_line) + " pat_row: " + str(self.pat_row)
            if blank_line:
                msg += " BLANK LINE"
            else:
                msg += " row_index: " + str(row_index)
                msg += " color: " + str(self.COLOR_SYMBOLS[color])
            self.logger.debug(msg)

            # get status to send to GUI
            self.__get_status(line_number, color, bits)

        else:
            self.logger.error("Requested line number out of range")
            return True  # stop knitting

        if not last_line:
            return False  # keep knitting
        elif self.inf_repeat:
            self.pattern_repeats += 1
            return False  # keep knitting
        else:
            return True  # pattern finished

    def __get_status(self, line_number, color, bits):
        self.status.current_row = self.pat_row + 1
        self.status.total_rows = self.pattern.pat_height
        self.status.line_number = line_number
        if self.inf_repeat:
            self.status.repeats = self.pattern_repeats
        if self.knit_mode == KnitMode.SINGLEBED:
            self.status.alt_color = self.pattern.palette[1]
            self.status.color_symbol = "A/B"
        else:
            self.status.alt_color = None
            self.status.color_symbol = self.COLOR_SYMBOLS[color]
        self.status.color = self.pattern.palette[color]
        if self.FLANKING_NEEDLES:
            self.status.bits = bits[self.pattern.knit_start_needle:self.
                                    pattern.knit_stop_needle + 1]
        else:
            self.status.bits = bits[self.__first_needle:self.__last_needle]

    def select_needles(self, color, row_index, blank_line):
        bits = bitarray([False] * Machine.WIDTH, endian="little")
        first_needle = max(0, self.pattern.pat_start_needle)
        last_needle = min(
            self.pattern.pat_width + self.pattern.pat_start_needle,
            Machine.WIDTH)

        # select needles flanking the pattern
        # if necessary to knit the background color
        if self.knit_mode.flanking_needles(color, self.num_colors):
            bits[0:first_needle] = True
            bits[last_needle:Machine.WIDTH] = True

        if not blank_line:
            first_pixel = first_needle - self.pattern.pat_start_needle
            last_pixel = last_needle - self.pattern.pat_start_needle
            bits[first_needle:last_needle] = (
                self.pattern.pattern_expanded
            )[row_index][first_pixel:last_pixel]

        self.__first_needle = first_needle
        self.__last_needle = last_needle
        return bits

    def knit(self, pattern, options):
        '''Finite State Machine governing serial communication'''
        method = "_knit_" + self.state.name.lower()
        if not hasattr(KnitStateMachine, method):
            # NONE, FINISHED
            return KnitOutput.NONE
        dispatch = getattr(KnitStateMachine, method)
        result = dispatch(self, pattern, options)
        return result
