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
#    Copyright 2014 Sebastian Oliva, Christian Obersteiner, Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

from PyQt5.QtCore import QObject, pyqtSignal, Qt
from .plugins.ayab_plugin.ayab_status import Status
from .plugins.ayab_plugin.ayab_options import Alignment


class SignalReceiver(QObject):
    """Encapsulates signals and slots.

    @author Tom Price
    @date   July 2020
    """
    # signals are defined as class attributes which are
    # over-ridden by instance attributes with the same name
    start_row_updater = pyqtSignal(int)
    progress_bar_updater = pyqtSignal(int, int, int, 'QString')
    knit_progress_updater = pyqtSignal(Status, int)
    status_updater = pyqtSignal(int, int, 'QString', int)
    notification_updater = pyqtSignal('QString', bool)
    popup_displayer = pyqtSignal('QString', 'QString')
    blocking_popup_displayer = pyqtSignal('QString', 'QString')
    audio_player = pyqtSignal('QString')
    needles_updater = pyqtSignal(int, int)
    alignment_updater = pyqtSignal(Alignment)
    image_loaded_flagger = pyqtSignal()
    image_transformed_flagger = pyqtSignal()
    row_start_updater = pyqtSignal(int)
    image_sizer = pyqtSignal()
    configuration_fail_flagger = pyqtSignal()
    configured_flagger = pyqtSignal()
    knitting_finisher = pyqtSignal(bool)

    # knit_progress_finisher = pyqtSignal()

    def __init__(self):
        super().__init__()  # initialize superobject

    def connect_slots(self, parent):
        self.start_row_updater.connect(parent.update_start_row)
        self.progress_bar_updater.connect(parent.pb.update)
        self.knit_progress_updater.connect(parent.update_knit_progress,
                                           type=Qt.BlockingQueuedConnection)
        self.status_updater.connect(parent.update_status_tab)
        self.notification_updater.connect(parent.update_notification)
        self.blocking_popup_displayer.connect(parent.display_blocking_popup)
        self.popup_displayer.connect(parent.display_blocking_popup)
        self.audio_player.connect(parent.audio,
                                  type=Qt.BlockingQueuedConnection)
        self.needles_updater.connect(parent.scene.update_needles)
        self.alignment_updater.connect(parent.scene.update_alignment)
        self.image_sizer.connect(parent.set_image_dimensions)
        self.knitting_finisher.connect(parent.reset_ui_after_knitting)
