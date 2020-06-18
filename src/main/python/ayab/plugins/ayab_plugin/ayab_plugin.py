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

import math
import logging
import os

from PIL import ImageOps

from PyQt5 import QtGui, QtWidgets, QtCore

from .ayab_options import Ui_DockWidget
import serial.tools.list_ports

from . import ayab_image
from ayab.plugins.knitting_plugin import KnittingPlugin
from .ayab_control import AYABControl, AYABControlKnitResult, KnittingMode


class AyabPlugin(KnittingPlugin):
    def __init__(self):
        super(AyabPlugin, self).__init__({})

        self.__ayab_control = AYABControl()

        self.__logger = logging.getLogger(type(self).__name__)

    def __del__(self):
        self.__ayab_control.close()

    def onknit(self, e):
        self.__logger.debug("called onknit on AyabPlugin")

        if self.conf["continuousReporting"] is True:
            self.options_ui.tabWidget.setCurrentIndex(1)

        self._knitImage = True
        while self._knitImage:
            result = self.__ayab_control.knit(self.__image, self.conf)
            self._knit_progress_handler(self.__ayab_control.get_progress())
            self._knit_feedback_handler(result)
            if result is AYABControlKnitResult.FINISHED:
                break
        self.finish()

    def _knit_feedback_handler(self, result):
        if result is AYABControlKnitResult.CONNECTING_TO_MACHINE:
            self.__updateNotification("Connecting to machine...")

        if result is AYABControlKnitResult.WAIT_FOR_INIT:
            self.__updateNotification(
                        "Please init machine. (Set the carriage to mode KC-I "
                        "or KC-II and move the carriage over the left "
                        "turn mark)."
                    )
        if result is AYABControlKnitResult.ERROR_WRONG_API:
            self.__notify_user(
                "Wrong Arduino Firmware Version. " +
                "Please check if you have flashed " +
                "the latest version. (" + str(self._API_VERSION) + ")")

        if result is AYABControlKnitResult.PLEASE_KNIT:
            self.__updateNotification("Please Knit")
            self.__emit_playsound("start")

        if result is AYABControlKnitResult.DEVICE_NOT_READY:
            self.__updateNotification()
            self.__wait_for_user_action(
                "Device not ready, configure and try again.")

        if result is AYABControlKnitResult.FINISHED:
            self.__updateNotification("Image transmission finished. "
                                      "Please knit until you hear the "
                                      "double beep sound.")
            self.__emit_playsound("finished")

    def _knit_progress_handler(self, progress):
        self.__emit_progress(progress["current_row"], progress["total_rows"],
                             progress["repeats"])
        self.__emit_color(progress["color"])
        self.__emit_status(progress["hall_l"], progress["hall_r"],
                           progress["carriage_type"],
                           progress["carriage_position"])

    def onconfigure(self, e):
        self.__logger.debug("called onconfigure on AYAB Knitting Plugin")
        # print ', '.join("%s: %s" % item for item in vars(e).items())
        parent_ui = self.__parent_ui

        # Start to knit with the bottom first
        pil_image = parent_ui.pil_image.rotate(180)
        conf = self.get_configuration_from_ui(parent_ui)

        # Mirroring option
        if conf.get("auto_mirror"):
            pil_image = ImageOps.mirror(pil_image)

        # TODO: detect if previous conf had the same
        # image to avoid re-generating.

        try:
            self.__image = ayab_image.ayabImage(pil_image,
                                                self.conf["num_colors"])
        except:
            self.__notify_user("You need to set an image.", "error")
            return

        if self.validate_configuration(conf):
            self.__emit_widget_knitcontrol_enabled(True)
            self.__emit_button_knit_enabled(True)

            if conf.get("start_needle") and conf.get("stop_needle"):
                self.__image.setKnitNeedles(conf.get("start_needle"),
                                            conf.get("stop_needle"))
            if conf.get("alignment"):
                self.__image.setImagePosition(conf.get("alignment"))

            self.__image.setStartLine(conf.get("start_line"))
            self.__emit_progress(
                conf.get("start_line") + 1, self.__image.imgHeight())
            self.__emit_color("")
        else:
            self.__emit_widget_knitcontrol_enabled(False)
            self.__emit_button_knit_enabled(False)

        return

    def validate_configuration(self, conf):
        if conf.get("start_needle") and conf.get("stop_needle"):
            if conf.get("start_needle") > conf.get("stop_needle"):
                self.__notify_user("Invalid needle start and end.", "warning")
                return False
        if conf.get("start_line") > self.__image.imgHeight():
            self.__notify_user("Start Line is larger than the image.")
            return False

        if conf.get("portname") == '':
            self.__notify_user("Please choose a valid port.")
            return False

        if conf.get("knitting_mode") == KnittingMode.SINGLEBED.value \
                and conf.get("num_colors") >= 3:
            self.__notify_user(
                "Singlebed knitting currently supports only 2 colors",
                "warning")
            return False

        if conf.get("knitting_mode") == KnittingMode.CIRCULAR_RIBBER.value \
                and conf.get("num_colors") >= 3:
            self.__notify_user("Circular knitting supports only 2 colors",
                               "warning")
            return False

        return True

    def onfinish(self, e):
        self.__logger.info("Finished Knitting.")
        self.__ayab_control.close()
        self.__parent_ui.resetUI()

    def cancel(self):
        self.__updateNotification("Knitting cancelled")
        self._knitImage = False

    def onerror(self, e):
        # TODO add message info from event
        self.__logger.error("Error while Knitting.")
        self.__ayab_control.close()

    def __wait_for_user_action(self, message="", message_type="info"):
        """
        Sends the display_blocking_pop_up_signal QtSignal
        to main GUI thread, blocking it.
        """
        self.__parent_ui.signalDisplayBlockingPopUp.emit(message, message_type)

    def __notify_user(self, message="", message_type="info"):
        """
        Sends the display_pop_up_signal QtSignal
        to main GUI thread, not blocking it.
        """
        self.__parent_ui.signalDisplayPopUp.emit(message, message_type)

    def __updateNotification(self, message=""):
        """Sends the signalUpdateNotification signal"""
        self.__parent_ui.signalUpdateNotification.emit(message)

    def __emit_progress(self, row, total=0, repeats=0):
        """Sends the updateProgress QtSignal."""
        self.__parent_ui.signalUpdateProgress.emit(int(row), int(total),
                                                   int(repeats))

    def __emit_color(self, color):
        """Sends the updateProgress QtSignal."""
        self.__parent_ui.signalUpdateColor.emit(color)

    def __emit_status(self, hall_l, hall_r, carriage_type, carriage_position):
        """Sends the updateStatus QtSignal"""
        self.__parent_ui.signalUpdateStatus.emit(hall_l, hall_r, carriage_type,
                                                 carriage_position)

    def __emit_button_knit_enabled(self, enabled):
        self.__parent_ui.signalUpdateButtonKnitEnabled.emit(enabled)

    def __emit_widget_knitcontrol_enabled(self, enabled):
        self.__parent_ui.signalUpdateWidgetKnitcontrolEnabled.emit(enabled)

    def __emit_needles(self):
        """Sends the updateNeedles QtSignal."""

        start_needle_text = self.options_ui.start_needle_edit.value()
        start_needle_color = self.options_ui.start_needle_color.currentText()
        start_needle = self.readNeedleSettings(start_needle_color,
                                               start_needle_text)

        stop_needle_text = self.options_ui.stop_needle_edit.value()
        stop_needle_color = self.options_ui.stop_needle_color.currentText()
        stop_needle = self.readNeedleSettings(stop_needle_color,
                                              stop_needle_text)

        self.__parent_ui.signalUpdateNeedles.emit(start_needle, stop_needle)

    def __emit_alignment(self):
        """Sends the updateAlignment QtSignal"""
        alignment_text = self.options_ui.alignment_combo_box.currentText()
        self.__parent_ui.signalUpdateAlignment.emit(alignment_text)

    def __emit_playsound(self, event):
        self.__parent_ui.signalPlaysound.emit(event)

    def slotSetImageDimensions(self, width, height):
        """Called by Main UI on loading of an image to set Start/Stop needle
    to image width. Updates the maximum value of the Start Line UI element"""
        left_side = math.trunc(width / 2)
        self.options_ui.start_needle_edit.setValue(left_side)
        self.options_ui.stop_needle_edit.setValue(width - left_side)
        self.options_ui.start_row_edit.setMaximum(height)

    def __onStartLineChanged(self):
        """ """
        start_row_edit = self.options_ui.start_row_edit.value()
        self.__emit_progress(start_row_edit)

    def setup_ui(self, parent_ui):
        """Sets up UI elements from ayab_options.Ui_DockWidget in parent_ui."""
        self.set_translator()
        self.__parent_ui = parent_ui
        self.options_ui = Ui_DockWidget()
        self.dock = parent_ui.ui.knitting_options_dock
        self.options_ui.setupUi(self.dock)
        self.options_ui.tabWidget.setTabEnabled(1, False)
        self.options_ui.label_progress.setText("")
        self.options_ui.label_direction.setText("")
        self.setup_behaviour_ui()

        # Disable "continuous reporting" checkbox and Status tab for now
        parent_ui.findChild(QtWidgets.QCheckBox,
                            "checkBox_ContinuousReporting").setVisible(False)
        parent_ui.findChild(QtWidgets.QTabWidget, "tabWidget").removeTab(1)

    def set_translator(self):
        dirname = os.path.dirname(__file__)
        self.translator = QtCore.QTranslator()
        self.translator.load(QtCore.QLocale.system(), "ayab_options", ".",
                             dirname, ".qm")
        app = QtCore.QCoreApplication.instance()
        app.installTranslator(self.translator)

    def unset_translator(self):
        app = QtCore.QCoreApplication.instance()
        app.removeTranslator(self.translator)

    def populate_ports(self, combo_box=None, port_list=None):
        if not combo_box:
            combo_box = self.__parent_ui.findChild(QtWidgets.QComboBox,
                                                   "serial_port_dropdown")
        if not port_list:
            port_list = self.getSerialPorts()

        combo_box.clear()

        def populate(combo_box, port_list):
            for item in port_list:
                # TODO: should display the info of the device.
                combo_box.addItem(item[0])

        populate(combo_box, port_list)

        # Add Simulation item to indicate operation without machine
        combo_box.addItem("Simulation")

    def setup_behaviour_ui(self):
        """Connects methods to UI elements."""
        conf_button = self.options_ui.configure_button
        conf_button.clicked.connect(self.conf_button_function)

        self.populate_ports()
        refresh_ports = self.options_ui.refresh_ports_button
        refresh_ports.clicked.connect(self.populate_ports)

        start_needle_edit = self.options_ui.start_needle_edit
        start_needle_edit.valueChanged.connect(self.__emit_needles)
        stop_needle_edit = self.options_ui.stop_needle_edit
        stop_needle_edit.valueChanged.connect(self.__emit_needles)

        start_needle_color = self.options_ui.start_needle_color
        start_needle_color.currentIndexChanged.connect(self.__emit_needles)
        stop_needle_color = self.options_ui.stop_needle_color
        stop_needle_color.currentIndexChanged.connect(self.__emit_needles)

        alignment_combo_box = self.options_ui.alignment_combo_box
        alignment_combo_box.currentIndexChanged.connect(self.__emit_alignment)

        start_row_edit = self.options_ui.start_row_edit
        start_row_edit.valueChanged.connect(self.__onStartLineChanged)

    def conf_button_function(self):
        self.configure()

    def cleanup_ui(self, parent_ui):
        """Cleans up UI elements inside knitting option dock."""
        # dock = parent_ui.knitting_options_dock
        dock = self.dock
        cleaner = QtCore.QObjectCleanupHandler()
        cleaner.add(dock.widget())
        self.__qw = QtGui.QWidget()
        dock.setWidget(self.__qw)
        self.unset_translator()

    def readNeedleSettings(self, color, needle):
        '''Reads the Needle Settings UI Elements and normalizes'''
        if (color == "orange"):
            return 100 - int(needle)
        elif (color == "green"):
            return 99 + int(needle)

    def get_configuration_from_ui(self, ui):
        """Creates a configuration dict from the ui elements.

    Returns:
      dict: A dict with configuration.

    """

        self.conf = {}
        continuousReporting = ui.findChild(
            QtWidgets.QCheckBox, "checkBox_ContinuousReporting").isChecked()
        if continuousReporting == 1:
            self.conf["continuousReporting"] = True
        else:
            self.conf["continuousReporting"] = False

        color_line_text = ui.findChild(QtWidgets.QSpinBox,
                                       "color_edit").value()
        self.conf["num_colors"] = int(color_line_text)

        # Internally, we start counting from zero
        # (for easier handling of arrays)
        start_line_text = ui.findChild(QtWidgets.QSpinBox,
                                       "start_row_edit").value()
        self.conf["start_line"] = int(start_line_text) - 1

        start_needle_color = ui.findChild(QtWidgets.QComboBox,
                                          "start_needle_color").currentText()
        start_needle_text = ui.findChild(QtWidgets.QSpinBox,
                                         "start_needle_edit").value()

        self.conf["start_needle"] = self.readNeedleSettings(
            start_needle_color, start_needle_text)

        stop_needle_color = ui.findChild(QtWidgets.QComboBox,
                                         "stop_needle_color").currentText()
        stop_needle_text = ui.findChild(QtWidgets.QSpinBox,
                                        "stop_needle_edit").value()

        self.conf["stop_needle"] = self.readNeedleSettings(
            stop_needle_color, stop_needle_text)

        alignment_text = ui.findChild(QtWidgets.QComboBox,
                                      "alignment_combo_box").currentText()
        self.conf["alignment"] = alignment_text

        self.conf["inf_repeat"] = \
            int(ui.findChild(QtWidgets.QCheckBox,
                             "infRepeat_checkbox").isChecked())

        self.conf["auto_mirror"] = \
            int(ui.findChild(QtWidgets.QCheckBox,
                             "autoMirror_checkbox").isChecked())

        knitting_mode_index = ui.findChild(QtWidgets.QComboBox,
                                           "knitting_mode_box").currentIndex()
        self.conf["knitting_mode"] = knitting_mode_index

        serial_port_text = ui.findChild(QtWidgets.QComboBox,
                                        "serial_port_dropdown").currentText()
        self.conf["portname"] = str(serial_port_text)

        # getting file location from textbox
        filename_text = ui.findChild(QtWidgets.QLineEdit,
                                     "filename_lineedit").text()
        self.conf["filename"] = str(filename_text)

        self.__logger.debug(self.conf)
        # Add more config options.
        return self.conf

    def getSerialPorts(self):
        """
        Returns a list of all USB Serial Ports
        """
        return list(serial.tools.list_ports.grep("USB"))
