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

import serial
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPlainTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer

from .cmd_line import CmdLine
from .state import State
from .hw_test_communication_mock import HardwareTestCommunicationMock


class HardwareTestDialog(QDialog):
    """Console for hardware test."""
    def __init__(self, parent):
        super().__init__()
        self.setModal(True)
        self.setWindowTitle("Hardware Test")  # TODO: translate
        self.resize(800, 800)
        self.__cmd_line = CmdLine(self)
        self.__console = QPlainTextEdit(self)
        self.__console.setReadOnly(True)
        self.__layout = QVBoxLayout()
        self.__layout.addWidget(self.__console)
        self.__layout.addWidget(self.__cmd_line)
        self.setLayout(self.__layout)
        self.__bar = self.__console.verticalScrollBar()
        font = QFont("Courier New", 14)
        self.__console.setFont(font)
        self.__cmd_line.setFont(font)

    def open(self, control):
        # self.__cmd_line.grabKeyboard()
        self.__control = control
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.auto)
        if isinstance(self.__control.com, HardwareTestCommunicationMock):
            self.__timer.start(500)  # every 0.5 s
        self.show()

    def auto(self):
        self.__control.com.auto()

    def output(self, msg):
        self.__console.insertPlainText(msg)
        self.__bar.setValue(self.__bar.maximum())

    def send_cmd_API6(self, cmd):
        self.__control.com.write_API6(cmd)
        self.output("\n$ " + cmd + "\n")
        if cmd.lower() == "quit":
            self.hide()

    def hideEvent(self, event):
        self.__timer.stop()
        self.__console.setPlainText("")
        self.__control.state == State.FINISHED
        self.accept()
