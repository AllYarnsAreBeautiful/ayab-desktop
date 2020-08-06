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

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QSettings, QCoreApplication
from PyQt5.QtWidgets import QFrame, QListWidgetItem

import serial
import json
import logging
import os
import sys
import platform
import re
from subprocess import run, STDOUT, PIPE, check_output

from .firmware_flash_gui import Ui_Firmware
from . import utils


class FirmwareFlash(QFrame):
    # Arduino devices and their `avrdude` names
    device_dict = {
        "mega2560": "m2560",
        "uno": "atmega328p",
    }
    # Arduino programmers and their `avrdude` names
    programmer_dict = {
        "uno": "arduino",
        "mega2560": "wiring",
    }

    def __init__(self, parent):
        # TODO: add creator that does not depend from super to ease testing.
        super().__init__()
        self.__logger = logging.getLogger(type(self).__name__)
        self.__app_context = parent.app_context

        self.ui = Ui_Firmware()
        self.ui.setupUi(self)
        self.ui.flash_firmware.setEnabled(False)
        self.load_json()

        self.ui.port_combo_box.currentIndexChanged.connect(self.port_selected)
        self.ui.controller_list.itemClicked[QListWidgetItem].connect(
            self.controller_item_activated)
        self.ui.firmware_list.itemClicked[QListWidgetItem].connect(
            self.firmware_item_activated)
        self.ui.flash_firmware.clicked.connect(self.execute_flash_command)

    def open(self):
        utils.populate_ports(self.ui.port_combo_box)
        self.port_selected()
        self.show()

    def load_json(self):
        self.json_object = self.parse_json("")
        self.add_items_from_json_object()

    def parse_json(self, json_string):
        path = self.__app_context.get_resource("ayab/firmware/firmware.json")
        with open(path) as data_file:
            data = json.load(data_file)
        return data

    def add_items_from_json_object(self):
        self.load_controllers()
        self.clean_firmware_list()

    def load_controllers(self):
        self.clean_controller_list()
        repo = self.json_object
        for controller in repo.get("controller", []):
            self.add_controller_to_list(controller)

    def controller_item_activated(self, control_qitem):
        """
        Signal on controller_list activated.
        Triggers loading of firmwares.
        """
        self.load_firmware(control_qitem.text())
        self.ui.flash_firmware.setEnabled(False)

    def load_firmware(self, controller_qstring):
        self.clean_firmware_list()
        controller_key = str(controller_qstring)
        repo = self.json_object
        for firmware in repo['controller'][controller_key]:
            self.add_firmware_dict_to_list(firmware)

    def firmware_item_activated(self, firmware_qitem):
        """Signal on firmware_list activated."""
        self.ui.flash_firmware.setEnabled(self.valid_port())

    def valid_port(self):
        return self.port != ""

    def port_selected(self):
        self.port = self.ui.port_combo_box.currentText()

    def clean_controller_list(self):
        self.__clean_QListWidget(self.ui.controller_list)

    def clean_firmware_list(self):
        self.__clean_QListWidget(self.ui.firmware_list)

    def __clean_QListWidget(self, qlistw):
        qlistw.clear()

    def add_controller_to_list(self, controller):
        self.ui.controller_list.addItem(controller)

    def add_firmware_dict_to_list(self, firmware):
        ## Could add more info to display, such as date.
        version = firmware.get("version", "unspecified version")
        self.ui.firmware_list.addItem(version)

    def execute_flash_command(self):
        self.ui.flash_firmware.setEnabled(False)
        self.__logger.debug("port " + str(self.port))
        os_name = platform.system()
        base_dir = os.path.dirname(__file__)
        controller_name = str(self.ui.controller_list.currentItem().text())
        firmware_key = str(self.ui.firmware_list.currentItem().text())
        firmware_name = "firmware.hex"
        for firmware in self.json_object['controller'][controller_name]:
            if firmware.get("version") == firmware_key:
                firmware_name = firmware.get("file")

        command = self.generate_command(base_dir, os_name, controller_name,
                                        firmware_name)
        if command is None:
            return False
        # else
        tr_ = QCoreApplication.translate
        try:
            p = check_output(command, stderr=STDOUT, timeout=10, shell=True)
        except Exception as e:
            self.__logger.info("Error flashing firmware: " + str(e))
            utils.display_blocking_popup(
                tr_("Firmware", "Error flashing firmware."), "error")
            return False
        else:
            self.__logger.info("Flashing done!")
            utils.display_blocking_popup(
                tr_("Firmware", "Flashing done!"))
            return True

    def generate_command(self, base_dir, os_name, controller_name,
                         firmware_name):
        if os_name == "Windows":
            exe_route = self.__app_context.get_resource(
                "ayab/firmware/avrdude.exe")
            exe_route = "\"" + exe_route + "\""
        elif os_name == "Linux":
            # We assume avrdude is available in path
            try:
                # run subprocess
                result = run(["which", "avrdude"], stdout=PIPE, stderr=PIPE)
                print(result)
            except:
                self.__logger.error("`avrdude` not found in path")
                utils.display_blocking_popup(
                    QCoreApplication.translate(
                        "FirmwareFlash",
                        "Error flashing firmware: `avrdude` not found."),
                    "error")
                return None
            exe_route = re.sub(r"\n$", r"", result.stdout.decode("ascii"))
        elif os_name == "Darwin":  # macOS
            exe_route = self.__app_context.get_resource(
                "ayab/firmware/avrdude_mac")

        binary_file = os.path.join(
            self.__app_context.get_resource("ayab/firmware"), controller_name,
            firmware_name)
        device = self.device_dict.get(controller_name)
        programmer = self.programmer_dict.get(controller_name, "wiring")

        # avrdude command.
        # http://www.ladyada.net/learn/avr/avrdude.html
        # http://sharats.me/the-ever-useful-and-neat-subprocess-module.html
        exec_command = """{0} -p {1} -c {2} -P {3} -b115200 -D -Uflash:w:"{4}":i """.format(exe_route, device, programmer, self.port, binary_file)

        if os_name == "Windows" or os_name == "Darwin":
            exec_command += " -C \"" + self.__app_context.get_resource(
                "ayab/firmware/avrdude.conf") + "\""

        self.__logger.debug(exec_command)
        return exec_command
