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

import logging
from time import sleep
from PIL import Image

from PyQt5.QtCore import QTranslator, QCoreApplication, QLocale, QObjectCleanupHandler, pyqtSignal
from PyQt5.QtWidgets import QComboBox, QDockWidget, QWidget

from .. import utils
from ..observable import Observable
from .control import Control
from .state import Operation, State
from .pattern import Pattern
from .options import OptionsTab, Alignment, NeedleColor
from .status import Status, StatusTab
from .mode import Mode
from .output import Output, FeedbackHandler
from .dock_gui import Ui_Dock


class Engine(Observable, QDockWidget):
    """
    Top-level class for the slave thread that communicates with the shield.

    Implemented as a subclass of `QDockWidget` and `Observable`.
    """
    port_opener = pyqtSignal()

    def __init__(self, parent):
        # set up UI
        super().__init__(parent.seer)
        self.ui = Ui_Dock()
        self.ui.setupUi(self)
        self.config = OptionsTab(parent)
        self.config.portname = self.__read_portname()
        self.config.refresh()
        self.status = StatusTab()
        self.setup_ui()
        parent.ui.dock_container_layout.addWidget(self)

        self.pattern = None
        self.control = Control(parent, self)
        self.__feedback = FeedbackHandler(parent)
        self.__logger = logging.getLogger(type(self).__name__)
        # self.fs =

    def __del__(self):
        self.control.stop()

    def setup_ui(self):
        # insert tabs
        tr_ = QCoreApplication.translate
        self.ui.tab_widget.insertTab(0, self.config, tr_("Dock", "Settings"))
        self.ui.tab_widget.insertTab(1, self.status, tr_("Dock", "Status"))

        # disable status tab at first
        self.__disable_status_tab()

        # remove Status tab for now
        self.__close_status_tab()

        # activate UI elements
        self.__activate_ui()

    def __disable_status_tab(self):
        self.ui.tab_widget.setTabEnabled(1, False)
        self.status.ui.label_progress.setText("")
        self.status.ui.label_direction.setText("")
        self.status.active = False

    def __close_status_tab(self):
        self.ui.tab_widget.removeTab(1)
        self.status.active = False

    def __activate_ui(self):
        """Connects UI elements to signal slots."""
        self.__populate_ports()
        self.ui.refresh_ports_button.clicked.connect(self.__populate_ports)

    def __populate_ports(self, port_list=None):
        combo_box = self.ui.serial_port_dropdown
        utils.populate_ports(combo_box, port_list)
        # Add Simulation item to indicate operation without machine
        combo_box.addItem(
            QCoreApplication.translate("KnitEngine", "Simulation"))

    def __read_portname(self):
        return self.ui.serial_port_dropdown.currentText()

    def knit_config(self, image):
        """
        Read and check configuration options from options dock UI.
        """
        # get configuration options
        self.config.read(self.__read_portname())
        self.__logger.debug(self.config.as_dict())

        # start to knit with the bottom first
        image = image.transpose(Image.ROTATE_180)

        # mirroring option
        if self.config.auto_mirror:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)

        # TODO: detect if previous conf had the same
        # image to avoid re-generating.
        self.pattern = Pattern(image, self.config.machine,
                               self.config.num_colors)

        # validate configuration options
        valid, msg = self.validate()
        if not valid:
            self.emit_popup(msg)
            self.emit_bad_config_flag()

        # update pattern
        self.pattern.set_knit_needles(self.config.start_needle,
                                          self.config.stop_needle,
                                          self.config.machine)
        self.pattern.alignment = self.config.alignment

        # update progress bar
        self.emit_progress_bar_updater(self.config.start_row + 1,
                                       self.pattern.pat_height, 0, "")

        # switch to status tab
        # if self.config.continuous_reporting:
        #     self.__status_tab.activate()

        # send signal to start knitting
        self.emit_knitting_starter()

    def validate(self):
        if self.config.start_row > self.pattern.pat_height:
            return False, "Start row is larger than the image."
        # else
        return self.config.validate()

    def run(self, operation):
        self.__canceled = False

        # setup knitting controller
        self.config.portname = self.__read_portname()
        self.control.start(self.pattern, self.config, operation)

        while True:
            # continue operating
            # typically each step involves some communication with the device
            output = self.control.operate(operation)
            self.__feedback.handle(output)
            if operation == Operation.KNIT:
                self.__handle_status()
            if self.__canceled or self.control.state == State.FINISHED:
                break

        self.control.stop()

        if operation == Operation.KNIT:
            if self.__canceled:
                self.emit_notification("Knitting canceled.")
                self.__logger.info("Knitting canceled.")
            else:
                self.__logger.info("Finished knitting.")
            # small delay to finish printing to knit progress window
            # before "finish.wav" sound plays
            sleep(1)
        else:
            # TODO: provide translations for these messages
            if self.__canceled:
                self.emit_notification("Testing canceled.")
                self.__logger.info("Testing canceled.")
            else:
                self.__logger.info("Finished testing.")

        # send signal to finish operation
        # "finish.wav" sound only plays if knitting was not canceled
        self.emit_operation_finisher(operation, not self.__canceled)

    def __handle_status(self):
        if self.status.active:
            self.status.refresh()
        # If we do not make a copy of status object to emit to the UI thread
        # then the signal knit_progress_updater must use a blocking connection
        # that holds up this thread until the knit progress window has finished
        # updating, Otherwise if the knit progress window lags the status
        # will change before the information is written to the UI.
        data = Status()
        data.copy(self.status)
        self.emit_knit_progress_updater(data, self.control.passes_per_row, self.control.midline, self.config.auto_mirror)
        self.emit_progress_bar_updater(data.current_row, self.pattern.pat_height,
                                       data.repeats, data.color_symbol)

    def cancel(self):
        self.__canceled = True
