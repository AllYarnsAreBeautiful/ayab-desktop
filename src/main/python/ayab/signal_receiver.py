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
from .engine.status import Status
from .engine.options import Alignment
from .engine.state import Operation
from .engine.control import Control
from .utils import display_blocking_popup


class Observer(QObject):
    """
    Container for signals.

    @author Tom Price
    @date   July 2020
    """
    # signals are defined as class attributes which are
    # over-ridden by instance attributes with the same name
    start_row_updater = pyqtSignal(int)
    progress_bar_updater = pyqtSignal(int, int, int, 'QString')
    knit_progress_updater = pyqtSignal(Status, int, int, bool)
    notifier = pyqtSignal('QString', bool)
    # statusbar_updater = pyqtSignal('QString', bool)
    popup_displayer = pyqtSignal('QString', 'QString')
    blocking_popup_displayer = pyqtSignal('QString', 'QString')
    audio_player = pyqtSignal('QString')
    needles_updater = pyqtSignal(int, int)
    alignment_updater = pyqtSignal(Alignment)
    image_resizer = pyqtSignal()
    got_image_flag = pyqtSignal()
    new_image_flag = pyqtSignal()
    bad_config_flag = pyqtSignal()
    knitting_starter = pyqtSignal()
    operation_finisher = pyqtSignal(Operation, bool)
    hw_test_starter = pyqtSignal(Control)
    hw_test_writer = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def signals(self):
        """Iterator over names of signals."""
        return filter(
            lambda x: type(getattr(self, x)).__name__ == "pyqtBoundSignal",
            Observer.__dict__.keys())

    def activate_signals(self, parent):
        self.start_row_updater.connect(parent.update_start_row)
        self.progress_bar_updater.connect(parent.progbar.update)
        self.knit_progress_updater.connect(parent.knitprog.update)
        self.notifier.connect(parent.notify)
        # self.statusbar_updater.connect(parent.statusbar.update)
        self.blocking_popup_displayer.connect(display_blocking_popup)
        self.popup_displayer.connect(display_blocking_popup)
        self.audio_player.connect(parent.audio.play,
                                  type=Qt.BlockingQueuedConnection)
        self.needles_updater.connect(parent.scene.update_needles)
        self.alignment_updater.connect(parent.scene.update_alignment)
        self.image_resizer.connect(parent.set_image_dimensions)
        self.operation_finisher.connect(parent.finish_operation)
        self.hw_test_starter.connect(parent.hw_test.open)
        self.hw_test_writer.connect(parent.hw_test.output)
