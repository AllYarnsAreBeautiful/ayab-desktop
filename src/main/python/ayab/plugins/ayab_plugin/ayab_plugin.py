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
# "import weakref
# from copy import copy
from time import sleep
import serial.tools.list_ports
from PIL import ImageOps
from PyQt5.QtCore import QTranslator, QCoreApplication, QLocale, QObjectCleanupHandler
from PyQt5.QtWidgets import QComboBox, QWidget
from .ayab_image import AyabImage
from .ayab_control import AyabControl, AyabControlKnitResult
from .ayab_options import Options, KnittingMode, Alignment, NeedleColor
from .ayab_options_gui import Ui_DockWidget


class AyabPlugin(object):
    def __init__(self):
        self.__ayab_control = AyabControl()
        self.__logger = logging.getLogger(type(self).__name__)

    def __del__(self):
        self.__ayab_control.close()

    def setupUi(self, parent):
        """Sets up UI elements from ayab_options.Ui_DockWidget in parent."""
        self.__parent = parent  # weakref.ref(parent)
        self.__set_translator()
        self.ui = Ui_DockWidget()
        self.dock = parent.ui.knitting_options_dock
        self.ui.setupUi(self.dock)
        self.ui.tabWidget.setTabEnabled(1, False)
        self.ui.label_progress.setText("")
        self.ui.label_direction.setText("")
        KnittingMode.addItems(self.ui.knitting_mode_box)
        Alignment.addItems(self.ui.alignment_combo_box)
        NeedleColor.addItems(self.ui.start_needle_color)
        NeedleColor.addItems(self.ui.stop_needle_color)
        self.ui.stop_needle_color.setCurrentIndex(1)
        self.__setup_behavior()

        # Disable "continuous reporting" checkbox and Status tab for now
        self.ui.checkBox_ContinuousReporting.setVisible(False)
        self.ui.tabWidget.removeTab(1)

    def __set_translator(self):
        app = QCoreApplication.instance()
        self.translator = QTranslator()
        language = self.__parent.prefs.settings.value("language")
        lang_dir = self.__parent.app_context.get_resource("ayab/translations")
        try:
            self.translator.load("ayab_trans." + language, lang_dir)
        except (TypeError, FileNotFoundError):
            self.__logger(
                "Unable load translation file for preferred language, " +
                "using default locale")
            try:
                self.translator.load(QLocale.system(), "ayab_trans", "",
                                     lang_dir)
            except Exception:
                self.__logger(
                    "Unable to load translation file for default locale, " +
                    "using American English")
                self.translator.load("ayab_trans.en_US", lang_dir)
        except Exception:
            self.__logger("Unable to load translation file")
            raise
        app.installTranslator(self.translator)

    def __setup_behavior(self):
        """Connects methods to UI elements."""
        self.__populate_ports()
        self.ui.refresh_ports_button.clicked.connect(self.__populate_ports)
        self.ui.start_needle_edit.valueChanged.connect(
            self.__emit_update_needles)
        self.ui.stop_needle_edit.valueChanged.connect(
            self.__emit_update_needles)
        self.ui.start_needle_color.currentIndexChanged.connect(
            self.__emit_update_needles)
        self.ui.stop_needle_color.currentIndexChanged.connect(
            self.__emit_update_needles)
        self.ui.alignment_combo_box.currentIndexChanged.connect(
            self.__emit_update_alignment)
        self.ui.start_row_edit.valueChanged.connect(self.update_start_row)

    def __populate_ports(self, combo_box=None, port_list=None):
        if not combo_box:
            combo_box = self.__parent.findChild(QComboBox,
                                                "serial_port_dropdown")
        if not port_list:
            port_list = self.__get_serial_ports()
        combo_box.clear()
        self.__populate(combo_box, port_list)
        # Add Simulation item to indicate operation without machine
        combo_box.addItem(
            QCoreApplication.translate("AyabPlugin", "Simulation"))

    def __populate(self, combo_box, port_list):
        for item in port_list:
            # TODO: should display the info of the device.
            combo_box.addItem(item[0])

    def __get_serial_ports(self):
        """
        Returns a list of all USB Serial Ports
        """
        return list(serial.tools.list_ports.grep("USB"))

    def configure(self):
        # get configuration options
        self.__conf = Options()
        self.__conf.read(self.ui)
        self.__logger.debug(self.__conf.as_dict())

        # start to knit with the bottom first
        image = self.__parent.scene.image.rotate(180)

        # mirroring option
        if self.__conf.auto_mirror:
            image = ImageOps.mirror(image)

        # TODO: detect if previous conf had the same
        # image to avoid re-generating.

        self.__image = AyabImage(image, self.__conf.num_colors)
        if self.__conf.start_row > self.__image.img_height:
            self.__emit_configure_fail("Start row is larger than the image.")
            return

        # validate configuration options
        valid, msg = self.__conf.validate_configuration()
        if not valid:
            self.__emit_configure_fail(msg)
            return

        # update image
        if self.__conf.start_needle and self.__conf.stop_needle:
            self.__image.set_knit_needles(self.__conf.start_needle,
                                          self.__conf.stop_needle)
        self.__image.alignment = self.__conf.alignment

        # update progress bar
        self.__emit_progress(self.__conf.start_row + 1,
                             self.__image.img_height, 0, "")

        # switch to status tab
        if self.__conf.continuous_reporting is True:
            self.ui.tabWidget.setCurrentIndex(1)

        # send signal to start knitting
        self.__parent.signal_configured.emit()

    def knit(self):
        self.__canceled = False

        while True:
            # knit next row
            result = self.__ayab_control.knit(self.__image, self.__conf)
            self.__knit_feedback_handler(result)
            # do not need to make copy of progress object to emit to UI thread
            # because signal_update_knit_progress connection blocks this thread
            # progress = copy(self.__ayab_control.progress)
            progress = self.__ayab_control.progress
            row_mult = self.__ayab_control.get_row_multiplier()
            self.__knit_progress_handler(progress, row_mult)
            if self.__canceled or result is AyabControlKnitResult.FINISHED:
                break

        self.__logger.info("Finished knitting.")
        self.__ayab_control.close()

        # small delay to finish printing to knit progress window
        # before "finish.wav" sound plays
        sleep(1)

        # send signal to finish knitting
        self.__parent.signal_done_knitting.emit(not self.__canceled)

    def __knit_feedback_handler(self, result):
        if result is AyabControlKnitResult.CONNECTING_TO_MACHINE:
            self.__emit_notification("Connecting to machine...")

        if result is AyabControlKnitResult.WAIT_FOR_INIT:
            self.__emit_notification(
                "Please start machine. (Set the carriage to mode KC-I " +
                "or KC-II and move the carriage over the left turn mark).")

        if result is AyabControlKnitResult.ERROR_WRONG_API:
            self.__emit_popup("Wrong Arduino firmware version. Please check " +
                              "that you have flashed the latest version. (" +
                              str(self.__ayab_control.API_VERSION) + ")")

        if result is AyabControlKnitResult.PLEASE_KNIT:
            self.__emit_notification("Please knit.")
            self.__emit_playsound("start")

        if result is AyabControlKnitResult.DEVICE_NOT_READY:
            self.__emit_notification()
            self.__emit_blocking_popup("Device not ready, try again.")

        if result is AyabControlKnitResult.FINISHED:
            self.__emit_notification(
                "Image transmission finished. Please knit until you " +
                "hear the double beep sound.")

    def __knit_progress_handler(self, progress, row_multiplier):
        self.__emit_progress(progress.current_row, progress.total_rows,
                             progress.repeats, progress.color_symbol)
        self.__emit_status(progress.hall_l, progress.hall_r,
                           progress.carriage_type, progress.carriage_position)
        self.__emit_knit_progress(progress, row_multiplier)

    def cancel(self):
        self.__emit_notification("Knitting canceled.")
        self.__canceled = True

    # never called
    # def fail(self):
    #     # TODO add message info from event
    #     self.__logger.error("Error while knitting.")
    #     self.__ayab_control.close()

    def set_image_dimensions(self, width, height):
        """Called by Main UI on loading of an image to set Start/Stop needle
        to image width. Updates the maximum value of the Start Line UI element"""
        left_side = width // 2
        self.ui.start_needle_edit.setValue(left_side)
        self.ui.stop_needle_edit.setValue(width - left_side)
        self.ui.start_row_edit.setMaximum(height)

    def cleanup_ui(self, parent):
        """Cleans up UI elements inside knitting option dock."""
        # dock = parent.knitting_options_dock
        dock = self.dock
        cleaner = QObjectCleanupHandler()
        cleaner.add(dock.widget())
        self.__qw = QWidget()
        dock.setWidget(self.__qw)
        self.__unset_translator()

    def __unset_translator(self):
        app = QCoreApplication.instance()
        app.removeTranslator(self.translator)

    def __emit_blocking_popup(self, message="", message_type="info"):
        """
        Sends the signal_display_blocking_popup QtSignal
        to main GUI thread, blocking it.
        """
        self.__parent.signal_display_blocking_popup.emit(
            QCoreApplication.translate("AyabPlugin", message), message_type)

    def __emit_popup(self, message="", message_type="info"):
        """
        Sends the signal_display_popup QtSignal
        to main GUI thread, not blocking it.
        """
        self.__parent.signal_display_popup.emit(
            QCoreApplication.translate("AyabPlugin", message), message_type)

    def __emit_configure_fail(self, message=""):
        self.__emit_popup(message)
        self.__parent.signal_configure_fail.emit()

    def __emit_notification(self, message=""):
        """Sends the signal_update_notification signal"""
        self.__parent.signal_update_notification.emit(
            QCoreApplication.translate("AyabPlugin", message))

    def __emit_knit_progress(self, progress, row_multiplier):
        """Sends the update_knit_progress QtSignal."""
        self.__parent.signal_update_knit_progress.emit(progress,
                                                       row_multiplier)

    def __emit_progress(self, row, total=0, repeats=0, color_symbol=""):
        """Sends the update_progress_bar QtSignal."""
        self.__parent.signal_update_progress_bar.emit(row, total, repeats,
                                                      color_symbol)

    def __emit_status(self, hall_l, hall_r, carriage_type, carriage_position):
        """Sends the update_status QtSignal"""
        self.__parent.signal_update_status.emit(hall_l, hall_r, carriage_type,
                                                carriage_position)

    def __emit_update_needles(self):
        """Sends the signal_update_needles QtSignal."""
        start_needle = NeedleColor.read_start_needle(self.ui)
        stop_needle = NeedleColor.read_stop_needle(self.ui)
        self.__parent.signal_update_needles.emit(start_needle, stop_needle)

    def __emit_update_alignment(self):
        """Sends the signal_update_alignment QtSignal"""
        alignment = Alignment(self.ui.alignment_combo_box.currentIndex())
        self.__parent.signal_update_alignment.emit(alignment)

    def __emit_playsound(self, event):
        # blocking connection means that thread waits until sound has finished playing
        self.__parent.signal_playsound.emit(event)

    def update_start_row(self):
        start_row_edit = self.ui.start_row_edit.value()
        total_rows = self.__parent.scene.image.size[1]
        self.__emit_progress(start_row_edit, total_rows, 0, "")
