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

from enum import Enum, auto

from PyQt5.QtCore import QCoreApplication

from .communication import AyabCommunication, MessageToken
from .communication_mockup import AyabCommunicationMockup
from .output import KnitOutput


class KnitState(Enum):
    # NONE = auto()
    SETUP = auto()
    INIT = auto()
    WAIT_FOR_INIT = auto()
    START = auto()
    OPERATE = auto()
    # FINISHED = auto()


class KnitStateMachine(object):
    """
    Each method is a step in the finite state machine that governs
    communication with the shield and is called only by `AyabControl.knit()`

    @author Tom Price
    @date   June 2020
    """
    def _knit_setup(control, pattern, options):
        control.logger.debug("KnitState SETUP")
        control.former_request = 0
        control.line_block = 0
        control.pattern_repeats = 0
        control.pattern = pattern
        control.pat_height = pattern.pat_height
        control.num_colors = options.num_colors
        control.start_row = options.start_row
        control.mode = options.mode
        control.inf_repeat = options.inf_repeat
        control.len_pat_expanded = control.pat_height * control.num_colors
        control.passes_per_row = control.mode.row_multiplier(control.num_colors)
        control.reset_status()
        if not control.func_selector():
            return KnitOutput.ERROR_INVALID_SETTINGS
        # else
        control.logger.debug(options.portname)
        if options.portname == QCoreApplication.translate(
                "KnitEngine", "Simulation"):
            control.com = AyabCommunicationMockup()
        else:
            control.com = AyabCommunication()
        if not control.com.open_serial(options.portname):
            control.logger.error("Could not open serial port")
            return KnitOutput.ERROR_SERIAL_PORT
        # else
        # setup complete
        control.state = KnitState.INIT
        return KnitOutput.NONE

    def _knit_init(control, pattern, options):
        control.logger.debug("KnitState INIT")
        rcvMsg, rcvParam = control.check_serial()
        if rcvMsg == MessageToken.cnfInfo:
            if rcvParam == control.API_VERSION:
                control.state = KnitState.WAIT_FOR_INIT
                return KnitOutput.WAIT_FOR_INIT
            else:
                control.logger.error("Wrong API version: " + str(rcvParam) +
                                     ", expected: " + str(control.API_VERSION))
                return KnitOutput.ERROR_WRONG_API
        # else
        control.com.req_info()
        return KnitOutput.CONNECTING_TO_MACHINE

    def _knit_wait_for_init(control, pattern, options):
        control.logger.debug("KnitState WAIT_FOR_INIT")
        rcvMsg, rcvParam = control.check_serial()
        if rcvMsg == MessageToken.indState:
            if rcvParam == 1:
                control.com.req_start(control.pattern.knit_start_needle,
                                      control.pattern.knit_stop_needle,
                                      options.continuous_reporting)
                control.state = KnitState.START
            else:
                control.logger.debug("Init failed")
        # fallthrough
        return KnitOutput.NONE

    def _knit_start(control, pattern, options):
        control.logger.debug("KnitState START")
        rcvMsg, rcvParam = control.check_serial()
        if rcvMsg == MessageToken.cnfStart:
            if rcvParam == 1:
                control.state = KnitState.OPERATE
                return KnitOutput.PLEASE_KNIT
            else:
                control.logger.error("Device not ready")
                return KnitOutput.DEVICE_NOT_READY
        # fallthrough
        return KnitOutput.NONE

    def _knit_operate(control, pattern, options):
        control.logger.debug("KnitState OPERATE")
        rcvMsg, rcvParam = control.check_serial()
        if rcvMsg == MessageToken.reqLine:
            pattern_finished = control.cnf_line(rcvParam)
            if pattern_finished:
                control.state = KnitState.SETUP
                return KnitOutput.FINISHED
            # else
            return KnitOutput.NEXT_LINE
        # fallthrough
        return KnitOutput.NONE
