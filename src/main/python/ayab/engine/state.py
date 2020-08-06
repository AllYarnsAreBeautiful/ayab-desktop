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

from .communication import Communication, Token
from .communication_mockup import CommunicationMockup
from .output import Output


class Operation(Enum):
    KNIT = auto()
    TEST = auto()


class State(Enum):
    SETUP = auto()
    INIT = auto()
    REQUEST_START = auto()
    CONFIRM_START = auto()
    RUN_KNIT = auto()
    REQUEST_TEST = auto()
    CONFIRM_TEST = auto()
    RUN_TEST = auto()


class StateMachine(object):
    """
    Each method is a step in the finite state machine that governs
    communication with the shield and is called only by `AyabControl.knit()`

    @author Tom Price
    @date   June 2020
    """
    def _API6_setup(control, operation):
        control.logger.debug("State SETUP")
        if operation == Operation.KNIT:
            if not control.func_selector():
                return Output.ERROR_INVALID_SETTINGS
        # else
        control.logger.debug(control.portname)
        if control.portname == QCoreApplication.translate(
                "KnitEngine", "Simulation"):
            control.com = CommunicationMockup()
        else:
            control.com = Communication()
        if not control.com.open_serial(control.portname):
            control.logger.error("Could not open serial port")
            return Output.ERROR_SERIAL_PORT
        # else
        # setup complete
        control.state = State.INIT
        return Output.NONE

    def _API6_init(control, operation):
        control.logger.debug("State INIT")
        rcvMsg, rcvParam = control.check_serial()
        if rcvMsg == Token.cnfInfo:
            if rcvParam >= control.FIRST_SUPPORTED_API_VERSION:
                control.api_version = rcvParam
                if operation == Operation.TEST:
                    control.state = State.REQUEST_TEST
                else:
                    control.state = State.REQUEST_START
                return Output.WAIT_FOR_INIT
            else:
                control.logger.error("Wrong API version: " + str(rcvParam) +
                                     ", expected >= " +
                                     str(control.FIRST_SUPPORTED_API_VERSION))
                return Output.ERROR_WRONG_API
        # else
        control.com.req_info()
        return Output.CONNECTING_TO_MACHINE

    def _API6_request_start(control, operation):
        control.logger.debug("State REQUEST_START")
        rcvMsg, rcvParam = control.check_serial()
        if rcvMsg == Token.indState:
            if rcvParam == 1:
                control.com.req_start_API6(control.machine.value,
                                           control.pattern.knit_start_needle,
                                           control.pattern.knit_stop_needle,
                                           control.continuous_reporting)
                control.state = State.CONFIRM_START
            else:
                # any value of rcvParam other than 1 is some kind of error code
                control.logger.debug("Knit init failed")
                # TODO: more output to describe error
        # fallthrough
        return Output.NONE

    def _API6_confirm_start(control, operation):
        control.logger.debug("State CONFIRM_START")
        rcvMsg, rcvParam = control.check_serial()
        if rcvMsg == Token.cnfStart:
            if rcvParam == 1:
                control.state = State.RUN_KNIT
                return Output.PLEASE_KNIT
            else:
                # any value of rcvParam other than 1 is some kind of error code
                control.logger.error("Device not ready")
                # TODO: more output to describe error
                return Output.DEVICE_NOT_READY
        # fallthrough
        return Output.NONE

    def _API6_run_knit(control, operation):
        control.logger.debug("State RUN_KNIT")
        rcvMsg, rcvParam = control.check_serial()
        if rcvMsg == Token.reqLine:
            pattern_finished = control.cnf_line_API6(rcvParam)
            if pattern_finished:
                control.state = State.SETUP
                return Output.FINISHED
            # else
            return Output.NEXT_LINE
        # fallthrough
        return Output.NONE

    def _API6_request_test(control, operation):
        control.logger.debug("State REQUEST_TEST")
        rcvMsg, rcvParam = control.check_serial()
        if rcvMsg == Token.indState:
            if rcvParam == 1:
                control.com.req_test_API6(control.machine.value)
                control.state = State.CONFIRM_TEST
            else:
                # any value of rcvParam other than 1 is some kind of error code
                control.logger.debug("Test init failed")
                # TODO: more output to describe error
        # fallthrough
        return Output.NONE

    def _API6_confirm_test(control, operation):
        control.logger.debug("State CONFIRM_TEST")
        rcvMsg, rcvParam = control.check_serial()
        if rcvMsg == Token.cnfTest:
            if rcvParam == 1:
                control.state = State.RUN_TEST
                return Output.NONE
            else:
                # any value of rcvParam other than 1 is some kind of error code
                control.logger.error("Device not ready")
                # TODO: more output to describe error
                return Output.DEVICE_NOT_READY
        # fallthrough
        return Output.NONE

    def _API6_run_test(control, operation):
        control.logger.debug("State RUN_TEST")
        # TODO: open serial monitor
        return Output.NONE
