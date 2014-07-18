# -*- coding: utf-8 -*-
# This file is part of AYAB.


from PyQt4 import QtGui, QtCore

import serial
import serial.tools.list_ports

from firmware_flash_ui import Ui_FirmwareFlashFrame

class FirmwareFlash(QtGui.QFrame):

    def __init__(self):
      super(FirmwareFlash, self).__init__(None)

      self.__firmware_ui = Ui_FirmwareFlashFrame()
      self.__firmware_ui.setupUi(self)
      ports_list = self.getSerialPorts()
      def populate(ui, port_list):
        for item in port_list:
          ui.port_combo_box.addItem(item[0])
      populate(self.__firmware_ui, ports_list)

    def getSerialPorts(self):
      """
      Returns a list of all USB Serial Ports
      """
      return list(serial.tools.list_ports.grep("USB"))