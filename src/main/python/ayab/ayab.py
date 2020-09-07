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
"""Provides a graphical interface for users to operate AYAB."""

from fbs_runtime.application_context.PyQt5 import ApplicationContext

import sys
import logging

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import Qt, QThread, QCoreApplication, QTimer

from .main_gui import Ui_MainWindow
from .fsm import FSM
from .observer import Observer
from .audio import AudioPlayer
from .menu import Menu
from .scene import Scene
from .transforms import Transform
from .firmware_flash import FirmwareFlash
from .preferences import Preferences
# from .statusbar import StatusBar
from .progressbar import ProgressBar
from .about import About
from .knitprogress import KnitProgress
from .thread import GenericThread
from .engine import Engine
from .engine.state import Operation
from .engine.options import Alignment
from .engine.hw_test import HardwareTestDialog
from .machine import Machine


class GuiMain(QMainWindow):
    """
    GuiMain is the top level class in the AYAB GUI.

    GuiMain inherits from QMainWindow and instantiates a window with
    components from `menu_gui.ui`.
    """
    def __init__(self, app_context):
        super().__init__()
        self.app_context = app_context

        # get preferences
        self.seer = Observer()
        self.prefs = Preferences(self)

        # create UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # add modular components
        self.menu = Menu(self)
        self.setMenuBar(self.menu)
        # self.statusbar = StatusBar(self)
        # self.setStatusBar(self.statusbar)
        self.about = About(self)
        self.scene = Scene(self)
        self.knitprog = KnitProgress(self)
        self.engine = Engine(self)
        self.hw_test = HardwareTestDialog(self)
        self.progbar = ProgressBar(self)
        self.flash = FirmwareFlash(self)
        self.audio = AudioPlayer(self)
        self.knit_thread = GenericThread(self.engine.run, Operation.KNIT)
        self.test_thread = GenericThread(self.engine.run, Operation.TEST)

        # show UI
        self.showMaximized()

        # Activate signals and UI elements
        self.seer.activate_signals(self)
        self.__activate_ui()
        self.__activate_menu()

        # initialize FSM
        self.fsm = FSM()
        self.fsm.set_transitions(self)
        self.fsm.set_properties(self)
        self.fsm.machine.start()

    def __activate_ui(self):
        self.ui.load_file_button.clicked.connect(
            self.scene.ayabimage.select_file)
        self.ui.filename_lineedit.returnPressed.connect(
            self.scene.ayabimage.select_file)
        self.ui.cancel_button.clicked.connect(self.engine.cancel)
        self.hw_test.finished.connect(
            lambda: self.finish_operation(Operation.TEST, False))

    def __activate_menu(self):
        self.menu.ui.action_quit.triggered.connect(
            QCoreApplication.instance().quit)
        self.menu.ui.action_load_AYAB_firmware.triggered.connect(
            self.flash.open)
        self.menu.ui.action_set_preferences.triggered.connect(
            self.prefs.open_dialog)
        self.menu.ui.action_about.triggered.connect(self.about.show)
        # get names of image actions from Transform methods
        transforms = filter(lambda x: x[0] != "_", Transform.__dict__.keys())
        for t in transforms:
            action = getattr(self.menu.ui, "action_" + t)
            slot = getattr(self.scene.ayabimage, t)
            action.triggered.connect(slot)

    def start_knitting(self):
        """Start the knitting process."""
        self.start_operation()
        # reset knit progress window
        self.knitprog.start()
        # start thread for knit engine
        self.knit_thread.start()

    def start_testing(self):
        """Start the testing process."""
        self.start_operation()
        # start thread for test engine
        self.test_thread.start()

    def start_operation(self):
        """Disable UI elements at start of operation."""
        self.menu.depopulate()
        self.ui.filename_lineedit.setEnabled(False)
        self.ui.load_file_button.setEnabled(False)

    def finish_operation(self, operation: Operation, beep: bool):
        """(Re-)enable UI elements after operation finishes."""
        self.menu.repopulate()
        self.ui.filename_lineedit.setEnabled(True)
        self.ui.load_file_button.setEnabled(True)
        if operation == Operation.KNIT and beep:
            self.audio.play("finish")

    def set_image_dimensions(self):
        """Set dimensions of image."""
        width, height = self.scene.ayabimage.image.size
        self.engine.config.update_needles()  # in case machine width changed
        self.engine.config.set_image_dimensions(width, height)
        self.progbar.row = self.scene.row_progress + 1
        self.progbar.total = height
        self.progbar.refresh()
        self.notify(
            QCoreApplication.translate("Scene", "Image dimensions") +
            ": {} x {}".format(width, height), False)
        self.scene.refresh()

    def update_start_row(self, start_row):
        self.progbar.update(start_row)
        self.scene.row_progress = start_row

    def notify(self, text, log=True):
        """Update the notification field."""
        if log:
            logging.info("Notification: " + text)
        self.ui.label_notifications.setText(text)
