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

from enum import Enum
from PyQt5.QtCore import QCoreApplication
from .ayab_communication import AyabCommunication, MessageToken
from .ayab_communication_mockup import AyabCommunicationMockup
from .ayab_knit_output import KnitOutput


class KnitState(Enum):
    # NONE = 0
    SETUP = 1
    INIT = 2
    WAIT_FOR_INIT = 3
    START = 4
    OPERATE = 5
    # FINISHED = 6


class KnitStateMachine(object):
    def _knit_setup(ayab_control, pattern, options):
        ayab_control.logger.debug("KnitState SETUP")
        ayab_control.status.reset()
        ayab_control.former_request = 0
        ayab_control.line_block = 0
        ayab_control.pattern_repeats = 0
        ayab_control.pattern = pattern
        ayab_control.pat_height = pattern.pat_height
        ayab_control.num_colors = options.num_colors
        ayab_control.start_row = options.start_row
        ayab_control.knit_mode = options.knit_mode
        ayab_control.inf_repeat = options.inf_repeat
        ayab_control.len_pat_expanded = ayab_control.pat_height * ayab_control.num_colors
        ayab_control.passes_per_row = ayab_control.knit_mode.row_multiplier(
            ayab_control.num_colors)
        if not ayab_control.func_selector():
            return KnitOutput.ERROR_INVALID_SETTINGS
        # else
        ayab_control.logger.debug(options.portname)
        if options.portname == QCoreApplication.translate(
                "AyabPlugin", "Simulation"):
            ayab_control.com = AyabCommunicationMockup()
        else:
            ayab_control.com = AyabCommunication()
        if not ayab_control.com.open_serial(options.portname):
            ayab_control.logger.error("Could not open serial port")
            return KnitOutput.ERROR_SERIAL_PORT
        # else
        # setup complete
        ayab_control.state = KnitState.INIT
        return KnitOutput.NONE

    def _knit_init(ayab_control, pattern, options):
        ayab_control.logger.debug("KnitState INIT")
        rcvMsg, rcvParam = ayab_control.check_serial()
        if rcvMsg == MessageToken.cnfInfo:
            if rcvParam == ayab_control.API_VERSION:
                ayab_control.state = KnitState.WAIT_FOR_INIT
                return KnitOutput.WAIT_FOR_INIT
            else:
                ayab_control.logger.error("Wrong API version: " +
                                          str(rcvParam) + ", expected: " +
                                          str(ayab_control.API_VERSION))
                return KnitOutput.ERROR_WRONG_API
        # else
        ayab_control.com.req_info()
        return KnitOutput.CONNECTING_TO_MACHINE

    def _knit_wait_for_init(ayab_control, pattern, options):
        ayab_control.logger.debug("KnitState WAIT_FOR_INIT")
        rcvMsg, rcvParam = ayab_control.check_serial()
        if rcvMsg == MessageToken.indState:
            if rcvParam == 1:
                ayab_control.com.req_start(
                    ayab_control.pattern.knit_start_needle,
                    ayab_control.pattern.knit_stop_needle,
                    options.continuous_reporting)
                ayab_control.state = KnitState.START
            else:
                ayab_control.logger.debug("Init failed")
        # fallthrough
        return KnitOutput.NONE

    def _knit_start(ayab_control, pattern, options):
        ayab_control.logger.debug("KnitState START")
        rcvMsg, rcvParam = ayab_control.check_serial()
        if rcvMsg == MessageToken.cnfStart:
            if rcvParam == 1:
                ayab_control.state = KnitState.OPERATE
                return KnitOutput.PLEASE_KNIT
            else:
                ayab_control.logger.error("Device not ready")
                return KnitOutput.DEVICE_NOT_READY
        # fallthrough
        return KnitOutput.NONE

    def _knit_operate(ayab_control, pattern, options):
        ayab_control.logger.debug("KnitState OPERATE")
        rcvMsg, rcvParam = ayab_control.check_serial()
        if rcvMsg == MessageToken.reqLine:
            pattern_finished = ayab_control.cnf_line(rcvParam)
            if pattern_finished:
                ayab_control.state = KnitState.SETUP
                return KnitOutput.FINISHED
        # fallthrough
        return KnitOutput.NONE
