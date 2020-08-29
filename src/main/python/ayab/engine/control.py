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
from bitarray import bitarray

from PyQt5.QtCore import QCoreApplication

from ..observable import Observable
from .communication import Communication, Token
from .communication_mock import CommunicationMock
from .options import Alignment
from .mode import Mode, ModeFunc
from .state import State, StateMachine, Operation
from .output import Output
#from ..machine import Machine


class Control(Observable):
    """
    Class governing information flow with the shield.
    """
    BLOCK_LENGTH = 256
    COLOR_SYMBOLS = "A", "B", "C", "D", "E", "F"
    FIRST_SUPPORTED_API_VERSION = 0x06  # currently this is the only supported version
    FLANKING_NEEDLES = True

    def __init__(self, parent, engine):
        super().__init__(parent.seer)
        self.logger = logging.getLogger(type(self).__name__)
        self.status = engine.status

    def start(self, pattern, options, operation):
        self.machine = options.machine
        if operation == Operation.KNIT:
            self.former_request = 0
            self.line_block = 0
            self.pattern_repeats = 0
            self.pattern = pattern
            self.pat_height = pattern.pat_height
            self.num_colors = options.num_colors
            self.start_row = options.start_row
            self.mode = options.mode
            self.inf_repeat = options.inf_repeat
            self.continuous_reporting = options.continuous_reporting
            self.len_pat_expanded = self.pat_height * self.num_colors
            self.passes_per_row = self.mode.row_multiplier(self.num_colors)
            self.start_needle = max(0, self.pattern.pat_start_needle)
            self.end_needle = min(
                self.pattern.pat_width + self.pattern.pat_start_needle,
                self.machine.width)
            self.start_pixel = self.start_needle - self.pattern.pat_start_needle
            self.end_pixel = self.end_needle - self.pattern.pat_start_needle
            if self.FLANKING_NEEDLES:
                self.midline = self.pattern.knit_end_needle - self.machine.width // 2
            else:
                self.midline = self.end_needle - self.machine.width // 2
            self.reset_status()
        self.portname = options.portname
        self.state = State.SETUP

    def stop(self):
        try:
            self.com.close_serial()
        except Exception:
            pass

    def func_selector(self):
        """
        Method selecting the function that decides which line of data to send
        according to the knitting mode and number of colors.

        @author Tom Price
        @date   June 2020
        """
        if not self.mode.good_ncolors(self.num_colors):
            self.logger.error("Wrong number of colours for the knitting mode")
            return False
        # else
        func_name = self.mode.knit_func(self.num_colors)
        if not hasattr(ModeFunc, func_name):
            self.logger.error(
                "Unrecognized value returned from Mode.knit_func()")
            return False
        # else
        self.mode_func = getattr(ModeFunc, func_name)
        return True

    def reset_status(self):
        self.status.reset()
        if self.mode == Mode.SINGLEBED:
            self.status.alt_color = self.pattern.palette[1]
            self.status.color_symbol = ""  # "A/B"
        else:
            self.status.alt_color = None

    def check_serial_API6(self):
        msg, token, param = self.com.update_API6()
        if token == Token.cnfInfo:
            self.__log_cnfInfo(msg)
        elif token == Token.indState:
            self.status.parse_device_state_API6(param, msg)
        elif token == Token.testRes:
            if len(msg) > 0:
                self.emit_hw_test_writer(msg[1:].decode())
        return token, param

    def __log_cnfInfo(self, msg):
        api = msg[1]
        log = "API v" + str(api)
        if api >= 5:
            log += ", FW v" + str(msg[2]) + "." + str(msg[3])
        self.logger.info(log)

    def cnf_line_API6(self, line_number):
        if not (line_number < self.BLOCK_LENGTH):
            self.logger.error("Requested line number out of range")
            return True  # stop knitting
        # else
        # TODO: some better algorithm for block wrapping
        if self.former_request == self.BLOCK_LENGTH - 1 and line_number == 0:
            # wrap to next block of lines
            self.line_block += 1

        # store requested line number for next request
        self.former_request = line_number
        requested_line = line_number

        # adjust line_number with current block
        line_number += self.BLOCK_LENGTH * self.line_block

        # get data for next line of knitting
        color, row_index, blank_line, last_line = self.mode_func(
            self, line_number)
        bits = self.select_needles_API6(color, row_index, blank_line)

        # send line to machine
        flag = last_line and not self.inf_repeat
        self.com.cnf_line_API6(requested_line, color, flag, bits.tobytes())

        # screen output
        # TODO: tidy up this code
        msg = str(self.line_block) + " " + str(line_number) + " reqLine: " + \
            str(requested_line) + " pat_row: " + str(self.pat_row)
        if blank_line:
            msg += " BLANK LINE"
        else:
            msg += " row_index: " + str(row_index)
            msg += " color: " + str(self.COLOR_SYMBOLS[color])
        self.logger.debug(msg)

        # get status to send to GUI
        self.__update_status(line_number, color, bits)

        if not last_line:
            return False  # keep knitting
        elif self.inf_repeat:
            self.pattern_repeats += 1
            return False  # keep knitting
        else:
            return True  # pattern finished

    def __update_status(self, line_number, color, bits):
        self.status.current_row = self.pat_row + 1
        self.status.line_number = line_number
        if self.inf_repeat:
            self.status.repeats = self.pattern_repeats
        if self.mode != Mode.SINGLEBED:
            self.status.color_symbol = self.COLOR_SYMBOLS[color]
        self.status.color = self.pattern.palette[color]
        if self.FLANKING_NEEDLES:
            self.status.bits = bits[self.pattern.knit_start_needle:self.pattern.knit_end_needle]
        else:
            self.status.bits = bits[self.start_needle:self.end_needle]

    def select_needles_API6(self, color, row_index, blank_line):
        bits = bitarray([False] * self.machine.width, endian="little")

        # select needles flanking the pattern
        # if necessary to knit the background color
        if self.mode.flanking_needles(color, self.num_colors):
            bits[0:self.start_needle] = True
            bits[self.end_needle:self.machine.width] = True

        if not blank_line:
            bits[self.start_needle:self.end_needle] = (
                self.pattern.pattern_expanded
            )[row_index][self.start_pixel:self.end_pixel]

        return bits

    def operate(self, operation, API_version=6):
        """Finite State Machine governing serial communication"""
        method = "_API" + str(API_version) + "_" + self.state.name.lower()
        if not hasattr(StateMachine, method):
            return Output.NONE
        dispatch = getattr(StateMachine, method)
        result = dispatch(self, operation)
        return result
