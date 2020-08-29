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

# from PyQt5.QtCore import QStateMachine, QState
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication

from .communication import Communication, Token
from .communication_mock import CommunicationMock
from .hw_test_communication_mock import HardwareTestCommunicationMock
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
    FINISHED = auto()


class StateMachine(object):
    """
    Each method is a step in the finite state machine that governs serial
M
    communication with the device and is called only by `Control.operate()`

    @author Tom Price
    @date   June 2020
    """

    #     def __init__():
    #         """Define Finite State Machine"""
    #
    #         # Finite State Machine
    #         self.machine = QStateMachine()
    #
    #         # Machine states
    #         self.SETUP = QState(self.machine)
    #         self.INIT = QState(self.machine)
    #         self.REQUEST_START = QState(self.machine)
    #         self.CONFIRM_START = QState(self.machine)
    #         self.RUN_KNIT = QState(self.machine)
    #         self.REQUEST_TEST = QState(self.machine)
    #         self.CONFIRM_TEST = QState(self.machine)
    #         self.RUN_TEST = QState(self.machine)
    #         self.FINISHED = QState(self.machine)
    #
    #         # Set machine state
    #         self.machine.setInitialState(self.SETUP)

    def set_transitions(self, parent):
        """Define transitions between states for Finite State Machine"""

        # Events that trigger state changes
        self.SETUP.addTransition(parent.port_opener, self.INIT)

    def _API6_setup(control, operation):
        control.logger.debug("State SETUP")
        if operation == Operation.KNIT:
            if not control.func_selector():
                return Output.ERROR_INVALID_SETTINGS
        # else
        control.logger.debug("Port name: " + control.portname)
        if control.portname == QCoreApplication.translate(
                "KnitEngine", "Simulation"):
            if operation == Operation.KNIT:
                control.com = CommunicationMock()
            else:
                control.com = HardwareTestCommunicationMock()
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
        token, param = control.check_serial_API6()
        if token == Token.cnfInfo:
            if param >= control.FIRST_SUPPORTED_API_VERSION:
                control.api_version = param
                if operation == Operation.TEST:
                    control.state = State.REQUEST_TEST
                    # TODO: need more informative messages for HW test
                    return Output.NONE
                else:
                    control.state = State.REQUEST_START
                    return Output.WAIT_FOR_INIT
            else:
                control.logger.error("Wrong API version: " + str(param) +
                                     ", expected >= " +
                                     str(control.FIRST_SUPPORTED_API_VERSION))
                return Output.ERROR_WRONG_API
        # else
        control.com.req_info()
        return Output.CONNECTING_TO_MACHINE

    def _API6_request_start(control, operation):
        control.logger.debug("State REQUEST_START")
        token, param = control.check_serial_API6()
        if token == Token.indState:
            if param == 0:
                control.com.req_start_API6(control.machine.value,
                                           control.pattern.knit_start_needle,
                                           control.pattern.knit_end_needle - 1,
                                           control.continuous_reporting)
                control.state = State.CONFIRM_START
            else:
                # any value of param other than 1 is some kind of error code
                control.logger.debug("Knit init failed")
                # TODO: more output to describe error
        # fallthrough
        return Output.NONE

    def _API6_confirm_start(control, operation):
        control.logger.debug("State CONFIRM_START")
        token, param = control.check_serial_API6()
        if token == Token.cnfStart:
            if param == 0:
                control.state = State.RUN_KNIT
                return Output.PLEASE_KNIT
            else:
                # any value of param other than 1 is some kind of error code
                control.logger.error("Device not ready")
                # TODO: more output to describe error
                return Output.DEVICE_NOT_READY
        # fallthrough
        return Output.NONE

    def _API6_run_knit(control, operation):
        control.logger.debug("State RUN_KNIT")
        token, param = control.check_serial_API6()
        if token == Token.reqLine:
            pattern_finished = control.cnf_line_API6(param)
            if pattern_finished:
                control.state = State.FINISHED
                return Output.KNITTING_FINISHED
            # else
            return Output.NEXT_LINE
        # fallthrough
        return Output.NONE

    def _API6_request_test(control, operation):
        control.logger.debug("State REQUEST_TEST")
        token, param = control.check_serial_API6()
        if token == Token.indState:
            if param == 0:
                control.com.req_test_API6(control.machine.value)
                control.state = State.CONFIRM_TEST
            else:
                # any value of param other than 1 is some kind of error code
                control.logger.debug("Test init failed")
                # TODO: more output to describe error
        # fallthrough
        return Output.NONE

    def _API6_confirm_test(control, operation):
        control.logger.debug("State CONFIRM_TEST")
        token, param = control.check_serial_API6()
        if token == Token.cnfTest:
            if param == 0:
                control.emit_hw_test_starter(control)
                control.state = State.RUN_TEST
                # TODO: need more informative messages for HW test
                return Output.NONE
            else:
                # any value of param other than 1 is some kind of error code
                control.logger.error("Device not ready")
                # TODO: more output to describe error
                return Output.DEVICE_NOT_READY
        # fallthrough
        return Output.NONE

    def _API6_run_test(control, operation):
        # control.logger.debug("State RUN_TEST")
        token, param = control.check_serial_API6()
        return Output.NONE

    def _API6_finished(control, operation):
        control.logger.debug("State FINISHED")
        try:
            control.timer.stop()
        except Exception:
            pass
        control.state = State.SETUP
        return Output.NONE
