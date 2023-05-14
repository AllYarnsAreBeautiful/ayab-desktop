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

from copy import copy
import serial
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPlainTextEdit, QButtonGroup, QPushButton, QGroupBox, QHBoxLayout, QCheckBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer

#from .cmd_buttons import CmdButtons
from .state import State
from .communication import Token
from .hw_test_communication_mock import HardwareTestCommunicationMock


class HardwareTestDialog(QDialog):
    """Console for hardware tests."""

    commands = ["help", "send", "beep", "read", "auto", "test", "quit"] 

    def __init__(self, parent):
        super().__init__()
        self.setModal(True)
        self.setWindowTitle("Hardware Test")  # TODO: translate
        self.resize(800, 800)
        self.__layout = QVBoxLayout()

        # console
        self.__console = QPlainTextEdit(self)
        self.__console.setReadOnly(True)
        self.__bar = self.__console.verticalScrollBar()
        font = QFont("Courier New", 14)
        self.__console.setFont(font)
        self.__layout.addWidget(self.__console)

        # command buttons
        self.__command_box = QGroupBox("Commands")
        self.__button_row = QHBoxLayout()
        for button in self.commands:
            name = "_" + button + "_button"
            setattr(self, name, QPushButton(button.title()))
            widget = getattr(self, name)
            self.__button_row.addWidget(widget)
            widget.clicked.connect(
                lambda state, widget=widget, button=button:
                self.__button_pushed(widget, button))
        self._auto_button.setCheckable(True)  # toggles on/off
        self._test_button.setCheckable(True)  # toggles on/off
        self.__command_box.setLayout(self.__button_row)
        self.__layout.addWidget(self.__command_box)

        # solenoid checkboxes
        self.__solenoids = QGroupBox("Solenoids")
        self.__solenoid_row = QHBoxLayout()
        self.__solenoid = list()
        for s in range(16):
            self.__solenoid.append(QCheckBox(str(s)))
            self.__solenoid_row.addWidget(self.__solenoid[s])
            self.__solenoid[s].toggled.connect(
                lambda state, idx = s: self.__set_solenoid(idx))
        self.__solenoids.setLayout(self.__solenoid_row)
        self.__layout.addWidget(self.__solenoids)
        self.setLayout(self.__layout)

        # TODO: customize appearance of solenoid checkboxes
        self.setStyleSheet("""
        QCheckBox {}
        """)

    def open(self, control):
        self.__control = control
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.timer_event)
        if isinstance(self.__control.com, HardwareTestCommunicationMock):
            self.__control.com.setup()
            self.__timer.start(500)  # every 0.5 s
        self.show()

    def timer_event(self):
        self.__control.com.timer_event()

    def output(self, msg):
        self.__console.insertPlainText(msg)
        self.__bar.setValue(self.__bar.maximum())

    def hideEvent(self, event):
        self.__timer.stop()
        self.__console.setPlainText("")
        self.__control.state == State.FINISHED
        self.accept()

    def reject(self):
        # reset dialog
        self._auto_button.setChecked(False)
        self._test_button.setChecked(False)
        for s in range(16):
            self.__solenoid[s].setChecked(False)
        self.hide()

    def __button_pushed(self, widget: QPushButton, button: str) -> None:
        payload = bytearray()
        token = getattr(Token, button + "Cmd").value
        payload.append(token)
        if button in ["auto", "test"]:
            val = widget.isChecked()
            payload.append(val)
            self.output("\n> " + button + " " + str(int(val)) + "\n")
        else:
            self.output("\n> " + button + "\n")
        if button == "quit":
            self.reject()
        self.__control.com.write_API6(payload)

    def __set_solenoid(self, idx: int) -> None:
        val = self.__solenoid[idx].isChecked()
        self.output("\n> set " + str(idx) + " " + str(int(val)) + "\n")
        payload = bytearray()
        payload.append(Token.setCmd.value)
        payload.append(idx)
        payload.append(val)
        self.__control.com.write_API6(payload)
