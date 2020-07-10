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

from PyQt5.QtCore import QCoreApplication


class Observable(object):
    """
    Contains `emit` methods for all the signals in the `Observer` class.

    @author Tom Price
    @date   July 2020
    """
    def __init__(self, observer, *args, **kwargs):
        self.__seer = observer
        for s in self.__seer.signals():
            setattr(self, "emit_" + s, self.__make_emit_method(s))
        super().__init__(*args, **kwargs)

    def __make_emit_method(self, signal):
        return lambda *args: getattr(self.__seer, signal).emit(*args)

    def emit_blocking_popup(self, message="", message_type="info"):
        """Sends the blocking_popup_displayer signal."""
        self.emit_blocking_popup_displayer(
            QCoreApplication.translate("AyabPlugin", message), message_type)

    def emit_popup(self, message="", message_type="info"):
        """Sends the popup_displayer signal."""
        self.emit_popup_displayer(
            QCoreApplication.translate("AyabPlugin", message), message_type)

    def emit_notification(self, message="", log=True):
        """Sends the notification_updater signal."""
        self.emit_notification_updater(
            QCoreApplication.translate("AyabPlugin", message), log)
