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
#    Copyright 2013 Christian Obersteiner, Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop
"""
Mockup Class of AYABCommunication for Test/Simulation purposes
"""

import logging
from time import sleep

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from .communication import AyabCommunication, MessageToken


class AyabCommunicationMockup(AyabCommunication):
    """Class Handling the serial communication protocol."""
    def __init__(self, delay=True, step=False) -> None:
        logging.basicConfig(level=logging.DEBUG)
        self.__logger = logging.getLogger(type(self).__name__)
        self.__delay = delay
        self.__step = step
        self.reset()

    def __del__(self) -> None:
        pass

    def reset(self):
        self.__is_open = False
        self.__is_started = False
        self.__rx_msg_list = list()
        self.__line_count = 0

    def is_open(self) -> bool:
        return self.__is_open

    def close_serial(self) -> None:
        self.reset()

    def open_serial(self, portname=None) -> bool:
        self.__is_open = True
        # if self.__delay:
        #     sleep(2) # wait for knitting progress dialog
        return True

    def update(self) -> tuple:
        if self.__is_open and self.__is_started:
            reqLine = bytearray([0x82, self.__line_count])
            self.__line_count += 1
            self.__line_count %= 256
            self.__rx_msg_list.append(reqLine)
            if self.__delay:
                sleep(1)  # wait for knitting progress dialog to update

            # step through output line by line
            if self.__step:
                # pop up box waits for user input before moving on to next line
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Line number = " + str(self.__line_count))
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                ret = None
                ret = msg.exec_()
                while ret == None:
                    pass

        if len(self.__rx_msg_list) > 0:
            return self.parse_update(self.__rx_msg_list.pop(0))

        return None, MessageToken.none, 0

    def req_start(self, start_needle, stop_needle,
                  continuous_reporting) -> None:
        self.__is_started = True
        cnfStart = bytearray([0xC1, 0x1])
        self.__rx_msg_list.append(cnfStart)

    def req_info(self) -> None:
        cnfInfo = bytearray([0xC3, 0x5, 0xFF, 0xFF])
        self.__rx_msg_list.append(cnfInfo)

        indState = bytearray([0x84, 0x1, 0xFF, 0xFF, 0xFF, 0xFF, 0x1, 0x7F])
        self.__rx_msg_list.append(indState)

    def req_test(self) -> None:
        cnfTest = bytearray([0xC4, 0x1])
        self.__rx_msg_list.append(cnfTest)

    def cnf_line(self, line_number, line_data, flags) -> bool:
        return True
