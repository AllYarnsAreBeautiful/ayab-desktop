# -*- coding: utf-8 -*-
# This file is part of AYAB.


from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QFrame

import serial
import serial.tools.list_ports
import json
import logging
import os
import sys
import platform
import subprocess
from subprocess import Popen, PIPE, STDOUT

from .firmware_flash_ui import Ui_FirmwareFlashFrame


class FirmwareFlash(QFrame):

    def __init__(self, parent_ui):
        # TODO: add creator that does not depend from super to ease testing.
        super(FirmwareFlash, self).__init__(None)

        self.__parent_ui = parent_ui

        self.ui = Ui_FirmwareFlashFrame()
        self.ui.setupUi(self)

        self.load_ports()
        self.load_json()

        self.ui.hardware_list.itemClicked[QtWidgets.QListWidgetItem].connect(self.hardware_item_activated)
        self.ui.controller_list.itemClicked[QtWidgets.QListWidgetItem].connect(self.controller_item_activated)
        self.ui.firmware_list.itemClicked[QtWidgets.QListWidgetItem].connect(self.firmware_item_activated)
        self.ui.flash_firmware.clicked.connect(self.execute_flash_command)

    def display_blocking_pop_up(self, message="", message_type="info"):
        logging.debug("message emited: '{}'".format(message))
        box_function = {
            "info": QtWidgets.QMessageBox.information,
            "warning": QtWidgets.QMessageBox.warning,
            "error": QtWidgets.QMessageBox.critical,
        }
        message_box_function = box_function.get(message_type,
                                                QtWidgets.QMessageBox.warning)
        ret = message_box_function(
            self,
            "AYAB",
            message,
            QtWidgets.QMessageBox.Ok,
            QtWidgets.QMessageBox.Ok)
        if ret == QtWidgets.QMessageBox.Ok:
            return True

    def load_json(self):
        self.json_object = self.parse_json("")
        self.add_items_from_json_object(self.json_object)

    def parse_json(self, json_string):
        os_name = platform.system()
        if os_name == "Windows":
            # determine if application is a script file or frozen exe
            if getattr(sys, 'frozen', False):
                path = (os.path.dirname(sys.executable) +
                        "\\plugins\\ayab_plugin\\firmware\\firmware.json")
            else:
                path = (os.path.dirname(os.path.realpath(__file__)) +
                    "/firmware/firmware.json")
        else:
            path = (os.path.dirname(os.path.realpath(__file__)) +
                    "/firmware/firmware.json")

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
            if self.json_object.get(hardware_device, [])['description'] == hardware_qitem.text():
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
        for controller in repo.get(self.chosen_hardware_device, []).get("controller", []):
            self.add_controller_to_list(controller)

    def load_firmware(self, controller_qstring):
        self.clean_firmware_list()
        controller_key = str(controller_qstring)
        repo = self.json_object
        for firmware in repo[self.chosen_hardware_device]['controller'][controller_key]:
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
        controller_name = str(self.ui.controller_list.currentItem().text())
        firmware_key = str(self.ui.firmware_list.currentItem().text())
        firmware_name = "firmware.hex"
        for firmware in self.json_object[self.chosen_hardware_device]['controller'][controller_name]:
            if firmware.get("version") == firmware_key:
                firmware_name = firmware.get("file")

        command = self.generate_command_with_options(base_dir,
                                                     os_name,
                                                     port,
                                                     controller_name,
                                                     firmware_name,
                                                     )

        try:
            p = Popen(command,
                      stdout=PIPE, stderr=STDOUT, shell=True)

            rc = p.poll()
            while rc != 0:
                while True:
                    line = p.stdout.readline()
                    logging.debug(line)
                    if not line:
                        break
                rc = p.poll()

            if rc == 0:
                logging.info("Flashing Done!")
                self.display_blocking_pop_up("Flashing Done!")
            else:
                logging.info("Error on flashing firmware.")
                self.display_blocking_pop_up("Error on flashing firmware.",
                                             message_type="error")
        except Exception as e:
            logging.info("Error on flashing firmware." + e)
            self.display_blocking_pop_up("Error on flashing firmware.",
                                         message_type="error")

    def generate_command_with_options(self, base_dir, os_name, port,
                                      controller_name, firmware_name):

        if os_name == "Windows":
            # determine if application is a script file or frozen exe
            if getattr(sys, 'frozen', False):
                exe_route = os.path.join(os.path.dirname(sys.executable),
                        "plugins","ayab_plugin","firmware","avrdude.exe")
            else:
                exe_route = os.path.join(base_dir, "firmware", "avrdude.exe")
            exe_route = "\"" + exe_route + "\""
        elif os_name == "Linux":
            # We assume avrdude is available in path
            try:
                subprocess.call(["which avrdude"])
            except:
                logging.error("avrdude not found in path")
            exe_route = "avrdude"
        elif os_name == "Darwin":  # macOS
            exe_route = os.path.join(base_dir, "firmware", "avrdude_mac")

        if os_name == "Windows":
            if getattr(sys, 'frozen', False):
                binary_file = os.path.join(os.path.dirname(sys.executable),
                        "plugins","ayab_plugin","firmware",controller_name,firmware_name)
            else:
                binary_file = os.path.join(base_dir, "firmware",
                                       controller_name, firmware_name)
        else:
            binary_file = os.path.join(base_dir, "firmware",
                                       controller_name, firmware_name)

        serial_port = port
        # List of Arduino controllers and their avrdude names.
        device_dict = {
            "mega2560": "m2560",
            "uno": "atmega328p",
        }
        device = device_dict.get(controller_name)

        programmer_dict = {
            "uno": "arduino",
            "mega2560": "wiring",
        }
        programmer = programmer_dict.get(controller_name, "wiring")

        # avrdude command.
        # http://www.ladyada.net/learn/avr/avrdude.html
        # http://sharats.me/the-ever-useful-and-neat-subprocess-module.html
        exec_command = """{0} -p {1} -c {2} -P {3} -b115200 -D -Uflash:w:"{4}":i """.format(
                       exe_route, device, programmer, serial_port, binary_file)

        if os_name == "Windows" or os_name == "Darwin":
            # determine if application is a script file or frozen exe
            if getattr(sys, 'frozen', False):
                exec_command += " -C \"" + os.path.join(os.path.dirname(sys.executable),
                                          "plugins","ayab_plugin","firmware","avrdude.conf") + "\""
            else:
                exec_command += " -C \"" + os.path.join(base_dir,
                                                      "firmware", "avrdude.conf") + "\""

        logging.debug(exec_command)
        return exec_command

    def load_ports(self):
        ports_list = self.getSerialPorts()

        def populate(ui, port_list):
            for item in port_list:
                ui.port_combo_box.addItem(item[0])
        populate(self.ui, ports_list)

    def getSerialPorts(self):
        """Returns a list of all USB Serial Ports"""
        return list(serial.tools.list_ports.grep("USB"))
