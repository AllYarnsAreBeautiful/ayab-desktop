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
import serial.tools.list_ports
from PIL import ImageOps
from PyQt5.QtCore import QTranslator, QCoreApplication, QLocale, QObjectCleanupHandler
from PyQt5.QtWidgets import QComboBox, QWidget
from .ayab_image import AyabImage
from .ayab_control import AyabControl, AyabControlKnitResult
from .ayab_mailman import SignalEmitter
from .ayab_options import Options, KnittingMode, Alignment, NeedleColor
from .ayab_options_gui import Ui_DockWidget


class AyabPlugin(object):
    def __init__(self):
        self.__control = AyabControl()
        self.__logger = logging.getLogger(type(self).__name__)

    def __del__(self):
        self.__control.close()

    def setupUi(self, parent):
        """Sets up UI elements from ayab_options.Ui_DockWidget in parent."""
        self.mailman = SignalEmitter(parent.mailbox)
        self.__feedback_handler = KnitFeedbackHandler(self.mailman)
        self.__set_translator(parent)

        # Dock widget
        self.ui = Ui_DockWidget()
        self.dock = parent.ui.knitting_options_dock
        self.ui.setupUi(self.dock)

        # Combo boxes
        KnittingMode.addItems(self.ui.knitting_mode_box)
        Alignment.addItems(self.ui.alignment_combo_box)
        NeedleColor.addItems(self.ui.start_needle_color)
        NeedleColor.addItems(self.ui.stop_needle_color)
        self.ui.start_needle_color.setCurrentIndex(0)
        self.ui.stop_needle_color.setCurrentIndex(1)

        # Status tab
        self.ui.tabWidget.setTabEnabled(1, False)
        self.ui.label_progress.setText("")
        self.ui.label_direction.setText("")

        # Disable "continuous reporting" checkbox and Status tab for now
        self.ui.checkBox_ContinuousReporting.setVisible(False)
        self.ui.tabWidget.removeTab(1)

        # activate UI elements
        self.__setup_behavior()

    def __set_translator(self, parent):
        app = QCoreApplication.instance()
        self.translator = QTranslator()
        language = parent.prefs.settings.value("language")
        lang_dir = parent.app_context.get_resource("ayab/translations")
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
            lambda: self.mailman.emit_update_needles(self.ui))
        self.ui.stop_needle_edit.valueChanged.connect(
            lambda: self.mailman.emit_update_needles(self.ui))
        self.ui.start_needle_color.currentIndexChanged.connect(
            lambda: self.mailman.emit_update_needles(self.ui))
        self.ui.stop_needle_color.currentIndexChanged.connect(
            lambda: self.mailman.emit_update_needles(self.ui))
        self.ui.alignment_combo_box.currentIndexChanged.connect(
            lambda: self.mailman.emit_update_alignment(self.ui))
        self.ui.start_row_edit.valueChanged.connect(self.update_start_row)

    def __populate_ports(self, combo_box=None, port_list=None):
        if not combo_box:
            combo_box = self.ui.serial_port_dropdown
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

    def configure(self, image):
        # get configuration options
        self.__conf = Options()
        self.__conf.read(self.ui)
        self.__logger.debug(self.__conf.as_dict())

        # start to knit with the bottom first
        image = image.rotate(180)

        # mirroring option
        if self.__conf.auto_mirror:
            image = ImageOps.mirror(image)

        # TODO: detect if previous conf had the same
        # image to avoid re-generating.

        self.__image = AyabImage(image, self.__conf.num_colors)
        if self.__conf.start_row > self.__image.img_height:
            self.mailman.emit_configure_fail(
                "Start row is larger than the image.")
            return

        # validate configuration options
        valid, msg = self.__conf.validate_configuration()
        if not valid:
            self.mailman.emit_configure_fail(msg)
            return

        # update image
        if self.__conf.start_needle and self.__conf.stop_needle:
            self.__image.set_knit_needles(self.__conf.start_needle,
                                          self.__conf.stop_needle)
        self.__image.alignment = self.__conf.alignment

        # update progress bar
        self.mailman.emit_progress(self.__conf.start_row + 1,
                                   self.__image.img_height, 0, "")

        # switch to status tab
        if self.__conf.continuous_reporting is True:
            self.ui.tabWidget.setCurrentIndex(1)

        # send signal to start knitting
        self.mailman.emit_configured()

    def knit(self):
        self.__canceled = False

        while True:
            # knit next row
            result = self.__control.knit(self.__image, self.__conf)
            self.__feedback_handler.handle(result)
            # do not need to make copy of progress object to emit to UI thread
            # because signal_update_knit_progress connection blocks this thread
            # progress = copy(self.__control.progress)
            status = self.__control.status
            row_mult = self.__control.get_row_multiplier()
            self.__knit_progress_handler(status, row_mult)
            if self.__canceled or result is AyabControlKnitResult.FINISHED:
                break

        self.__logger.info("Finished knitting.")
        self.__control.close()

        # small delay to finish printing to knit progress window
        # before "finish.wav" sound plays
        sleep(1)

        # send signal to finish knitting
        self.mailman.emit_done_knitting(not self.__canceled)

    def __knit_progress_handler(self, status, row_multiplier):
        self.mailman.emit_progress(status.current_row, status.total_rows,
                                   status.repeats, status.color_symbol)
        self.mailman.emit_knit_progress(status, row_multiplier)
        # update status tab
        self.ui.progress_hall_l.setValue(status.hall_l)
        self.ui.label_hall_l.setText(str(status.hall_l))
        self.ui.progress_hall_r.setValue(status.hall_r)
        self.ui.label_hall_r.setText(str(status.hall_r))
        self.ui.slider_position.setValue(status.carriage_position)
        self.ui.label_carriage.setText(status.carriage_type)

    def cancel(self):
        self.mailman.emit_notification("Knitting canceled.")
        self.__canceled = True

    def set_image_dimensions(self, width, height):
        """Called by Main UI on loading of an image to set Start/Stop needle
        to image width. Updates the maximum value of the Start Line UI element"""
        left_side = width // 2
        self.ui.start_needle_edit.setValue(left_side)
        self.ui.stop_needle_edit.setValue(width - left_side)
        self.ui.start_row_edit.setMaximum(height)

    def update_start_row(self):  # updates part of progress bar
        start_row_edit = int(self.ui.start_row_edit.value())
        self.mailman.emit_start_row(start_row_edit)

    # def cleanup_ui(self):
    #     """Cleans up UI elements inside knitting option dock."""
    #     dock = self.dock
    #     cleaner = QObjectCleanupHandler()
    #     cleaner.add(dock.widget())
    #     self.__qw = QWidget()
    #     dock.setWidget(self.__qw)
    #     self.__unset_translator()

    # def __unset_translator(self):
    #     app = QCoreApplication.instance()
    #     app.removeTranslator(self.translator)

    # def fail(self):
    #     # TODO add message info from event
    #     self.__logger.error("Error while knitting.")
    #     self.__control.close()


