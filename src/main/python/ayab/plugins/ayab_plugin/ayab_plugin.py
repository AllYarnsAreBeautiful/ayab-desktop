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
from PyQt5.QtCore import Qt, QTranslator, QCoreApplication, QLocale, QObjectCleanupHandler
from PyQt5.QtWidgets import QComboBox, QWidget
from . import USB_ports
from .ayab_pattern import AyabPattern
from .ayab_control import AyabControl
from .ayab_observable import Observable
from .ayab_options import Options, Alignment, NeedleColor
from .ayab_knit_mode import KnitMode
from .ayab_knit_output import KnitOutput, KnitFeedbackHandler
from .ayab_options_gui import Ui_DockWidget


class AyabPlugin(Observable):
    def __init__(self, parent):
        super().__init__(parent.seer)
        self.__control = AyabControl()
        self.__logger = logging.getLogger(type(self).__name__)
        self.__feedback = KnitFeedbackHandler(parent)
        self.ui = Ui_DockWidget()
        self.dock = parent.ui.knitting_options_dock
        self.setup_ui()
        self.config = Options(parent.prefs)
        self.refresh()

    def __del__(self):
        self.__control.close()

    def setup_ui(self):
        """Sets up UI elements from ayab_options.Ui_DockWidget in parent."""
        # Dock widget
        self.ui.setupUi(self.dock)

        # Combo boxes
        KnitMode.add_items(self.ui.knitting_mode_box)
        Alignment.add_items(self.ui.alignment_combo_box)
        NeedleColor.add_items(self.ui.start_needle_color)
        NeedleColor.add_items(self.ui.stop_needle_color)
        self.ui.start_needle_color.setCurrentIndex(0)
        self.ui.stop_needle_color.setCurrentIndex(1)

        # Status tab
        self.ui.tab_widget.setTabEnabled(1, False)
        self.ui.label_progress.setText("")
        self.ui.label_direction.setText("")

        # Disable "continuous reporting" checkbox and Status tab for now
        self.ui.continuous_reporting_checkbox.setVisible(False)
        self.ui.tab_widget.removeTab(1)

        # activate UI elements
        self.__activate_ui()

    def __activate_ui(self):
        """Connects UI elements to signal slots."""
        self.__populate_ports()
        self.ui.refresh_ports_button.clicked.connect(self.__populate_ports)
        self.ui.start_row_edit.valueChanged.connect(
            lambda: self.emit_start_row_updater(
                self.config.read_start_row(self.ui)))
        self.ui.start_needle_edit.valueChanged.connect(self.__update_needles)
        self.ui.stop_needle_edit.valueChanged.connect(self.__update_needles)
        self.ui.start_needle_color.currentIndexChanged.connect(
            self.__update_needles)
        self.ui.stop_needle_color.currentIndexChanged.connect(
            self.__update_needles)
        self.ui.alignment_combo_box.currentIndexChanged.connect(
            lambda: self.emit_alignment_updater(
                self.config.read_alignment(self.ui)))

    def __populate_ports(self, combo_box=None, port_list=None):
        if not combo_box:
            combo_box = self.ui.serial_port_dropdown
        USB_ports.populate_ports(combo_box, port_list)
        # Add Simulation item to indicate operation without machine
        combo_box.addItem(
            QCoreApplication.translate("AyabPlugin", "Simulation"))

    def __update_needles(self):
        """Sends the needles_updater signal."""
        start_needle = NeedleColor.read_start_needle(self.ui)
        stop_needle = NeedleColor.read_stop_needle(self.ui)
        self.emit_needles_updater(start_needle, stop_needle)

    def reset(self):
        """Reset dock to default settings."""
        self.config.reset()
        self.refresh()

    def refresh(self):
        """Refresh dock to default configuration options."""
        self.ui.knitting_mode_box.setCurrentIndex(self.config.knitting_mode)
        # self.ui.color_edit
        # self.ui.start_row_edit
        if self.config.inf_repeat:
            self.ui.inf_repeat_checkbox.setCheckState(Qt.Checked)
        else:
            self.ui.inf_repeat_checkbox.setCheckState(Qt.Unchecked)
        # self.ui.start_needle_color
        # self.ui.start_needle_edit
        # self.ui.stop_needle_color
        # self.ui.stop_needle_edit
        self.ui.alignment_combo_box.setCurrentIndex(self.config.alignment)
        if self.config.auto_mirror:
            self.ui.auto_mirror_checkbox.setCheckState(Qt.Checked)
        else:
            self.ui.auto_mirror_checkbox.setCheckState(Qt.Unchecked)
        # self.ui.continuous_reporting_checkbox

    def get_config(self, image):
        """
        Read and check configuration options from options dock UI.
        """
        # get configuration options
        self.config.read(self.ui)
        self.__logger.debug(self.config.as_dict())

        # start to knit with the bottom first
        image = image.transpose(Image.ROTATE_180)

        # mirroring option
        if self.config.auto_mirror:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)

        # TODO: detect if previous conf had the same
        # image to avoid re-generating.

        self.__pattern = AyabPattern(image, self.config.num_colors)
        if self.config.start_row > self.__pattern.pat_height:
            self.emit_popup("Start row is larger than the image.")
            self.emit_bad_config_flag()

        # validate configuration options
        valid, msg = self.config.validate()
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
        if self.config.continuous_reporting:
            self.ui.tab_widget.setCurrentIndex(1)

        # send signal to start knitting
        self.emit_knitting_starter()

    def knit(self):
        self.__canceled = False

        while True:
            # knit next row
            result = self.__control.knit(self.__pattern, self.config)
            self.__feedback.handle(result)
            self.__knit_progress_handler()
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

    def __knit_progress_handler(self):
        # do not need to make copy of status object to emit to UI thread
        # because signal knit_progress_updater connection blocks this thread
        # until it has finished
        # status = copy(self.__control.status)
        status = self.__control.status
        row_multiplier = self.__control.row_multiplier()
        self.emit_progress_bar_updater(status.current_row, status.total_rows,
                                       status.repeats, status.color_symbol)
        self.emit_knit_progress_updater(status, row_multiplier)
        if self.config.continuous_reporting:
            self.__update_status_tab(status)

    def __update_status_tab(self, status):
        self.ui.progress_hall_l.setValue(status.hall_l)
        self.ui.label_hall_l.setText(str(status.hall_l))
        self.ui.progress_hall_r.setValue(status.hall_r)
        self.ui.label_hall_r.setText(str(status.hall_r))
        self.ui.slider_position.setValue(status.carriage_position)
        self.ui.label_carriage.setText(status.carriage_type)

    def cancel(self):
        self.emit_notification("Knitting canceled.")
        self.__canceled = True

    def set_image_dimensions(self, width, height):
        """Called by Main UI on loading of an image to set Start/Stop needle
        to image width. Updates the maximum value of the Start Row UI element"""
        left_side = width // 2
        self.ui.start_needle_edit.setValue(left_side)
        self.ui.stop_needle_edit.setValue(width - left_side)
        self.ui.start_row_edit.setMaximum(height)
