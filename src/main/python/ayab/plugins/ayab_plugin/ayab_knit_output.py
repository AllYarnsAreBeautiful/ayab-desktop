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

from enum import Enum
from .ayab_observable import Observable


class KnitOutput(Enum):
    NONE = 0
    ERROR_INVALID_SETTINGS = 1
    ERROR_SERIAL_PORT = 2
    CONNECTING_TO_MACHINE = 3
    WAIT_FOR_INIT = 4
    ERROR_WRONG_API = 5
    PLEASE_KNIT = 6
    DEVICE_NOT_READY = 7
    FINISHED = 8


class KnitFeedbackHandler(Observable):
    """Polymorphic dispatch of notification signals on KnitOutput.

    @author Tom Price
    @data   July 2020
    """
    def __init__(self, parent):
        super().__init__(parent.seer)

    def handle(self, result):
        method = "_" + result.name.lower()
        if hasattr(self, method):
            dispatch = getattr(self, method)
            dispatch()

    def _connecting_to_machine(self):
        self.emit_notification("Connecting to machine...", False)

    def _wait_for_init(self):
        self.emit_notification(
            "Please start machine. (Set the carriage to mode KC-I " +
            "or KC-II and move the carriage over the left turn mark).")

    def _error_wrong_api(self):
        self.emit_popup("Wrong Arduino firmware version. Please check " +
                        "that you have flashed the latest version.")
        # + " (" + str(self.__control.API_VERSION) + ")")

    def _please_knit(self):
        self.emit_notification("Please knit.")
        self.emit_audio_player("start")

    def _device_not_ready(self):
        self.emit_notification("", False)
        self.emit_blocking_popup("Device not ready, try again.")

    def _finished(self):
        self.emit_notification(
            "Image transmission finished. Please knit until you " +
            "hear the double beep sound.")
