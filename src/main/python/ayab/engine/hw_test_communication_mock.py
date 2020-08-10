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

from time import sleep
from collections import deque
from PyQt5.QtCore import QObject, pyqtSignal

from .communication_mock import CommunicationMock


class HardwareTestCommunicationMock(QObject, CommunicationMock):
    commands = [
        "setSingle", "setAll", "readEOLsensors", "readEncoders", "beep",
        "autoRead", "autoTest", "send", "stop", "quit", "help", "test"
    ]

    def __init__(self):
        super().__init__()
        self.__autoReadOn = False
        self.__autoTestOn = False
        self.__output = deque()  # FIFO
        self.__flag = True
        self.setup()

    def setup(self):
        self.__output.appendleft("AYAB Hardware Test v1.0 API v6\n\n")
        self.helpCmd([])

    def write_API6(self, cmd: str) -> None:
        tokens = cmd.lower().split()
        try:
            i = [x.lower() for x in self.commands].index(tokens[0])
        except Exception as e:
            self.unrecognizedCmd(cmd)
        else:
            dispatch = getattr(self, self.commands[i] + "Cmd")
            dispatch(tokens)

    def read_API6(self) -> str:
        if len(self.__output) == 0:
            return ""
        # else
        return self.__output.pop()

    def prompt(self):
        # self.__output.appendleft("$ \n")
        pass

    def helpCmd(self, tokens):
        self.__output.appendleft("The following commands are available:\n")
        self.__output.appendleft("setSingle [0..15] [1/0]\n")
        self.__output.appendleft("setAll [0..255] [0..255]\n")
        self.__output.appendleft("readEOLsensors\n")
        self.__output.appendleft("readEncoders\n")
        self.__output.appendleft("beep\n")
        self.__output.appendleft("autoRead\n")
        self.__output.appendleft("autoTest\n")
        self.__output.appendleft("send\n")
        self.__output.appendleft("stop\n")
        self.__output.appendleft("help\n")

    def sendCmd(self, tokens):
        self.__output.appendleft("Called send\n")
        self.__output.appendleft("\x01\x02\x03\n")  # FIXME ???

    def beep(self):
        pass

    def beepCmd(self, tokens):
        self.__output.appendleft("Called beep\n")

    def encoderAChange(self):
        self.beep()

    def setSingleCmd(self, tokens):
        self.__output.appendleft("Called setSingle\n")
        if len(tokens) < 2 or tokens[1] == "":
            return
        # else
        solenoidNumber = int(tokens[1])
        if (solenoidNumber > 15):
            self.__output.appendleft("Invalid argument: " +
                                     str(solenoidNumber) + "\n")
        # arguments ignored

    def setAllCmd(self, tokens):
        self.__output.appendleft("Called setAll\n")
        # arguments ignored

    def readEOLsensors(self, output):
        output.appendleft("  EOL_L: 0")
        output.appendleft("  EOL_R: 0")

    def readEOLsensorsCmd(self, tokens):
        self.__output.appendleft("Called readEOLsensors\n")
        self.readEOLsensors(self.__output)
        self.__output.appendleft("\n")

    def readEncoders(self, output):
        output.appendleft("  ENC_A: LOW")
        output.appendleft("  ENC_B: LOW")
        output.appendleft("  ENC_C: LOW")

    def readEncodersCmd(self, tokens):
        self.__output.appendleft("Called readEncoders\n")
        self.readEncoders(self.__output)
        self.__output.appendleft("\n")

    def autoRead(self):
        self.readEOLsensors(self.__output)
        self.readEncoders(self.__output)
        self.__output.appendleft("\n")
        #sleep(1)

    def autoReadCmd(self, tokens):
        self.__output.appendleft("Called autoRead, send stop to quit\n")
        self.__autoReadOn = True

    def autoTest_even(self):
        self.__output.appendleft("Set even solenoids\n")
        # sleep(0.5)

    def autoTest_odd(self):
        self.__output.appendleft("Set odd solenoids\n")
        # sleep(0.5)

    def autoTestCmd(self, tokens):
        self.__output.appendleft("Called autoTest, send stop to quit\n")
        self.__autoTestOn = True

    def stopCmd(self, tokens):
        self.__autoReadOn = False
        self.__autoTestOn = False

    def unrecognizedCmd(self, cmd):
        self.__output.appendleft("Unrecognized command: " + cmd + "\n")
        self.helpCmd([])

    def quitCmd(self, tokens):
        pass

    def testCmd(self, tokens):
        self.auto()

    def auto(self):
        self.__flag = not self.__flag
        if self.__autoReadOn:
            if self.__flag:
                self.autoRead()
        if self.__autoTestOn:
            if self.__flag:
                self.autoTest_even()
            else:
                self.autoTest_odd()
