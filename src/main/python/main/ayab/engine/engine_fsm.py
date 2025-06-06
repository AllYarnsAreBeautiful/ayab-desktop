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

from enum import Enum, auto

from PySide6.QtCore import QCoreApplication
from PySide6.QtStateMachine import QStateMachine, QState

from .communication import Communication, Token
from .communication_mock import CommunicationMock
from .hw_test_communication_mock import HardwareTestCommunicationMock
from .output import Output
from typing import TYPE_CHECKING, Callable, Any

import time

if TYPE_CHECKING:
    from .control import Control
    from .engine import Engine


class Operation(Enum):
    KNIT = auto()
    TEST = auto()


class State(Enum):
    CONNECT = auto()
    VERSION_CHECK = auto()
    INIT = auto()
    REQUEST_START = auto()
    CONFIRM_START = auto()
    RUN_KNIT = auto()
    REQUEST_TEST = auto()
    CONFIRM_TEST = auto()
    RUN_TEST = auto()
    DISCONNECT = auto()
    FINISHING = auto()
    FINISHED = auto()


class StateMachine(QStateMachine):
    """
        Each method is a step in the finite state machine that governs serial
    M
        communication with the device and is called only by `Control.operate()`

        @author Tom Price
        @date   June 2020
    """

    CONNECT: QState
    VERSION_CHECK: QState

    lastRetry : float = 0.0

    @staticmethod
    def retry(method: Callable[..., None], args: Any=(), timeout: float=0.1) -> None:
        current_time = time.time()
        if (current_time - StateMachine.lastRetry) > timeout:
            StateMachine.lastRetry = current_time
            method(*args)

    def set_transitions(self, parent: Engine) -> None:
        """Define transitions between states for Finite State Machine"""

        # Events that trigger state changes
        self.CONNECT.addTransition(parent.port_opener, self.VERSION_CHECK)

    @staticmethod
    def _API6_connect(control: Control, operation: Operation) -> Output:
        control.logger.debug("State CONNECT")
        if operation == Operation.KNIT:
            if not control.func_selector():
                return Output.ERROR_INVALID_SETTINGS
        # else
        control.logger.debug("Port name: " + control.portname)
        if control.portname == QCoreApplication.translate("KnitEngine", "Simulation"):
            if operation == Operation.KNIT:
                control.com = CommunicationMock()
            else:
                control.com = HardwareTestCommunicationMock()  # type: ignore
        else:
            control.com = Communication()
        if not control.com.open_serial(control.portname):
            control.logger.error("Could not open serial port")
            control.state = State.FINISHED
            return Output.ERROR_SERIAL_PORT
        # else
        # setup complete
        control.state = State.VERSION_CHECK
        control.logger.debug("State VERSION_CHECK")
        return Output.NONE

    @staticmethod
    def _API6_version_check(control: Control, operation: Operation) -> Output:
        token, param = control.check_serial_API6()
        if token == Token.cnfInfo:
            if param >= control.FIRST_SUPPORTED_API_VERSION:
                control.api_version = param
                control.state = State.INIT
                control.logger.debug("State INIT")
                return Output.NONE
            else:
                control.logger.error(
                    "Wrong API version: "
                    + str(param)
                    + ", expected >= "
                    + str(control.FIRST_SUPPORTED_API_VERSION)
                )
                return Output.ERROR_WRONG_API
        # else
        StateMachine.retry(control.com.req_info)
        return Output.CONNECTING_TO_MACHINE

    @staticmethod
    def _API6_init(control: Control, operation: Operation) -> Output:
        token, param = control.check_serial_API6()
        if token == Token.cnfInit:
            # no errors? Move on
            if param == 0:
                if operation == Operation.TEST:
                    control.state = State.REQUEST_TEST
                    control.logger.debug("State REQUEST_TEST")
                    return Output.NONE
                else:
                    # operation = Operation.KNIT:
                    control.state = State.REQUEST_START
                    control.logger.debug("State REQUEST_START")
                    return Output.NONE
            else:
                control.logger.error("Error initializing firmware: " + str(param))
                return Output.ERROR_INITIALIZING_FIRMWARE
        # else
        StateMachine.retry(control.com.req_init_API6, (control.machine,))
        return Output.INITIALIZING_FIRMWARE

    @staticmethod
    def _API6_request_start(control: Control, operation: Operation) -> Output:
        token, param = control.check_serial_API6()
        if token == Token.indState:
            if param == 0:
                # record initial position, direction, carriage
                control.initial_carriage = control.status.carriage_type
                control.initial_position = control.status.carriage_position
                control.initial_direction = control.status.carriage_direction
                # set status.active
                control.status.active = control.continuous_reporting
                # request start
                control.com.req_start_API6(
                    control.pattern.knit_start_needle,
                    control.pattern.knit_end_needle - 1,
                    control.continuous_reporting,
                    control.prefs.value("disable_hardware_beep"),
                )
                control.state = State.CONFIRM_START
                control.logger.debug("State CONFIRM_START")
            else:
                # any value of param other than 0 is some kind of error code
                control.logger.debug(
                    "Knit init failed with error code "
                    + str(param)
                    + " in state "
                    + str(control.status.firmware_state)
                )
                # TODO: more output to describe error
        return Output.WAIT_FOR_INIT

    @staticmethod
    def _API6_confirm_start(control: Control, operation: Operation) -> Output:
        token, param = control.check_serial_API6()
        if token == Token.cnfStart:
            if param == 0:
                control.state = State.RUN_KNIT
                control.logger.debug("State RUN_KNIT")
                return Output.PLEASE_KNIT
            else:
                # any value of param other than 0 is some kind of error code
                control.logger.error(
                    "Device not ready, returned `cnfStart` with error code "
                    + str(param)
                )
                # TODO: more output to describe error
                return Output.DEVICE_NOT_READY
        # else
        return Output.NONE

    @staticmethod
    def _API6_run_knit(control: Control, operation: Operation) -> Output:
        token, param = control.check_serial_API6()
        if token == Token.reqLine:
            pattern_finished = control.cnf_line_API6(param)
            if pattern_finished:
                control.state = State.FINISHING
                return Output.NEXT_LINE
            else:
                return Output.NEXT_LINE
        # else
        return Output.NONE

    @staticmethod
    def _API6_request_test(control: Control, operation: Operation) -> Output:
        control.com.req_test_API6()
        control.state = State.CONFIRM_TEST
        control.logger.debug("State CONFIRM_TEST")
        return Output.NONE

    @staticmethod
    def _API6_confirm_test(control: Control, operation: Operation) -> Output:
        token, param = control.check_serial_API6()
        if token == Token.cnfTest:
            if param == 0:
                control.emit_hw_test_starter(control)
                control.state = State.RUN_TEST
                control.logger.debug("State RUN_TEST")
                # TODO: need more informative messages for HW test
                return Output.NONE
            else:
                # any value of param other than 0 is some kind of error code
                control.logger.error(
                    "Device not ready, returned `cnfTest` with error code " + str(param)
                )
                # TODO: more output to describe error
                return Output.DEVICE_NOT_READY
        # else
        return Output.NONE

    @staticmethod
    def _API6_run_test(control: Control, operation: Operation) -> Output:
        # Any incoming testRes messages are processed in check_serial_API6,
        # there is nothing more to do here.
        control.check_serial_API6()
        return Output.NONE

    @staticmethod
    def _API6_finishing(control: Control, operation: Operation) -> Output:
        token, param = control.check_serial_API6()
        if token == Token.reqLine:
            control.cnf_final_line_API6(param)

            # When closing the serial port, the final bytes written
            # may be dropped by the driver
            # (see https://github.com/serialport/serialport-rs/issues/117).
            # This may cause the final `cnfLine` response to get lost and the
            # firmware to get stuck knitting the previous row
            # (see https://github.com/AllYarnsAreBeautiful/ayab-desktop/issues/662).
            # To avoid this, before closing the port, we send a `reqInfo` message
            # to the firmware and wait for the response.
            control.com.req_info()
            control.state = State.DISCONNECT
            control.logger.debug("State DISCONNECT")
            return Output.DISCONNECTING_FROM_MACHINE
        # else
        return Output.NONE

    @staticmethod
    def _API6_disconnect(control: Control, operation: Operation) -> Output:
        token, _ = control.check_serial_API6()
        if token == Token.cnfInfo:
            # We received a response to our final `reqInfo` request,
            # it is now safe to close the port.
            control.state = State.FINISHED
            return Output.KNITTING_FINISHED
        # else
        return Output.NONE

    @staticmethod
    def _API6_finished(control: Control, operation: Operation) -> Output:
        control.logger.debug("State FINISHED")
        return Output.NONE
