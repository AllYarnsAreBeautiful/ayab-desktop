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

from __future__ import annotations
from typing import Optional
import serial
import sliplib
from enum import Enum
from ..machine import Machine

import logging
import pprint


class Token(Enum):
    unknown = -2
    none = -1
    reqInfo = 0x03
    cnfInfo = 0xC3
    reqTest = 0x04
    cnfTest = 0xC4
    reqStart = 0x01
    cnfStart = 0xC1
    reqLine = 0x82
    cnfLine = 0x42
    indState = 0x84
    helpCmd = 0x26
    sendCmd = 0x27
    beepCmd = 0x28
    readCmd = 0x29
    autoCmd = 0x2A
    testCmd = 0x2B
    quitCmd = 0x2C
    reqInit = 0x05
    cnfInit = 0xC5
    setCmd = 0x2D
    testRes = 0xEE
    debug = 0x9F
    slipFrameEnd = 0xC0


class Communication(object):
    """Class Handling the serial communication protocol."""

    def __init__(self, serial: Optional[serial.Serial] = None):
        """Create an AyabCommunication object,
        with an optional serial communication object."""
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(type(self).__name__)
        self.__ser = serial
        self.__driver = sliplib.Driver()
        self.rx_msg_list: list[bytes] = list()

    def __del__(self) -> None:
        """Handle behaviour on deletion by closing the serial port connection."""
        self.close_serial()

    def is_open(self) -> bool:
        """Return status of the serial interface"""
        if self.__ser is not None:
            return self.__ser.is_open
        else:
            return False

    def open_serial(self, portname: Optional[str] = None) -> bool:
        """Open serial port communication."""
        if not self.__ser:
            self.__portname = portname
            try:
                self.__ser = serial.Serial(self.__portname, 115200, timeout=0.1)
            except Exception:
                self.logger.error(f"could not open serial port {self.__portname}")
                raise CommunicationException()
            return True
        return False

    def close_serial(self) -> None:
        """Close the serial port."""
        if self.__ser is not None and self.__ser.is_open is True:
            try:
                self.__ser.close()
                del self.__ser
                self.__ser = None
                self.logger.info("Closing serial port successful.")
            except Exception:
                self.logger.warning(
                    "Closing serial port failed. \
                                      Was it ever open?"
                )

    # NB this method must be the same for all API versions
    def req_info(self) -> None:
        """Send a request for information to the device."""
        if self.__ser is None:
            return
        data = self.__driver.send(bytes([Token.reqInfo.value]))
        self.__ser.write(data)

    def req_test_API6(self) -> None:
        """Send a request for testing to the device."""
        if self.__ser is None:
            return
        data = self.__driver.send(bytes([Token.reqTest.value]))
        self.__ser.write(data)

    def req_start_API6(
        self,
        start_needle: int,
        stop_needle: int,
        continuous_reporting: bool,
        disable_hardware_beep: bool,
    ) -> None:
        """Send a start message to the device."""
        if self.__ser is None:
            return
        data = bytearray()
        data.append(Token.reqStart.value)
        data.append(start_needle)
        data.append(stop_needle)
        data.append(1 * continuous_reporting + 2 * (not disable_hardware_beep))
        hash = 0
        hash = add_crc(hash, data)
        data.append(hash)
        data = self.__driver.send(bytes(data))
        self.__ser.write(data)

    def req_init_API6(self, machine: Machine) -> None:
        """Send a start message to the device."""
        if self.__ser is None:
            return
        data = bytearray()
        data.append(Token.reqInit.value)
        data.append(machine.value)
        hash = 0
        hash = add_crc(hash, data)
        data.append(hash)
        data = self.__driver.send(bytes(data))
        self.__ser.write(data)

    def quit_API6(self) -> None:
        """Send a quit message to the device."""
        data = bytearray()
        data.append(Token.quitCmd.value)
        data = self.__driver.send(bytes(data))
        self.__ser.write(data)

    def cnf_line_API6(
        self, line_number: int, color: int, flags: int, line_data: bytes
    ) -> None:
        """Send a line of data via the serial port.

        Send a line of data to the serial port. All arguments are mandatory.
        The data sent here is parsed by the Arduino controller which sets the
        knitting needles accordingly.

        Args:
          line_number (int): The line number to be sent.
          color (int): The yarn color to be sent.
          flags (int): The flags sent to the controller.
          line_data (bytes): The bytearray to be sent to needles.
        """
        if self.__ser is None:
            return
        data = bytearray()
        data.append(Token.cnfLine.value)
        data.append(line_number)
        data.append(color)
        data.append(flags)
        data.extend(line_data)
        hash = 0
        hash = add_crc(hash, data)
        data.append(hash)
        data = self.__driver.send(bytes(data))
        self.__ser.write(data)

    def update_API6(self) -> tuple[bytes | None, Token, int]:
        """Read data from serial and parse as SLIP packet."""
        return self.parse_API6(self.read_API6())

    def parse_API6(self, msg: Optional[bytes]) -> tuple[bytes | None, Token, int]:
        if msg is None:
            return None, Token.none, 0
        # else
        for t in list(Token):
            if msg[0] == t.value:
                return msg, t, msg[1]
        # fallthrough
        self.logger.debug("unknown message: ")  # drop crlf
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(msg[1:-1].decode())
        return msg, Token.unknown, 0

    def read_API6(self) -> Optional[bytes]:
        """Read data from serial as SLIP packet."""
        if self.__ser:
            data = self.__ser.read(1000)
            if len(data) > 0:
                self.rx_msg_list.extend(self.__driver.receive(data))
            if len(self.rx_msg_list) > 0:
                return self.rx_msg_list.pop(0)  # FIFO
        # else
        return None

    def write_API6(self, cmd: bytearray) -> None:
        # SLIP protocol, no CRC8
        if self.__ser:
            self.__ser.write(cmd)


# CRC algorithm after Maxim/Dallas
def add_crc(crc: int, data: bytearray) -> int:
    for i in range(len(data)):
        n = data[i]
        for _j in range(8):
            f = (crc ^ n) & 1
            crc >>= 1
            if f:
                crc ^= 0x8C
            n >>= 1
    return crc & 0xFF


class CommunicationException(Exception):
    pass
