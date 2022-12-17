# -*- coding: utf-8 -*-
# This file is for AYAB @ https://github.com/AllYarnsAreBeautiful/ayab-desktop
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
#    Copyright 2021 Marcus Hoose
#    

"""Handles the ip communication protocol.

This module handles ip communication.
AyabIP uses an socket object to connect to the device.
"""

from .ayab_communication import AyabCommunication
import socket
import ipaddress
import logging
from time import sleep

# Port for TCP
remotePort = 12346


class AyabIP(AyabCommunication):

    def __init__(self, serial=None):
        super().__init__(serial=serial)
        logging.basicConfig(level=logging.DEBUG)
        self.__logger = logging.getLogger(type(self).__name__)
        self.__rxMsgList = list()
        self.__tarAddressPort = ("255.255.255.255", 12345)
        self.__sockTCP = None
        self.__isIP = False

    def __del__(self):
        self.close_socket()
        return super().__del__()

    def isOpen(self):
        return (not self.__isIP) or self.__sockTCP

    def open_serial(self, pPortname=None):
        try:
            ip = ipaddress.IPv4Address(ipaddress.ip_address(pPortname))
            return self.open_tcp(pPortname=pPortname)
        except:
            return super().open_serial(pPortname=pPortname)

    def close_serial(self):
        return super().close_serial()

    def open_tcp(self, pPortname=None):
        try:
            self.__portname = pPortname
            self.__tarAddressPort = (self.__portname, remotePort)
            self.__sockTCP = socket.socket(
                family=socket.AF_INET, type=socket.SOCK_STREAM)
            self.__sockTCP.settimeout(10.0)
            self.__sockTCP.connect(self.__tarAddressPort)
            self.__sockTCP.settimeout(0.0)
            self.__sockTCP.setblocking(False)
            self.__isIP = True
            self.__logger.info("Open TCP Socket successful")
            return True
        except:
            self.__logger.info("Open TCP Socket faild")
            return False

    def close_socket(self):
        if self.__sockTCP is not None:
            try:
                self.__sockTCP.close()
                del(self.__sockTCP)
                self.__sockTCP = None
                self.__logger.info("Closing TCP Socket successful.")
            except:
                self.__logger.warning(
                    "Closing TCP Socket failed. Was it ever open?")

    def update(self):
        """Reads data from serial and tries to parse as SLIP packet."""

        if self.__isIP:
            if self.__sockTCP:

                try:
                    data = self.__sockTCP.recv(1024)
                except BlockingIOError:
                    data = bytes()
                except Exception as e:
                    if hasattr(e, 'message'):
                        self.__logger.exception(e.message)
                    else:
                        self.__logger.exception("Connection...Error")
                    self.close_socket()
                    # sleep(0.001)
                else:
                    if len(data) > 0:
                        self.__rxMsgList.append(data)

                if len(self.__rxMsgList) > 0:
                    return self.__rxMsgList.pop(0)

            return None
        else:
            return super().update()

    def req_start(self, startNeedle, stopNeedle, continuousReporting):
        if self.__isIP:
            if self.__sockTCP:
                data = bytearray()
                data.append(0x01)
                data.append(startNeedle)
                data.append(stopNeedle)
                data.append(continuousReporting)
                try:
                    self.__sockTCP.send(bytes(data))
                except Exception as e:
                    if hasattr(e, 'message'):
                        self.__logger.exception(e.message)
                    else:
                        self.__logger.exception("Connection...Error")
                    self.close_socket()
        else:
            return super().req_start(startNeedle, stopNeedle, continuousReporting)

    def req_info(self):
        if self.__isIP:
            if self.__sockTCP:
                try:
                    self.__sockTCP.send(b'\x03')
                    self.__logger.info("SEND b'\x03'")
                    sleep(0.5)
                except Exception as e:
                    if hasattr(e, 'message'):
                        self.__logger.exception(e.message)
                    else:
                        self.__logger.exception("Connection...Error")
                    self.close_socket()

        else:
            return super().req_info()

    def req_test(self):
        if self.__isIP:
            if self.__sockTCP:
                try:
                    self.__sockTCP.send(b'\x04')
                except Exception as e:
                    if hasattr(e, 'message'):
                        self.__logger.exception(e.message)
                    else:
                        self.__logger.exception("Connection...Error")
                    self.close_socket()
        else:
            return super().req_test()

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
        dateSend = 0
        if self.__isIP:
            if self.__sockTCP:
                data = bytearray()
                data.append(0x42)
                data.append(lineNumber)
                data.extend(lineData)
                data.append(flags)
                data.append(crc8)
            try:
                dateSend = self.__sockTCP.send(bytes(data))
            except:
                return 0
        else:
            try:
                super().cnf_line(lineNumber, lineData, flags, crc8)
                dateSend = len(lineData) + 4
            except:
                return 0
            return

        return dateSend


class IPException(Exception):
    pass
