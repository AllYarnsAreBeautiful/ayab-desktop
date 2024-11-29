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

from PySide6.QtCore import QCoreApplication
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .signal_receiver import SignalReceiver
    from .utils import MessageTypes
    from .engine.status import Status
    from .engine.engine_fsm import Operation
    from .engine.options import Alignment
    from .engine.control import Control


class SignalSender(object):
    """
    Contains `emit` methods for all the signals in the `SignalReceiver` class.

    @author Tom Price
    @date   July 2020
    """

    def __init__(
        self, signal_receiver: SignalReceiver, *args: Any, **kwargs: Any
    ) -> None:
        self.__signal_receiver = signal_receiver
        super().__init__(*args, **kwargs)

    def emit_start_row_updater(self, start_row: int) -> None:
        self.__signal_receiver.start_row_updater.emit(start_row)

    def emit_progress_bar_updater(self, status: Status) -> None:
        self.__signal_receiver.progress_bar_updater.emit(status)

    def emit_knit_progress_updater(
        self, status: Status, row_multiplier: int, midline: int, auto_mirror: bool
    ) -> None:
        self.__signal_receiver.knit_progress_updater.emit(
            status, row_multiplier, midline, auto_mirror
        )

    def emit_notifier(self, text: str, log: bool) -> None:
        self.__signal_receiver.notifier.emit(text, log)

    def emit_popup_displayer(self, message: str, message_type: MessageTypes) -> None:
        self.__signal_receiver.popup_displayer.emit(message, message_type)

    def emit_blocking_popup_displayer(
        self, message: str, message_type: MessageTypes
    ) -> None:
        self.__signal_receiver.blocking_popup_displayer.emit(message, message_type)

    def emit_audio_player(self, sound: str) -> None:
        self.__signal_receiver.audio_player.emit(sound)

    def emit_needles_updater(self, start_needle: int, stop_needle: int) -> None:
        self.__signal_receiver.needles_updater.emit(start_needle, stop_needle)

    def emit_alignment_updater(self, alignment: Alignment) -> None:
        self.__signal_receiver.alignment_updater.emit(alignment)

    def emit_image_resizer(self) -> None:
        self.__signal_receiver.image_resizer.emit()

    def emit_image_reverser(self, image_reversed: bool) -> None:
        self.__signal_receiver.image_reverser.emit(image_reversed)

    def emit_got_image_flag(self) -> None:
        self.__signal_receiver.got_image_flag.emit()

    def emit_new_image_flag(self) -> None:
        self.__signal_receiver.new_image_flag.emit()

    def emit_bad_config_flag(self) -> None:
        self.__signal_receiver.bad_config_flag.emit()

    def emit_knitting_starter(self) -> None:
        self.__signal_receiver.knitting_starter.emit()

    def emit_operation_finisher(self, operation: Operation) -> None:
        self.__signal_receiver.operation_finisher.emit(operation)

    def emit_hw_test_starter(self, control: Control) -> None:
        self.__signal_receiver.hw_test_starter.emit(control)

    def emit_hw_test_writer(self, msg: str) -> None:
        self.__signal_receiver.hw_test_writer.emit(msg)

    # Meta Emitters
    def emit_blocking_popup(
        self, message: str = "", message_type: MessageTypes = "info"
    ) -> None:
        """Sends the blocking_popup_displayer signal."""
        self.emit_blocking_popup_displayer(
            QCoreApplication.translate("AyabPlugin", message), message_type
        )

    def emit_popup(
        self, message: str = "", message_type: MessageTypes = "info"
    ) -> None:
        """Sends the popup_displayer signal."""
        self.emit_popup_displayer(
            QCoreApplication.translate("AyabPlugin", message), message_type
        )

    def emit_notification(self, message: str = "", log: bool = True) -> None:
        """Sends the notifier signal."""
        self.emit_notifier(QCoreApplication.translate("AyabPlugin", message), log)
