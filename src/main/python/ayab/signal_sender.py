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

from PySide6.QtCore import QCoreApplication


class SignalSender(object):
    """
    Contains `emit` methods for all the signals in the `SignalReceiver` class.

    @author Tom Price
    @date   July 2020
    """
    def __init__(self, signal_receiver, *args, **kwargs):
        self.__signal_receiver = signal_receiver
        for s in self.__signal_receiver.signals():
            setattr(self, "emit_" + s, self.__make_emit_method(s))
        super().__init__(*args, **kwargs)

    def __make_emit_method(self, signal):
        return lambda *args: getattr(self.__signal_receiver, signal).emit(*args)

    def emit_blocking_popup(self, message="", message_type="info"):
        """Sends the blocking_popup_displayer signal."""
        self.emit_blocking_popup_displayer(
            QCoreApplication.translate("AyabPlugin", message), message_type)

    def emit_popup(self, message="", message_type="info"):
        """Sends the popup_displayer signal."""
        self.emit_popup_displayer(
            QCoreApplication.translate("AyabPlugin", message), message_type)

    def emit_notification(self, message="", log=True):
        """Sends the notifier signal."""
        self.emit_notifier(QCoreApplication.translate("AyabPlugin", message),
                           log)
