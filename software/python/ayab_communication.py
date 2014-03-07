# -*- coding: utf-8 -*-

import serial
from serial.tools import list_ports


class ayabCommunication(object):
   def __init__(self, pPortname):
      self.__portname = pPortname

   def __del__(self): 
      self.closeSerial()
      
   def openSerial(self):
      try:
        self.__ser = serial.Serial(self.__portname, 115200)
      except serial.SerialException:
        print "E: could not open serial port " + self.__portname
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


   def reqStart(self):
      msg = chr(0x01)                     #msg id
      msg += chr(int(StartNeedle))
      msg += chr(int(StopNeedle))
      msg += chr(int(StartLine))
      print "< reqStart"
      self.__ser.write(msg + '\n\r')
   

   def reqInfo(self):
      print "< reqInfo"
      self.__ser.write(chr(0x03) + '\n\r')
      

   def cnfLine(self,lineNumber, lineData, flags, crc8):
      msg  = chr(0x42)                    # msg id
      msg += chr(lineNumber)              # line number
      msg += lineData                     # line data
      msg += chr(flags)                   # flags
      msg += chr(crc8)                    # crc8
      print "< cnfLine"
      self.__ser.write(msg + '\n\r')
