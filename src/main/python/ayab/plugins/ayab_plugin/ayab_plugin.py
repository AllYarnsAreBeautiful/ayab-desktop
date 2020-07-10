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
# from copy import copy
from time import sleep
from PIL import Image
from PyQt5.QtCore import QTranslator, QCoreApplication, QLocale, QObjectCleanupHandler
from PyQt5.QtWidgets import QComboBox, QDockWidget, QWidget
from . import USB_ports
from .ayab_pattern import AyabPattern
from .ayab_control import AyabControl
from .ayab_observable import Observable
from .ayab_options import OptionsTab, Alignment, NeedleColor
from .ayab_status import Status, StatusTab
from .ayab_knit_mode import KnitMode
from .ayab_knit_output import KnitOutput, KnitFeedbackHandler
from .ayab_dock_gui import Ui_DockWidget


class AyabPlugin(Observable, QDockWidget):
    """
    Top-level class for the slave thread that communicates with the shield.

    Implemented as a subclass of `QDockWidget` and `Observable`.
    """
    def __init__(self, parent):
        super().__init__(parent.seer)
        self.ui = Ui_DockWidget()
        self.ui.setupUi(self)
        self.config = OptionsTab(parent.prefs)
        self.config.refresh()
        self.status = StatusTab()
        self.setup_ui()
        parent.ui.dock_container_layout.addWidget(self)
        self.__control = AyabControl(self)
        self.__logger = logging.getLogger(type(self).__name__)
        self.__feedback = KnitFeedbackHandler(parent)

    def __del__(self):
        self.__control.close()

    def setup_ui(self):
        # insert tabs
        tr_ = QCoreApplication.translate
        self.ui.tab_widget.insertTab(0, self.config,
                                     tr_("DockWidget", "Settings"))
        self.ui.tab_widget.insertTab(1, self.status,
                                     tr_("DockWidget", "Status"))

        # disable status tab at first
        self.__disable_status_tab()

        # remove Status tab for now
        self.__close_status_tab()

        # activate UI elements
        self.__activate_ui()


#  def __activate_status_tab(self):
#      self.ui.tab_widget.setTabEnabled(1, True)
#      self.ui.tab_widget.setCurrentIndex(1)
#      self.status.active = True

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
        self.config.ui.start_row_edit.valueChanged.connect(
            lambda: self.emit_start_row_updater(self.config.read_start_row()))
        self.config.ui.start_needle_edit.valueChanged.connect(
            self.__update_needles)
        self.config.ui.stop_needle_edit.valueChanged.connect(
            self.__update_needles)
        self.config.ui.start_needle_color.currentIndexChanged.connect(
            self.__update_needles)
        self.config.ui.stop_needle_color.currentIndexChanged.connect(
            self.__update_needles)
        self.config.ui.alignment_combo_box.currentIndexChanged.connect(
            lambda: self.emit_alignment_updater(self.config.read_alignment()))

    def __populate_ports(self, port_list=None):
        combo_box = self.ui.serial_port_dropdown
        USB_ports.populate_ports(combo_box, port_list)
        # Add Simulation item to indicate operation without machine
        combo_box.addItem(
            QCoreApplication.translate("AyabPlugin", "Simulation"))

    def __update_needles(self):
        """Sends the needles_updater signal."""
        start_needle = NeedleColor.read_start_needle(self.config.ui)
        stop_needle = NeedleColor.read_stop_needle(self.config.ui)
        self.emit_needles_updater(start_needle, stop_needle)

    # def refresh(self, image):
    #     self.portname = ""
    #     self.config.refresh()

    def knit_config(self, image):
        """
        Read and check configuration options from options dock UI.
        """
        # get configuration options
        self.config.read(self.ui.serial_port_dropdown.currentText())
        self.__logger.debug(self.config.as_dict())

        # start to knit with the bottom first
        image = image.transpose(Image.ROTATE_180)

        # mirroring option
        if self.config.auto_mirror:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)

        # TODO: detect if previous conf had the same
        # image to avoid re-generating.
        self.__pattern = AyabPattern(image, self.config.num_colors)

        # validate configuration options
        valid, msg = self.validate()
        if not valid:
            self.emit_popup(msg)
            self.emit_bad_config_flag()

        # update pattern
        if self.config.start_needle and self.config.stop_needle:
            self.__pattern.set_knit_needles(self.config.start_needle,
                                            self.config.stop_needle)
        self.__pattern.alignment = self.config.alignment

        # update progress bar
        self.emit_progress_bar_updater(self.config.start_row + 1,
                                       self.__pattern.pat_height, 0, "")

        # switch to status tab
        # if self.config.continuous_reporting:
        #     self.__status_tab.activate()

        # send signal to start knitting
        self.emit_knitting_starter()

    def validate(self):
        if self.config.start_row > self.__pattern.pat_height:
            return False, "Start row is larger than the image."
        # else
        return self.config.validate()

    def knit(self):
        self.__canceled = False

        while True:
            # continue knitting
            # typically each step involves some communication with the shield

            # FIXME pattern and config are only used by AyabControl.knit()
            # in the KnitState.SETUP step and do not need to be sent otherwise.
            result = self.__control.knit(self.__pattern, self.config)
            self.__feedback.handle(result)
            self.__status_handler()
            if self.__canceled or result is KnitOutput.FINISHED:
                break

        self.__logger.info("Finished knitting.")
        self.__control.close()

        # small delay to finish printing to knit progress window
        # before "finish.wav" sound plays
        sleep(1)

        # send signal to finish knitting
        # "finish.wav" sound only plays if knitting was not canceled
        self.emit_knitting_finisher(not self.__canceled)

    def __status_handler(self):
        if self.status.active:
            self.status.refresh()
        # if we do not make a copy of status object to emit to the UI thread
        # then the signal knit_progress_updater must use a blocking connection
        # that holds up this thread until the knit progress window has finished
        # updating, otherwise if the knit progress window lags the status
        # will change before the information is written to the UI.
        data = Status()
        data.copy(self.__control.status)
        row_multiplier = self.__control.knit_mode.row_multiplier(
            self.__control.num_colors)
        self.emit_knit_progress_updater(data, row_multiplier)
        self.emit_progress_bar_updater(data.current_row, data.total_rows,
                                       data.repeats, data.color_symbol)

    def cancel(self):
        self.emit_notification("Knitting canceled.")
        self.__canceled = True
