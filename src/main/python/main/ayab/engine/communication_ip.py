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
#    Copyright 2024 Marcus Hoose (eKnitter.com)
"""Handles the IP communication protocol.

This module handles IP communication, currently works in a synchronous way.
"""

from .communication import *

import socket
import ipaddress

import logging
import pprint
from time import sleep

# Port for TCP
remotePort = 12346

class CommunicationIP(Communication):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(type(self).__name__)
        self.__tarAddressPort = ("255.255.255.255", 12345)
        self.__sockTCP = None
        # socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.rx_msg_list = list()
        self.version = 6

    def __del__(self):
        return self.close_socket()

    def is_open(self):
        if self.__sockTCP is not None:
            return True
        else:
            return False

    def open_serial(self, portname=None):
        print("open: " , portname)
        return self.open_tcp(portname)

    def close_serial(self):
        return True

    def open_tcp(self, pPortname=None):
        try:
            self.__portname = pPortname
            self.__tarAddressPort = (self.__portname, remotePort)
            self.__sockTCP = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            self.__sockTCP.settimeout(10.0)
            self.__sockTCP.connect(self.__tarAddressPort)
            self.__sockTCP.settimeout(0.0)
            self.__sockTCP.setblocking(False)
            self.logger.info("Open TCP Socket successful")
            return True
        except:
            self.logger.info("Open TCP Socket faild")
            return False

    def close_socket(self):
        if self.__sockTCP is not None:
            try:
                self.__sockTCP.close()
                del self.__sockTCP
                self.logger.info("Closing TCP Socket successful.")
            except:
                self.logger.warning("Closing TCP Socket failed. (mem Leak?)")
            self.__sockTCP = None

    def send(self, data):
        if self.__sockTCP is not None:
            try:
                self.__sockTCP.send(bytes(data))
                # self.logger.info("SEND b'"+data+"'")
                sleep(0.5)
            except Exception as e:
                if hasattr(e, 'message'):
                    self.logger.exception(e.message)
                else:
                    self.logger.exception("Connection...Error")
                self.close_socket()

    # NB this method must be the same for all API versions
    def req_info(self):
        self.send([Token.reqInfo.value,self.version])

    def req_test_API6(self):
        self.send([Token.reqTest.value])

    def req_start_API6(self, start_needle, stop_needle,
                       continuous_reporting, disable_hardware_beep):
        """Send a start message to the device."""
        data = bytearray()
        data.append(Token.reqStart.value)
        data.append(start_needle)
        data.append(stop_needle)
        data.append(
            1 * continuous_reporting +
            2 * (not disable_hardware_beep))
        hash = 0
        hash = add_crc(hash, data)
        data.append(hash)
        data = self.send(data)

    def req_init_API6(self, machine: Machine):
        """Send a start message to the device."""
        data = bytearray()
        data.append(Token.reqInit.value)
        data.append(machine.value)
        hash = 0
        hash = add_crc(hash, data)
        data.append(hash)
        data = self.send(data)

    def cnf_line_API6(self, line_number, color, flags, line_data):
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
        data = bytearray()
        data.append(Token.cnfLine.value)
        data.append(line_number)
        data.append(color)
        data.append(flags)
        data.extend(line_data)
        hash = 0
        hash = add_crc(hash, data)
        data.append(hash)
        data = self.send(data)

    def update_API6(self):
        """Read data from serial and parse as SLIP packet."""
        return self.parse_API6(self.read_API6())

    def parse_API6(self, msg):
        if msg is None:
            return None, Token.none, 0
        # else
        for t in list(Token):
            if msg[0] == t.value:
                return msg, t, msg[1]
        # fallthrough
        self.logger.debug("unknown message: ")  # drop crlf
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(msg[1: -1].decode())
        return msg, Token.unknown, 0

    def read_API6(self):
        """Read data from serial as SLIP packet."""
        if self.__sockTCP is not None:
            try:
                data = self.__sockTCP.recv(1024)
            except BlockingIOError:
                data = bytes()
            except Exception as e:
                if hasattr(e, 'message'):
                    self.logger.exception(e.message)
                else:
                    self.logger.exception("Connection...Error")
                self.close_socket()
                self.open_tcp(self.__portname)
                data = bytes()

            if len(data) > 0:
                self.rx_msg_list.append(data)
            if len(self.rx_msg_list) > 0:
                return self.rx_msg_list.pop(0)  # FIFO
        # else
        return None

    def write_API6(self, cmd: str) -> None:
        # SLIP protocol, no CRC8
        if self.__ser:
            self.__ser.write(cmd)


# CRC algorithm after Maxim/Dallas
def add_crc(crc, data):
    for i in range(len(data)):
        n = data[i]
        for j in range(8):
            f = (crc ^ n) & 1
            crc >>= 1
            if f:
                crc ^= 0x8C
            n >>= 1
    return crc & 0xFF


class CommunicationException(Exception):
    pass
