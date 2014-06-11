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
#    Copyright 2013 Christian Obersteiner, Andreas Müller
#    https://bitbucket.org/chris007de/ayab-apparat/

"""Handles the serial communication protocol.

This module handles serial communication, currently works in a synchronous way.
AyabCommunication uses an internal PySerial.Serial object to connect to the device.
The initializer can also be overriden with a dummy serial object.
"""

import time
import serial

import logging


class AyabCommunication(object):
  """Class Handling the serial communication protocol."""

  def __init__(self, serial=None):
    """Creates an AyabCommunication object, with an optional serial-like object."""
    logging.basicConfig(level=logging.DEBUG)
    self.__logger = logging.getLogger(__name__)
    self.__ser = serial

  def __del__(self):
       self.close_serial()

  def open_serial(self, pPortname):
    if not self.__ser:
      self.__portname = pPortname
      try:
          self.__ser = serial.Serial(self.__portname, 115200)
          time.sleep(1)
      except:
        raise CommunicationException()
        #print "E: could not open serial port " + self.__portname
        #return False
      return True

  def close_serial(self):
      try:
          self.__ser.close()
      except:
          pass

  def read_line(self):
    """Reads a line from serial communication."""
    #FIXME should be explicitly bytestring
    line = ''
    while self.__ser.inWaiting() > 0:
        line += self.__ser.read(1)
    return line

  def req_start(self, startNeedle, stopNeedle):
      msg = chr(0x01)  # msg id
      msg += chr(int(startNeedle))
      msg += chr(int(stopNeedle))
      # print "< reqStart"
      self.__ser.write(msg + '\n\r')

  def req_info(self):
      # print "< reqInfo"
      self.__ser.write(chr(0x03) + '\n\r')

  def cnf_line(self, lineNumber, lineData, flags, crc8):
      msg = chr(0x42)                    # msg id
      msg += chr(lineNumber)              # line number
      msg += lineData                     # line data
      msg += chr(flags)                   # flags
      msg += chr(crc8)                    # crc8
      # print "< cnfLine"
      # print lineData
      self.__ser.write(msg + '\n\r')


class CommunicationException(Exception):
  pass
