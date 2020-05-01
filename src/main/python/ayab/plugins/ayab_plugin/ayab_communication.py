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

"""Handles the serial communication protocol.

This module handles serial communication, currently works in a synchronous way.
AyabCommunication uses an internal PySerial.Serial object to connect
to the device.
The initializer can also be overriden with a dummy serial object.
"""

import serial
import sliplib

import logging


class AyabCommunication(object):
    """Class Handling the serial communication protocol."""

    def __init__(self, serial=None):
        """Creates an AyabCommunication object,
        with an optional serial-like object."""
        logging.basicConfig(level=logging.DEBUG)
        self.__logger = logging.getLogger(type(self).__name__)
        self.__ser = serial
        self.__driver = sliplib.Driver()
        self.__rxMsgList = list()

    def __del__(self):
        """Handles on delete behaviour closing serial port object."""
        self.close_serial()

    def is_open(self):
        """Return status of the serial interface"""
        if self.__set is not None:
            return self.__ser.is_open
        else:
            return False

    def open_serial(self, pPortname=None):
        """Opens serial port communication with a portName."""
        if not self.__ser:
            self.__portname = pPortname
            try:
                self.__ser = serial.Serial(self.__portname, 115200,
                                           timeout=0.1)
            except:
                self.__logger.error("could not open serial port "
                                    + self.__portname)
                raise CommunicationException()
            return True

    def close_serial(self):
        """Closes serial port."""
        if self.__ser is not None and self.__ser.is_open is True:
            try:
                self.__ser.close()
                del(self.__ser)
                self.__ser = None
                self.__logger.info("Closing Serial port successful.")
            except:
                self.__logger.warning("Closing Serial port failed. \
                                      Was it ever open?")

    def update(self):
        """Reads data from serial and tries to parse as SLIP packet."""
        if self.__ser:
            data = self.__ser.read(1000)
            if len(data) > 0:
                self.__rxMsgList.extend(self.__driver.receive(data))

            if len(self.__rxMsgList) > 0:
                return self.__rxMsgList.pop(0)

        return None

    def req_start(self, startNeedle, stopNeedle, continuousReporting):
        """Sends a start message to the controller."""
        data = bytearray()
        data.append(0x01)
        data.append(startNeedle)
        data.append(stopNeedle)
        data.append(continuousReporting)
        data = self.__driver.send(bytes(data))
        self.__ser.write(data)

    def req_info(self):
        """Sends a request for information to controller."""
        data = self.__driver.send(b'\x03')
        self.__ser.write(data)

    def req_test(self):
        """"""
        data = self.__driver.send(b'\x04')
        self.__ser.write(data)

    def cnf_line(self, lineNumber, lineData, flags, crc8):
        """Sends a line of data via the serial port.

        Sends a line of data to the serial port, all arguments are mandatory.
        The data sent here is parsed by the Arduino controller which sets the
        knitting needles accordingly.

        Args:
          lineNumber (int): The line number to be sent.
          lineData (bytes): The bytearray to be sent to needles.
          flags (bytes): The flags sent to the controller.
          crc8 (bytes, optional): The CRC-8 checksum for transmission.

        """
        data = bytearray()
        data.append(0x42)
        data.append(lineNumber)
        data.extend(lineData)
        data.append(flags)
        data.append(crc8)
        data = self.__driver.send(bytes(data))
        self.__ser.write(data)


class CommunicationException(Exception):
    pass
