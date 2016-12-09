# -*- coding: utf-8 -*-
# This file is part of AYAB.


from PyQt4 import QtGui
from PyQt4.QtGui import QFrame

import serial
import serial.tools.list_ports
import json
import logging
import os
import platform
import pprint
from subprocess import Popen, PIPE, STDOUT

from firmware_flash_ui import Ui_FirmwareFlashFrame


class FirmwareFlash(QFrame):

    def __init__(self, parent_ui):
        #TODO: add creator that does not depend from super to ease testing.
        super(FirmwareFlash, self).__init__(None)

        self.__parent_ui = parent_ui

        self.ui = Ui_FirmwareFlashFrame()
        self.ui.setupUi(self)

        self.load_ports()
        self.load_json()

        self.ui.controller_list.itemClicked[QtGui.QListWidgetItem].connect(self.controller_item_activated)
        self.ui.flash_firmware.clicked.connect(self.execute_flash_command)

        self.ui.flash_firmware.setEnabled(False)

    def display_blocking_pop_up(self, message="", message_type="info"):
        logging.debug("message emited: '{}'".format(message))
        box_function = {
            "info": QtGui.QMessageBox.information,
            "warning": QtGui.QMessageBox.warning,
            "error": QtGui.QMessageBox.critical,
        }
        message_box_function = box_function.get(message_type,
                                                QtGui.QMessageBox.warning)
        ret = message_box_function(
            self,
            "AYAB",
            message,
            QtGui.QMessageBox.AcceptRole,
            QtGui.QMessageBox.AcceptRole)
        if ret == QtGui.QMessageBox.AcceptRole:
            return True

    def load_json(self):
        self.json_object = self.parse_json("")
        self.load_controllers(self.json_object)

    def parse_json(self, json_string):
        path = (os.path.dirname(os.path.realpath(__file__))
                + "/firmware/firmware.json")
        with open(path) as data_file:
            data = json.load(data_file)
        return data

    def controller_item_activated(self, control_qitem):
        '''Signal on controller_list activated. Enable Flash button.'''
        self.ui.flash_firmware.setEnabled(True)

    def load_controllers(self, json_object):
        self.clean_controller_list()
        for controller in json_object['controller']:
            self.add_controller_to_list(controller['device'])

    def clean_controller_list(self):
        self.__clean_QListWidget(self.ui.controller_list)

    def __clean_QListWidget(self, qlistw):
        qlistw.clear()

    def add_controller_to_list(self, controller):
        self.ui.controller_list.addItem(controller)

    def execute_flash_command(self):
        os_name = platform.system()
        base_dir = os.path.dirname(__file__)
        port = self.ui.port_combo_box.currentText()
        controller_id = self.ui.controller_list.currentRow()
        controller_name = unicode(self.json_object['controller'][controller_id]['device'])
        logging.warning(controller_id)
        logging.warning(controller_name)
        firmware_name = self.json_object['controller'][controller_id]['file']

        command = self.generate_command_with_options(base_dir,
                                                     os_name,
                                                     port,
                                                     controller_name,
                                                     firmware_name)

        try:
            p = Popen(command,
                      stdout=PIPE, stderr=STDOUT, shell=True)

            rc = p.poll()
            while rc != 0:
                while True:
                    line = p.stdout.readline()
                    logging.info
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

    def generate_command_with_options(self, 
                                      base_dir,
                                      os_name,
                                      port,
                                      controller_name,
                                      firmware_name):

        if os_name == "Windows":
            exe_route = os.path.join(base_dir, "firmware", ".\\avrdude.exe")
            exe_route = "\"" + exe_route + "\""
        elif os_name == "Linux":
            # We assume avrdude is available in path
            exe_route = "avrdude"

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

        ## avrdude command.
        ## http://www.ladyada.net/learn/avr/avrdude.html
        ## http://sharats.me/the-ever-useful-and-neat-subprocess-module.html
        exec_command = """{0} -v -p {1} -c {2} -P {3} -b115200 -D -Uflash:w:"{4}":i """.format(
                       exe_route, device, programmer, serial_port, binary_file)
        if os_name == "Windows":
            exec_command += " -C " + os.path.join(base_dir,
                                                  "firmware", "avrdude.conf")

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
