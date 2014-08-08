# -*- coding: utf-8 -*-
# This file is part of AYAB.


from PyQt4 import QtGui
from PyQt4.QtGui import QFrame
from PyQt4 import QtCore

import serial
import serial.tools.list_ports
import json
import logging
import os
import platform
import subprocess

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

      self.ui.hardware_list.itemClicked[QtGui.QListWidgetItem].connect(self.hardware_item_activated)
      self.ui.controller_list.itemClicked[QtGui.QListWidgetItem].connect(self.controller_item_activated)
      self.ui.firmware_list.itemClicked[QtGui.QListWidgetItem].connect(self.firmware_item_activated)
      self.ui.flash_firmware.clicked.connect(self.execute_flash_command)

    def display_blocking_pop_up(self, message="", message_type="info"):
      logging.debug("message emited: '{}'".format(message))
      box_function = {
          "info": QtGui.QMessageBox.information,
          "warning": QtGui.QMessageBox.warning,
          "error": QtGui.QMessageBox.critical,
      }
      message_box_function = box_function.get(message_type, QtGui.QMessageBox.warning)
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
      self.add_items_from_json_object(self.json_object)

    def parse_json(self, json_string):
      x = """{"kh910": {"uno": [{"url": "/", "version": "latest", "file": "firmware.hex"}], "mega2560": [{"url": "", "date": "", "version": "latest", "file": "firmware.hex", "sha1sum": ""}]}, "kh930": {"uno": [{"url": "/", "version": "latest", "file": "firmware.hex"}], "mega2560": [{"url": "", "date": "", "version": "latest", "file": "firmware.hex", "sha1sum": ""}]}, "hardware_test": {"uno": [{"url": "/", "version": "latest", "file": "firmware.hex"}], "mega2560": [{"url": "/", "version": "latest", "file": "firmware.hex"}]}}"""
      json_string = x
      return json.loads(json_string)

    def add_items_from_json_object(self, json_object):
      repo = json_object
      for hardware_device in repo:
        self.add_hardware_to_list(hardware_device)
        #for controller in repo.get(hardware_device, []):
          #self.add_controller_to_list(controller)
          #for firmware in repo[hardware_device][controller]:
            #self.add_firmware_dict_to_list(firmware)

    def hardware_item_activated(self, hardware_qitem):
      '''Signal on hardware_list activated. Triggers loading of controllers.'''
      logging.debug("selected "+hardware_qitem.text())
      self.load_controllers(hardware_qitem.text())

    def controller_item_activated(self, control_qitem):
      '''Signal on controller_list activated. Triggers loading of firmwares.'''
      logging.debug("selected "+control_qitem.text())
      hardware_loaded_qitem = self.ui.hardware_list.currentItem()
      self.load_firmware(hardware_loaded_qitem.text(), control_qitem.text())

    def firmware_item_activated(self, firmware_qitem):
      '''Signal on firmware_list activated.'''
      logging.debug("selected firmware qitem" +firmware_qitem.text())
      self.ui.flash_firmware.setEnabled(True)

    def load_controllers(self, hardware_qstring):
      self.clean_controller_list()
      repo = self.json_object
      hardware_string = unicode(hardware_qstring)
      for controller in repo.get(hardware_string, []):
        self.add_controller_to_list(controller)

    def load_firmware(self, hardware_qstring, controller_qstring):
      self.clean_firmware_list()
      hardware_key = unicode(hardware_qstring)
      controller_key = unicode(controller_qstring)
      repo = self.json_object
      for firmware in repo[hardware_key][controller_key]:
        self.add_firmware_dict_to_list(firmware)
      #print hardware_key
      #print controller_key

    def clean_hardware_list(self):
      self.__clean_QListWidget(self.ui.hardware_list)

    def clean_controller_list(self):
      self.__clean_QListWidget(self.ui.controller_list)

    def clean_firmware_list(self):
      self.__clean_QListWidget(self.ui.firmware_list)

    def __clean_QListWidget(self, qlistw):
      qlistw.clear()

    def add_hardware_to_list(self, hardware_device):
      logging.debug("Hardware Device "+ hardware_device)
      self.ui.hardware_list.addItem(hardware_device)

    def add_controller_to_list(self, controller):
      logging.debug("Controller "+ controller)
      self.ui.controller_list.addItem(controller)

    def add_firmware_dict_to_list(self, firmware):
      ## Could add more info to display, such as date.
      version = firmware.get("version", "unspecified version")
      logging.debug("firmware" + firmware.get("version"))
      self.ui.firmware_list.addItem(version)

    def execute_flash_command(self):
      os_name = platform.system()
      base_dir = os.path.dirname(__file__)
      port = self.ui.port_combo_box.currentText()
      hardware_name = unicode(self.ui.hardware_list.currentItem().text())
      controller_name = unicode(self.ui.controller_list.currentItem().text())
      firmware_key = unicode(self.ui.firmware_list.currentItem().text())
      firmware_name = "firmware.hex"
      for firmware in self.json_object[hardware_name][controller_name]:
        if firmware.get("version") == firmware_key:
          firmware_name = firmware.get("file")

      command = self.generate_command_with_options(base_dir,
                                                   os_name,
                                                   port,
                                                   hardware_name,
                                                   controller_name,
                                                   firmware_name,
                                                   )

      try:
        value = subprocess.call(command, shell=True)
        if value == 0:
          logging.info("Flashing Done!")
          self.display_blocking_pop_up("Flashing Done!")
        else:
          logging.info("Error on flashing firmware.")
          self.display_blocking_pop_up("Error on flashing firmware.", message_type="error")
      except e:
        logging.info("Error on flashing firmware.")
        self.display_blocking_pop_up("Error on flashing firmware.", message_type="error")

    def generate_command_with_options(self, base_dir, os_name, port, hardware_name, controller_name, firmware_name):
      exe_file_dict = {
                        "Windows": os.path.join("firmware", ".\\avrdude.exe"),
                        "Linux": os.path.join("firmware", "avrdude"), #TODO, detect 64bit OS
                      }
      ## If unknown OS we assume avrdude is installed and on the PATH.
      exe_file = exe_file_dict.get(os_name, "avrdude")
      exe_route = os.path.join(base_dir, exe_file)
      conf_file = os.path.join(base_dir, "firmware","avrdude.conf")

      binary_file = os.path.join(base_dir, "firmware", hardware_name, controller_name, firmware_name)
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
      exec_command = """{0} -v -p {1} -C "{2}" -c {3} -P {4} -b115200 -D -Uflash:w:"{5}":i """.format(
                     exe_route, device, conf_file, programmer, serial_port, binary_file)
      logging.debug(exec_command)
      return exec_command

    def load_ports(self):
      ports_list = self.getSerialPorts()
      def populate(ui, port_list):
        for item in port_list:
          ui.port_combo_box.addItem(item[0])
      populate(self.ui, ports_list)


    def getSerialPorts(self):
      """
      Returns a list of all USB Serial Ports
      """
      return list(serial.tools.list_ports.grep("USB"))
