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
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QFrame, QListWidgetItem

import serial
import json
import logging
import os
import sys
import platform
import subprocess
from subprocess import Popen, PIPE, STDOUT

from .firmware_flash_ui import Ui_FirmwareFlashFrame
from .plugins.ayab_plugin import USB_ports
from . import notify


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

        self.ui = Ui_FirmwareFlashFrame()
        self.ui.setupUi(self)
        self.ui.flash_firmware.setEnabled(False)

        USB_ports.populate_ports(self.ui.port_combo_box)
        self.load_json()

        # self.ui.hardware_list.itemClicked[QListWidgetItem].connect(
        #     self.hardware_item_activated)
        self.ui.controller_list.itemClicked[QListWidgetItem].connect(
            self.controller_item_activated)
        self.ui.firmware_list.itemClicked[QListWidgetItem].connect(
            self.firmware_item_activated)
        self.ui.flash_firmware.clicked.connect(self.execute_flash_command)

        # select hardware from settings
        # self.hardware_item_activated(
        #     self.ui.hardware_list.item(
        #         parent.prefs.settings.value("machine")))
        self.ui.hardware_list.setCurrentItem(self.ui.hardware_list.item(0))
        self.hardware_item_activated(self.ui.hardware_list.item(0))

    def load_json(self):
        self.json_object = self.parse_json("")
        self.add_items_from_json_object(self.json_object)

    def parse_json(self, json_string):
        path = self.__app_context.get_resource("ayab/firmware/firmware.json")

        with open(path) as data_file:
            data = json.load(data_file)
        return data

    def add_items_from_json_object(self, json_object):
        repo = json_object
        for hardware_device in repo:
            description = repo.get(hardware_device, [])['description']
            self.add_hardware_to_list(description)

    def hardware_item_activated(self, hardware_qitem):
        '''Signal on hardware_list activated. Triggers loading of controllers.'''
        for hardware_device in self.json_object:
            if self.json_object.get(
                    hardware_device,
                [])['description'] == hardware_qitem.text():
                self.chosen_hardware_device = hardware_device
                self.load_controllers()
                self.ui.flash_firmware.setEnabled(False)
                self.clean_firmware_list()

    def controller_item_activated(self, control_qitem):
        '''Signal on controller_list activated. Triggers loading of firmwares.'''
        self.load_firmware(control_qitem.text())
        self.ui.flash_firmware.setEnabled(False)

    def firmware_item_activated(self, firmware_qitem):
        '''Signal on firmware_list activated.'''
        self.ui.flash_firmware.setEnabled(True)

    def load_controllers(self):
        self.clean_controller_list()
        repo = self.json_object
        for controller in repo.get(self.chosen_hardware_device,
                                   []).get("controller", []):
            self.add_controller_to_list(controller)

    def load_firmware(self, controller_qstring):
        self.clean_firmware_list()
        controller_key = str(controller_qstring)
        repo = self.json_object
        for firmware in repo[
                self.chosen_hardware_device]['controller'][controller_key]:
            self.add_firmware_dict_to_list(firmware)

    def clean_hardware_list(self):
        self.__clean_QListWidget(self.ui.hardware_list)

    def clean_controller_list(self):
        self.__clean_QListWidget(self.ui.controller_list)

    def clean_firmware_list(self):
        self.__clean_QListWidget(self.ui.firmware_list)

    def __clean_QListWidget(self, qlistw):
        qlistw.clear()

    def add_hardware_to_list(self, hardware_device):
        self.ui.hardware_list.addItem(hardware_device)

    def add_controller_to_list(self, controller):
        self.ui.controller_list.addItem(controller)

    def add_firmware_dict_to_list(self, firmware):
        ## Could add more info to display, such as date.
        version = firmware.get("version", "unspecified version")
        self.ui.firmware_list.addItem(version)

    def execute_flash_command(self):
        os_name = platform.system()
        base_dir = os.path.dirname(__file__)
        port = self.ui.port_combo_box.currentText()
        self.__logger.debug("port " + str(port))
        controller_name = str(self.ui.controller_list.currentItem().text())
        firmware_key = str(self.ui.firmware_list.currentItem().text())
        firmware_name = "firmware.hex"
        for firmware in self.json_object[
                self.chosen_hardware_device]['controller'][controller_name]:
            if firmware.get("version") == firmware_key:
                firmware_name = firmware.get("file")

        command = self.generate_command(base_dir, os_name, port,
                                        controller_name, firmware_name)
        try:
            p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)

            rc = p.poll()
            while rc != 0:
                while True:
                    line = p.stdout.readline()
                    # self.__logger.debug(line)
                    if not line:
                        break
                rc = p.poll()

            if rc == 0:
                self.__logger.info("Flashing Done!")
                notify.display_blocking_popup(
                    "Flashing Done!")  # TODO translate
            else:
                self.__logger.info("Error on flashing firmware.")
                notify.display_blocking_popup("Error on flashing firmware.",
                                              "error")  # TODO translate
        except Exception as e:
            self.__logger.info("Error on flashing firmware. " + str(e))
            notify.display_blocking_popup("Error on flashing firmware.",
                                          "error")  # TODO translate

    def generate_command(self, base_dir, os_name, port, controller_name,
                         firmware_name):
        if os_name == "Windows":
            exe_route = self.__app_context.get_resource(
                "ayab/firmware/avrdude.exe")
            exe_route = "\"" + exe_route + "\""
        elif os_name == "Linux":
            # We assume avrdude is available in path
            try:
                subprocess.call(["which avrdude"])
            except:
                self.__logger.error("`avrdude` not found in path")
                return None
            exe_route = "avrdude"
        elif os_name == "Darwin":  # macOS
            exe_route = self.__app_context.get_resource(
                "ayab/firmware/avrdude_mac")

        binary_file = os.path.join(
            self.__app_context.get_resource("ayab/firmware"), controller_name,
            firmware_name)

        serial_port = port
        device = self.device_dict.get(controller_name)

        programmer = self.programmer_dict.get(controller_name, "wiring")

        # avrdude command.
        # http://www.ladyada.net/learn/avr/avrdude.html
        # http://sharats.me/the-ever-useful-and-neat-subprocess-module.html
        exec_command = """{0} -p {1} -c {2} -P {3} -b115200 -D -Uflash:w:"{4}":i """.format(
            exe_route, device, programmer, serial_port, binary_file)

        if os_name == "Windows" or os_name == "Darwin":
            exec_command += " -C \"" + self.__app_context.get_resource(
                "ayab/firmware/avrdude.conf") + "\""

        self.__logger.debug(exec_command)
        return exec_command
