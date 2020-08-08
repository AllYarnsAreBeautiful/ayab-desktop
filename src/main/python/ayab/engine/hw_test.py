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

from .communication import Communication
from .communication_mockup import CommunicationMockup
from .hw_test_mock import HardwareTestMock
from .cmd_line import CmdLine
from ..thread import GenericThread
"""Console for hardware test."""


class HardwareTest(QDialog):
    def __init__(self):
        super().__init__()
        # self.setModal(True)
        self.setWindowTitle("Hardware Test")
        self.resize(800, 800)
        self.__hw = HardwareTestMock(self)
        self.__layout = QVBoxLayout()
        self.__console = QPlainTextEdit(self)
        self.__console.setReadOnly(True)
        self.__cmd_line = CmdLine(self)
        self.__layout.addWidget(self.__console)
        # self.__cmd_line.grabKeyboard()
        self.setLayout(self.__layout)
        # font = QFont("Ubuntu Mono", 14)
        font = QFont("Courier New", 14)
        self.__console.setFont(font)
        self.__cmd_line.setFont(font)
        self.__layout.addWidget(self.__cmd_line)
        self.__bar = self.__console.verticalScrollBar()
        self.open()

    def open(self):
        # if portname == Simulation:
        self.__test_mock_thread = GenericThread(self.__hw.loop)
        self.__test_mock_thread.finished.connect(self.quit)
        self.__test_mock_thread.start()
        self.show()

    def hw_test_send_cmd_API6(self, cmd):
        self.__hw.send(cmd)
        self.__console.appendPlainText("$ " + cmd + "\n")
        self.__bar.setValue(self.__bar.maximum())

    def hw_test_read_API6(self, msg):
        self.__console.insertPlainText(msg)
        self.__bar.setValue(self.__bar.maximum())

    def quit(self):
        # HardwareTestMock.loop() already finished
        # close serial connection
        # close dialog
        self.accept()