class KnitFeedbackHandler(object):
    """Polymorphic dispatch of notification signals on AyabControlKnitResult.

    @author Tom Price
    @data   July 2020
    """
    def __init__(self, signal_emitter):
        self.__mailman = signal_emitter

    def handle(self, result):
        method = "_" + result.name.lower()
        if hasattr(self, method):
            dispatch = getattr(self, method)
            dispatch()

    def _connecting_to_machine(self):
        self.__mailman.emit_notification("Connecting to machine...")

    def _wait_for_init(self):
        self.__mailman.emit_notification(
            "Please start machine. (Set the carriage to mode KC-I " +
            "or KC-II and move the carriage over the left turn mark).")

    def _error_wrong_api(self):
        self.__mailman.emit_popup(
            "Wrong Arduino firmware version. Please check " +
            "that you have flashed the latest version. (" +
            str(self.__control.API_VERSION) + ")")

    def _please_knit(self):
        self.__mailman.emit_notification("Please knit.")
        self.__mailman.emit_audio("start")

    def _device_not_ready(self):
        self.__mailman.emit_notification()
        self.__mailman.emit_blocking_popup("Device not ready, try again.")

    def _finished(self):
        self.__mailman.emit_notification(
            "Image transmission finished. Please knit until you " +
            "hear the double beep sound.")
