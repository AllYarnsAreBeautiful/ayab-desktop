# -*- coding: utf-8 -*-
#This file is part of AYAB.
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

import time
import serial

#TODO implement logging

class ayabCommunication(object):
   def __init__(self, pCallback, pPortname):
      self.__callback = pCallback
      self.__portname = pPortname

   def __del__(self): 
      self.closeSerial()

   def __printToConsole(self, pString):
      self.__callback(pString)
      
   def openSerial(self):
      try:
        self.__ser = serial.Serial(self.__portname, 115200)
        time.sleep(1)
      except:
        self.__printToConsole("E: could not open serial port " + self.__portname)
        return False
      return True

      
   def closeSerial(self):
      try:
        self.__ser.close()
      except:
        pass


   def readLine(self):
      line = ''
      while self.__ser.inWaiting() > 0:
          line += self.__ser.read(1)
      return line


   def reqStart(self, startNeedle, stopNeedle):
      msg = chr(0x01)                     #msg id
      msg += chr(int(startNeedle))
      msg += chr(int(stopNeedle))
      #print "< reqStart"
      self.__ser.write(msg + '\n\r')
   

   def reqInfo(self):
      #print "< reqInfo"
      self.__ser.write(chr(0x03) + '\n\r')
      

   def cnfLine(self,lineNumber, lineData, flags, crc8):
      msg  = chr(0x42)                    # msg id
      msg += chr(lineNumber)              # line number
      msg += lineData                     # line data
      msg += chr(flags)                   # flags
      msg += chr(crc8)                    # crc8
      #print "< cnfLine"
      self.__ser.write(msg + '\n\r')
