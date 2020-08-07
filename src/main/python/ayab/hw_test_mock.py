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


class HardwareTestMock(object):
    commands = [
        "setSingle", "setAll", "readEOLsensors", "readEncoders", "beep",
        "autoRead", "autoTest", "send", "stop", "help"
    ]

    def __init__(self):
        self.autoReadOn = False
        self.autoTestOn = False
        self.__output = []
        self.setup()

    def send(self, cmd):
        tokens = cmd.split()
        if tokens[0] in self.commands:
            dispatch = getattr(self, tokens[0] + "Cmd")
            dispatch(self, tokens)
        else:
            self.unrecognizedCmd(cmd)

    def read(self):
        output = self.__output.join
        self.output = []
        return output

    def prompt(self):
        self.__output.append("$ \n")

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
        self.__output.append("help\n")
        self.prompt()

    def sendCmd(self, tokens):
        self.__output.append("Called send\n")
        self.__output.append("\x01\x02\x03\n")
        self.prompt()

    def beep(self):
        pass

    def beepCmd(self, tokens):
        self.__output.append("Called beep\n")
        self.prompt()

    def encoderAChange(self):
        self.beep()

    def setSingleCmd(self, tokens):
        self.__output.append("Called setSingle\n")
        if tokens[1] == "":
            return
        # else
        solenoidNumber = int(arg)
        if (solenoidNumber > 15):
            self.__output.append("Invalid argument: " + str(solenoidNumber) +
                                 "\n")
            return
        # else
        self.prompt()

    def setAllCmd(self, tokens):
        self.__output.append("Called setAll\n")
        if tokens[1] == "":
            return
        # else
        if tokens[2] == "":
            return
        # else
        self.prompt()

    def readEOLsensors(self):
        self.__output.append("  EOL_L: 0")
        self.__output.append("  EOL_R: 0")

    def readEOLsensorsCmd(self, tokens):
        self.__output.append("Called readEOLsensors\n")
        self.readEOLsensors()
        self.__output.append("\n")
        self.prompt()

    def readEncoders(self):
        self.__output.append("  ENC_A: LOW")
        self.__output.append("  ENC_B: LOW")
        self.__output.append("  ENC_C: LOW")

    def readEncodersCmd(self, tokens):
        self.__output.append("Called readEncoders\n")
        self.readEncoders()
        self.__output.append("\n")
        self.prompt()

    def autoRead(self):
        self.__output.append("\n")
        self.readEOLsensors()
        self.readEncoders()
        self.__output.append("\n")
        self.prompt()
        sleep(1)

    def autoReadCmd(self, tokens):
        self.__output.append("Called autoRead, send stop to quit\n")
        self.autoReadOn = True
        self.readEncoders()
        self.__output.append("\n")
        self.prompt()

    def autoTest(self):
        self.__output.append("\n")
        self.__output.append("Set even solenoids\n")
        sleep(0.5)
        self.__output.append("\n")
        self.__output.append("Set odd solenoids\n")
        self.prompt()
        sleep(0.5)

    def autoTestCmd(self, tokens):
        self.__output.append("Called autoTest, send stop to quit\n")
        self.autoTestOn = True

    def stopCmd(self, tokens):
        self.autoReadOn = True
        self.autoTestOn = True
        self.prompt()

    def unrecognizedCmd(self, cmd):
        self.__output.append("Unrecognized command\n")
        self.__output.append(cmd + "\n")
        self.helpCmd([])

    def setup(self):
        self.__output.append("AYAB Hardware Test v1.0 API v6\n\n")
        self.helpCmd([])

    def loop(self):
        if self.autoReadOn:
            self.autoRead()
        if self.autoTestOn:
            self.autoTest()
        # limit length of output to 100 strings
        self.__output = self.__output[:100]
