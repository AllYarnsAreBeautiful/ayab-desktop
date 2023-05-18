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
#    Copyright 2013 Christian Obersteiner, Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

import re
from time import sleep
from PyQt5.QtCore import QObject, pyqtSignal

from .communication import Token
from .communication_mock import CommunicationMock


class HardwareTestCommunicationMock(QObject, CommunicationMock):
    """Simulate device for hardware tests."""
    def __init__(self):
        super().__init__()
        self.__tokens = [
            Token[key] for key in Token._member_map_.keys()
            if re.search("Cmd$", key)
        ]

    def setup(self):
        self.reset()
        self.__autoReadOn = False
        self.__autoTestOn = False
        self.__timer_event_odd = False
        self.__output(Token.testRes, "AYAB Hardware Test v1.0 API v6\n\n")
        self._handle_helpCmd(bytes())

    def write_API6(self, msg: bytes) -> None:
        token = msg[0]
        try:
            i = [t.value for t in self.__tokens].index(token)
        except ValueError:
            self.__handle_unrecognizedCmd()
        else:
            cmd = self.__tokens[i].name
            self.__output(Token.testRes,
                          "Called " + re.sub("CMD$", "", cmd.upper()) + "\n")
            dispatch = getattr(self, "_handle_" + cmd)
            dispatch(msg)

    def update_API6(self):
        return self.parse_API6(self.read_API6())

    def read_API6(self):
        if len(self.rx_msg_list) == 0:
            return None
        # else
        res = self.rx_msg_list.popleft()  # FIFO
        return res

    def __output(self, token: Token, msg: str) -> None:
        self.rx_msg_list.append(bytes([token.value]) + msg.encode())

    # command handlers

    def _handle_helpCmd(self, msg):
        self.__output(Token.testRes, "The following commands are available:\n")
        self.__output(Token.testRes, "SET solenoid [0..15] [0/1]\n")
        self.__output(Token.testRes, "READ encoders and EOL sensors\n")
        self.__output(Token.testRes, "AUTO [0/1] continuous reads\n")
        self.__output(Token.testRes, "TEST [0/1] toggle solenoids\n")
        self.__output(Token.testRes, "SEND a test message\n")
        self.__output(Token.testRes, "BEEP test buzzer\n")
        self.__output(Token.testRes, "HELP show commands\n")
        self.__output(Token.testRes, "QUIT\n")

    def _handle_sendCmd(self, msg):
        self.__output(Token.testRes, "\x31\x32\x33\n")

    def _handle_beepCmd(self, msg):
        self.__beep()

    def _handle_readCmd(self, msg):
        self.__read_EOL_sensors()
        self.__read_encoders()
        self.__output(Token.testRes, "\n")

    def _handle_autoCmd(self, msg):
        self.__autoReadOn = msg[1]

    def _handle_testCmd(self, msg):
        self.__autoTestOn = msg[1]

    def _handle_quitCmd(self, msg):
        pass

    def _handle_setCmd(self, msg):
        if len(msg) < 3:
            return
        # else
        try:
            solenoidNumber = int(msg[1])
        except ValueError:
            self.__bad_arg(msg[1])
            return
        if (solenoidNumber < 0 or solenoidNumber > 15):
            self.__bad_arg(msg[1])
            return
        # else
        try:
            solenoidValue = int(msg[2])
        except ValueError:
            self.__bad_arg(msg[2])
            return
        if (solenoidValue < 0 or solenoidValue > 1):
            self.__bad_arg(msg[2])
            return
        # arguments ignored

    def __handle_unrecognizedCmd():
        pass

    def __beep(self):
        pass

    def __read_EOL_sensors(self):
        self.__output(Token.testRes, "  EOL_L: 0")
        self.__output(Token.testRes, "  EOL_R: 0")

    def __read_encoders(self):
        self.__output(Token.testRes, "  ENC_A: LOW")
        self.__output(Token.testRes, "  ENC_B: LOW")
        self.__output(Token.testRes, "  ENC_C: LOW")

    def __bad_arg(self, arg):
        self.__output(Token.testRes, "Invalid argument: " + arg + "\n")

    # timer event handlers

    def timer_event(self):
        if self.__autoReadOn:
            if self.__timer_event_odd:
                self.__auto_read()
        if self.__autoTestOn:
            if self.__timer_event_odd:
                self.__auto_test_odd()
            else:
                self.__auto_test_even()
        self.__timer_event_odd = not self.__timer_event_odd

    def __auto_read(self):
        self.__read_EOL_sensors()
        self.__read_encoders()
        self.__output(Token.testRes, "\n")

    def __auto_test_even(self):
        self.__output(Token.testRes, "Set even solenoids\n")

    def __auto_test_odd(self):
        self.__output(Token.testRes, "Set odd solenoids\n")
