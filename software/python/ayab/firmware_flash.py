# -*- coding: utf-8 -*-
# This file is part of AYAB.


from PyQt4 import QtGui, QtCore

import serial
import serial.tools.list_ports
import json
import logging

from firmware_flash_ui import Ui_FirmwareFlashFrame

class FirmwareFlash(QtGui.QFrame):

    def __init__(self):
      #TODO: add creator that does not depend from super to ease testing.
      super(FirmwareFlash, self).__init__(None)

      self.ui = Ui_FirmwareFlashFrame()
      self.ui.setupUi(self)

      #TODO: move to function
      ports_list = self.getSerialPorts()
      def populate(ui, port_list):
        for item in port_list:
          ui.port_combo_box.addItem(item[0])
      populate(self.ui, ports_list)

      self.load_json()

    def load_json(self):
      json_object = self.parse_json("")
      self.add_items_from_json_object(json_object)

    def parse_json(self, json_string):
      x = """{"kh910": {"uno": [{"url": "/", "version": "latest"}, {"url": "/kh910/uno/ayab_k910_uno_v3.hex", "version": "v3"}], "mega2560": [{"url": "/", "date": "", "version": "latest", "sha1sum": ""}, {"url": "/kh910/mega2560/ayab_kh910_mega_v3.hex", "version": "v3"}]}, "kh930": {"uno": [{"url": "/kh930/uno/ayab_kh930_uno_v3.hex", "version": "latest"}], "mega2560": [{"url": "/kh930/mega/ayab_kh930_mega_v3.hex", "version": "latest"}]}, "hardware_test": {"uno": [{"version": "latest"}], "mega2560": [{"date": "", "version": "latest", "sha1sum": ""}]}}"""
      json_string = x
      return json.loads(json_string)

    def add_items_from_json_object(self, json_object):
      repo = json_object
      for hardware_device in repo:
        self.add_hardware_to_list(hardware_device)
        for controller in repo.get(hardware_device, []):
          self.add_controller_to_list(controller)
          for firmware in repo[hardware_device][controller]:
            self.add_firmware_dict_to_list(firmware)

    def add_hardware_to_list(self, hardware_device):
      logging.debug("Hardware Device "+ hardware_device)
      self.ui.firmware_list.addItem(hardware_device)

    def add_controller_to_list(self, controller):
      logging.debug("Controller "+ controller)
      self.ui.device_list.addItem(controller)

    def add_firmware_dict_to_list(self, firmware):
      ## Could add more info to display, such as date.
      version = firmware.get("version", "unspecified version")
      logging.debug("firmware" + firmware.get("version"))
      self.ui.firmware_list.addItem(version)

    def getSerialPorts(self):
      """
      Returns a list of all USB Serial Ports
      """
      return list(serial.tools.list_ports.grep("USB"))