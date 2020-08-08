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
from PyQt5.QtCore import QObject, pyqtSignal


class HardwareTestMock(QObject):
    hw_output_sender = pyqtSignal(str)
    commands = [
        "setSingle", "setAll", "readEOLsensors", "readEncoders", "beep",
        "autoRead", "autoTest", "send", "stop", "quit", "help"
    ]

    def __init__(self, parent):
        super().__init__()
        self.__autoReadOn = False
        self.__autoTestOn = False
        self.__output = list()
        self.__auto = list()
        self.__quit = False
        self.setup()
        self.hw_output_sender.connect(parent.hw_test_read_API6)

    def send(self, cmd):
        tokens = cmd.lower().split()
        try:
            i = [x.lower() for x in self.commands].index(tokens[0])
        except Exception as e:
            self.unrecognizedCmd(cmd)
        else:
            dispatch = getattr(self, self.commands[i] + "Cmd")
            dispatch(tokens)

    def read(self):
        output = "".join(self.__output)
        self.__output = list()
        self.hw_output_sender.emit(output)

    def prompt(self):
        # self.__output.append("$ \n")
        pass

    def helpCmd(self, tokens):
        self.__output.append("The following commands are available:\n")
        self.__output.append("setSingle [0..15] [1/0]\n")
        self.__output.append("setAll [0..255] [0..255]\n")
        self.__output.append("readEOLsensors\n")
        self.__output.append("readEncoders\n")
        self.__output.append("beep\n")
        self.__output.append("autoRead\n")
        self.__output.append("autoTest\n")
        self.__output.append("send\n")
        self.__output.append("stop\n")
        self.__output.append("help\n")

    def sendCmd(self, tokens):
        self.__output.append("Called send\n")
        self.__output.append("\x01\x02\x03\n")  # FIXME ???

    def beep(self):
        pass

    def beepCmd(self, tokens):
        self.__output.append("Called beep\n")

    def encoderAChange(self):
        self.beep()

    def setSingleCmd(self, tokens):
        self.__output.append("Called setSingle\n")
        if tokens[1] == "":
            return
        # else
        solenoidNumber = int(tokens[1])
        if (solenoidNumber > 15):
            self.__output.append("Invalid argument: " + str(solenoidNumber) +
                                 "\n")
        # else

    def setAllCmd(self, tokens):
        self.__output.append("Called setAll\n")
        if tokens[1] == "":
            return
        # else
        if tokens[2] == "":
            return
        # else

    def readEOLsensors(self, output):
        output.append("  EOL_L: 0")
        output.append("  EOL_R: 0")

    def readEOLsensorsCmd(self, tokens):
        self.__output.append("Called readEOLsensors\n")
        self.readEOLsensors(self.__output)
        self.__output.append("\n")

    def readEncoders(self, output):
        output.append("  ENC_A: LOW")
        output.append("  ENC_B: LOW")
        output.append("  ENC_C: LOW")

    def readEncodersCmd(self, tokens):
        self.__output.append("Called readEncoders\n")
        self.readEncoders(self.__output)
        self.__output.append("\n")

    def autoRead(self):
        self.readEOLsensors(self.__auto)
        self.readEncoders(self.__auto)
        self.__auto.append("\n")
        sleep(1)

    def autoReadCmd(self, tokens):
        self.__output.append("Called autoRead, send stop to quit\n")
        self.__autoReadOn = True

    def autoTest(self):
        self.__auto.append("Set even solenoids\n")
        sleep(0.5)
        self.__auto.append("Set odd solenoids\n")
        sleep(0.5)

    def autoTestCmd(self, tokens):
        self.__output.append("Called autoTest, send stop to quit\n")
        self.__autoTestOn = True

    def stopCmd(self, tokens):
        self.__autoReadOn = False
        self.__autoTestOn = False

    def unrecognizedCmd(self, cmd):
        self.__output.append("Unrecognized command: " + cmd + "\n")
        self.helpCmd([])

    def setup(self):
        self.__output.append("AYAB Hardware Test v1.0 API v6\n\n")
        self.helpCmd([])

    def quitCmd(self, tokens):
        self.__quit = True

    def loop(self):
        while not self.__quit:
            if self.__autoReadOn:
                self.autoRead()
            if self.__autoTestOn:
                self.autoTest()
            if len(self.__output) > 0:
                self.read()
            if len(self.__auto) > 0:
                if self.__autoReadOn or self.__autoTestOn:
                    self.__output = self.__auto
                    self.read()
                self.__auto = list()
