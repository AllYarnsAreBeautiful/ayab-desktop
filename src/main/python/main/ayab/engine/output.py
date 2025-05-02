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

from ..signal_sender import SignalSender
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..ayab import GuiMain


class Output(Enum):
    NONE = auto()
    ERROR_INVALID_SETTINGS = auto()
    ERROR_SERIAL_PORT = auto()
    CONNECTING_TO_MACHINE = auto()
    DISCONNECTING_FROM_MACHINE = auto()
    INITIALIZING_FIRMWARE = auto()
    WAIT_FOR_INIT = auto()
    ERROR_WRONG_API = auto()
    ERROR_INITIALIZING_FIRMWARE = auto()
    PLEASE_KNIT = auto()
    DEVICE_NOT_READY = auto()
    NEXT_LINE = auto()
    KNITTING_FINISHED = auto()


class FeedbackHandler(SignalSender):
    """Polymorphic dispatch of notification signals on KnitOutput.

    @author Tom Price
    @date   July 2020
    """

    def __init__(self, parent: GuiMain):
        super().__init__(parent.signal_receiver)

    def handle(self, result: Output) -> None:
        method = "_" + result.name.lower()
        if hasattr(self, method):
            dispatch = getattr(self, method)
            dispatch()

    def _none(self) -> None:
        self.emit_notification("", False)

    def _connecting_to_machine(self) -> None:
        self.emit_notification("Connecting to machine...", False)

    def _disconnecting_from_machine(self) -> None:
        self.emit_notification("Disconnecting from machine...")

    def _initializing_firmware(self) -> None:
        self.emit_notification("Initializing firmware")

    def _error_initializing_firmware(self) -> None:
        self.emit_notification("Error initializing firmware")

    def _error_serial_port(self) -> None:
        self.emit_notification("Error opening serial port")

    def _wait_for_init(self) -> None:
        self.emit_notification(
            "Please start machine. (Set the carriage to mode KC-I "
            + "or KC-II and move the carriage over the left turn mark)."
        )

    def _error_wrong_api(self) -> None:
        self.emit_popup(
            "Wrong Arduino firmware version. Please check "
            + "that you have flashed the latest version."
        )
        # + " (" + str(self.__control.API_VERSION) + ")")

    def _please_knit(self) -> None:
        self.emit_notification("Please knit.")
        self.emit_audio_player("start")

    def _device_not_ready(self) -> None:
        self.emit_notification("", False)
        self.emit_blocking_popup("Device not ready, try again.")

    def _next_line(self) -> None:
        self.emit_audio_player("nextline")

    def _knitting_finished(self) -> None:
        self.emit_audio_player("finish")
        self.emit_notification(
            "Image transmission finished. Please knit until you "
            + "hear the double beep sound."
        )
