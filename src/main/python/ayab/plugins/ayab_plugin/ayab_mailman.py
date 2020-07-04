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

from PyQt5.QtCore import QTranslator, QCoreApplication
from .ayab_options import Options, KnittingMode, Alignment, NeedleColor


class SignalEmitter(object):
    """Encapsulates signal emission methods.

    @author Tom Price
    @date   July 2020
    """
    def __init__(self, signal_receiver):
        self.__mailbox = signal_receiver

    def emit_blocking_popup(self, message="", message_type="info"):
        """
        Sends the signal.display_blocking_popup QtSignal
        to main GUI thread, blocking it.
        """
        self.__mailbox.blocking_popup_displayer.emit(
            QCoreApplication.translate("AyabPlugin", message), message_type)

    def emit_popup(self, message="", message_type="info"):
        """
        Sends the signal_display_popup QtSignal
        to main GUI thread, not blocking it.
        """
        self.__mailbox.popup_displayer.emit(
            QCoreApplication.translate("AyabPlugin", message), message_type)

    def emit_configure_fail(self, message=""):
        self.emit_popup(message)
        self.__mailbox.configuration_fail_flagger.emit()

    def emit_notification(self, message="", log=True):
        """Sends the notification_updater signal"""
        self.__mailbox.notification_updater.emit(
            QCoreApplication.translate("AyabPlugin", message), log)

    def emit_knit_progress(self, status, row_multiplier):
        """Sends the knit_progress_updater QtSignal."""
        self.__mailbox.knit_progress_updater.emit(status, row_multiplier)

    def emit_progress(self, row, total=0, repeats=0, color_symbol=""):
        """Sends the progress_bar_updater QtSignal."""
        self.__mailbox.progress_bar_updater.emit(row, total, repeats,
                                                 color_symbol)

    def emit_start_row(self, start_row):
        """Sends the start_row_updater QtSignal."""
        self.__mailbox.start_row_updater.emit(start_row)

    def emit_image_transformed(self):
        """Sends the image_transformed_flagger QtSignal."""
        self.__mailbox.image_transformed_flagger.emit()

    def emit_image_dimensions(self):
        """Sends the image_sizer QtSignal."""
        self.__mailbox.image_sizer.emit()

    def emit_update_needles(self, ui):
        """Sends the needles_updater QtSignal."""
        start_needle = NeedleColor.read_start_needle(ui)
        stop_needle = NeedleColor.read_stop_needle(ui)
        self.__mailbox.needles_updater.emit(start_needle, stop_needle)

    def emit_update_alignment(self, ui):
        """Sends the alignment_updater QtSignal"""
        alignment = Alignment(ui.alignment_combo_box.currentIndex())
        self.__mailbox.alignment_updater.emit(alignment)

    def emit_audio(self, event):
        # blocking connection means that thread waits until sound has finished playing
        self.__mailbox.audio_player.emit(event)

    def emit_configured(self):
        self.__mailbox.configured_flagger.emit()

    def emit_done_knitting(self, flag):
        self.__mailbox.knitting_finisher.emit(flag)
