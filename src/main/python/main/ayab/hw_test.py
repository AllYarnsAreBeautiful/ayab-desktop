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

from __future__ import annotations
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QGroupBox,
    QHBoxLayout,
    QCheckBox,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import QTimer

# from .cmd_buttons import CmdButtons
from .engine.engine_fsm import State
from .engine.communication import Token
from .engine.hw_test_communication_mock import HardwareTestCommunicationMock
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ayab import GuiMain


class HardwareTestDialog(QDialog):
    """Console for hardware tests."""

    commands = [
        "help",
        "send",
        "beep",
        "readEOLsensors",
        "readEncoders",
        "autoRead",
        "autoTest",
        "quit",
    ]

    def __init__(self, parent: GuiMain):
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
            widget: QPushButton = QPushButton(button)
            widget.setAutoDefault(False)
            self.__button_row.addWidget(widget)
            widget.clicked.connect(
                lambda widget=widget, button=button: self.__button_pushed(
                    widget, button
                )
            )
            setattr(self, name, widget)
        self._autoRead_button.setCheckable(True)  # toggles on/off
        self._autoTest_button.setCheckable(True)  # toggles on/off
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
                lambda state, idx=s: self.__set_solenoid(idx)
            )
        self.__solenoids.setLayout(self.__solenoid_row)
        self.__layout.addWidget(self.__solenoids)
        self.setLayout(self.__layout)

        # TODO: customize appearance of solenoid checkboxes
        self.setStyleSheet(
            """
        QCheckBox {}
        """
        )

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
        assert self.__control.state == State.FINISHED
        self.accept()

    def reject(self):
        # send quitCmd
        payload = bytearray()
        token = Token.quitCmd.value
        payload.append(token)
        self.__control.com.write_API6(payload)
        self.__control.state = State.FINISHED
        # reset dialog
        self._autoRead_button.setChecked(False)
        self._autoTest_button.setChecked(False)
        for s in range(16):
            self.__solenoid[s].setChecked(False)
        self.hide()

    def __button_pushed(self, widget: QPushButton, button: str) -> None:
        if button == "quit":
            self.reject()
        else:
            payload = bytearray()
            if widget.isCheckable() and not widget.isChecked():
                payload.append(Token.stopCmd.value)
                self.output("\n> stop\n")
                self._autoRead_button.setChecked(False)
                self._autoTest_button.setChecked(False)
            else:
                token = getattr(Token, button + "Cmd").value
                payload.append(token)
                self.output("\n> " + button + "\n")
            self.__control.com.write_API6(payload)

    def __set_solenoid(self, idx: int) -> None:
        val = self.__solenoid[idx].isChecked()
        self.output("\n> setSingle " + str(idx) + " " + str(int(val)) + "\n")
        payload = bytearray()
        payload.append(Token.setSingleCmd.value)
        payload.append(idx)
        payload.append(val)
        self.__control.com.write_API6(payload)
