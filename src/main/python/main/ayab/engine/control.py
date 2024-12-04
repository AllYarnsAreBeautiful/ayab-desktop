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
import logging
from bitarray import bitarray

from ..signal_sender import SignalSender
from .communication import Communication, Token
from .communication_mock import CommunicationMock
from .options import OptionsTab
from .mode import Mode, ModeFunc
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .mode import ModeFuncType
    from .engine import Engine
    from ..ayab import GuiMain
from .engine_fsm import State, Operation, StateMachine
from .output import Output
from .status import Carriage, Direction, StatusTab
from .pattern import Pattern
from ..preferences import Preferences


class Control(SignalSender):
    """
    Class governing information flow with the shield.
    """

    BLOCK_LENGTH = 256
    COLOR_SYMBOLS = "A", "B", "C", "D", "E", "F"
    FIRST_SUPPORTED_API_VERSION = 6  # currently this is the only supported version
    FLANKING_NEEDLES = True

    com: Communication | CommunicationMock
    continuous_reporting: bool
    end_needle: int
    end_pixel: int
    former_request: int
    inf_repeat: bool
    initial_carriage: Carriage
    initial_direction: Direction
    initial_position: int
    len_pat_expanded: int
    line_block: int
    mode: Mode
    mode_func: ModeFuncType
    num_colors: int
    passes_per_row: int
    pat_height: int
    pat_row: int
    pattern: Pattern
    pattern_repeats: int
    portname: str
    prefs: Preferences
    start_needle: int
    start_pixel: int
    start_row: int
    state: State
    logger: logging.Logger

    def __init__(self, parent: GuiMain, engine: Engine):
        super().__init__(parent.signal_receiver)
        self.logger = logging.getLogger(type(self).__name__)
        self.status: StatusTab = engine.status
        self.notification = Output.NONE
        self.api_version: int = self.FIRST_SUPPORTED_API_VERSION

    def start(
        self, pattern: Pattern, options: OptionsTab, operation: Operation
    ) -> None:
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
            self.prefs = options.prefs
            self.len_pat_expanded = self.pat_height * self.num_colors
            self.passes_per_row = self.mode.row_multiplier(self.num_colors)
            self.start_needle = max(0, self.pattern.pat_start_needle)
            self.end_needle = min(
                self.pattern.pat_width + self.pattern.pat_start_needle,
                self.machine.width,
            )
            self.start_pixel = self.start_needle - self.pattern.pat_start_needle
            self.end_pixel = self.end_needle - self.pattern.pat_start_needle
            self.initial_carriage = Carriage.Unknown
            self.initial_position = -1
            self.initial_direction = Direction.Unknown
            self.reset_status()
        self.portname = options.portname
        self.state = State.CONNECT

    def stop(self) -> None:
        try:
            self.com.close_serial()
        except Exception:
            pass

    def func_selector(self) -> bool:
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
            self.logger.error("Unrecognized value returned from Mode.knit_func()")
            return False
        # else
        self.mode_func: ModeFuncType = getattr(ModeFunc, func_name)
        return True

    def reset_status(self) -> None:
        self.status.reset()
        if self.mode == Mode.SINGLEBED:
            self.status.alt_color = self.pattern.palette[1]
            self.status.color_symbol = ""  # "A/B"
        else:
            self.status.alt_color = None

        self.status.machine_width = self.machine.width

        if self.FLANKING_NEEDLES and self.mode != Mode.SINGLEBED:
            self.status.knit_start_needle = self.pattern.knit_start_needle
        else:
            # in single-bed mode, only the pattern bits are emitted, no extra needles
            self.status.knit_start_needle = self.start_needle

        self.status.passes_per_row = self.passes_per_row

    def check_serial_API6(self) -> tuple[Token, int]:
        msg, token, param = self.com.update_API6()
        if msg is None:
            return Token.none, param  # TODO: Do We Throw Here?
        if token == Token.cnfInfo:
            self.__log_cnfInfo(msg)
        elif token == Token.indState:
            self.status.parse_device_state_API6(param, msg)
        elif token == Token.testRes:
            if len(msg) > 0:
                self.emit_hw_test_writer(msg[1:].decode())
        return token, param

    def __log_cnfInfo(self, msg: bytes) -> None:
        api = msg[1]
        log = "API v" + str(api)
        if api >= 5:
            log += ", FW v" + str(msg[2]) + "." + str(msg[3]) + "." + str(msg[4])
            suffix = msg[5:21]
            suffix_null_index = suffix.find(0)
            suffix_str = suffix[: suffix_null_index + 1].decode()
            if len(suffix_str) > 1:
                log += "-" + suffix_str
        self.logger.info(log)

    def cnf_line_API6(self, line_number: int) -> bool:
        if not (line_number < self.BLOCK_LENGTH):
            self.logger.error("Requested line number out of range")
            return True  # stop knitting
        # else
        # TODO: some better algorithm for block wrapping
        if self.former_request == self.BLOCK_LENGTH - 1 and line_number == 0:
            # wrap to next block of lines
            self.line_block += 1
        # requested line number should either be
        # the same as the previous request, or the next line
        elif (
            self.former_request != line_number
            and self.former_request + 1 != line_number
        ):
            self.logger.error("Requested line number out of sequence")
            return True  # stop knitting

        # store requested line number for next request
        self.former_request = line_number
        requested_line = line_number

        # adjust line_number with current block
        line_number += self.BLOCK_LENGTH * self.line_block

        # get data for next line of knitting
        color, row_index, blank_line, last_line = self.mode_func(self, line_number)
        bits = self.select_needles_API6(color, row_index, blank_line)

        # Send line to machine
        # Note that we never set the "final line" flag here, because
        # we will send an extra blank line afterwards to make sure we
        # can track the final line being knitted.
        flags = 0
        self.com.cnf_line_API6(requested_line, color, flags, bits.tobytes())

        # screen output
        # TODO: tidy up this code
        msg = (
            str(self.line_block)
            + " "
            + str(line_number)
            + " reqLine: "
            + str(requested_line)
            + " pat_row: "
            + str(self.pat_row)
        )
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

    def cnf_final_line_API6(self, requested_line: int) -> None:
        self.logger.debug("sending blank line as final line=%d", requested_line)

        # prepare a blank line as the final line
        bits = bitarray(self.machine.width, endian="little")

        # send line to machine
        color = 0  # doesn't matter
        flags = 1  # this is the last line
        self.com.cnf_line_API6(requested_line, color, flags, bits.tobytes())

    def __update_status(self, line_number: int, color: int, bits: bitarray) -> None:
        self.status.total_rows = self.pat_height
        self.status.current_row = self.pat_row + 1
        self.status.line_number = line_number
        if self.inf_repeat:
            self.status.repeats = self.pattern_repeats
        if self.mode != Mode.SINGLEBED:
            self.status.color_symbol = self.COLOR_SYMBOLS[color]  # type: ignore
        self.status.color = self.pattern.palette[color]
        if self.FLANKING_NEEDLES and self.mode != Mode.SINGLEBED:
            self.status.bits = bits[
                self.pattern.knit_start_needle : self.pattern.knit_end_needle
            ]
        else:
            self.status.bits = bits[self.start_needle : self.end_needle]
        self.status.carriage_type = self.initial_carriage
        if line_number % 2 == 0:
            self.status.carriage_direction = self.initial_direction
        else:
            self.status.carriage_direction = self.initial_direction.reverse()

    def select_needles_API6(
        self, color: int, row_index: int, blank_line: bool
    ) -> bitarray:
        bits = bitarray(self.machine.width, endian="little")

        # select needles flanking the pattern
        # if necessary to knit the background color
        if (
            self.mode.flanking_needles(color, self.num_colors)
            and self.mode != Mode.SINGLEBED
        ):
            bits[0 : self.start_needle] = True
            bits[self.end_needle : self.machine.width] = True

        if not blank_line:
            bits[self.start_needle : self.end_needle] = (self.pattern.pattern_expanded)[
                row_index
            ][self.start_pixel : self.end_pixel]

        return bits

    def operate(self, operation: Operation) -> Output:
        """Finite State Machine governing serial communication"""
        method = "_API" + str(self.api_version) + "_" + self.state.name.lower()
        if not hasattr(StateMachine, method):
            # TODO: yell about this maybe?
            return Output.NONE
        dispatch: Callable[[Control, Operation], Output] = getattr(StateMachine, method)
        result = dispatch(self, operation)
        return result
