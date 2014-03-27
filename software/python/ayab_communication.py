# -*- coding: utf-8 -*-

import time
import serial

#TODO implement logging

class ayabCommunication(object):
   def __init__(self, pPortname):
      self.__portname = pPortname

   def __del__(self): 
      self.closeSerial()
      
   def openSerial(self):
      try:
        self.__ser = serial.Serial(self.__portname, 115200)
        time.sleep(1)
      except:
        print "E: could not open serial port " + self.__portname
        raw_input("press Enter")
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


   def reqStart(self, startNeedle, stopNeedle, startLine):
      msg = chr(0x01)                     #msg id
      msg += chr(int(startNeedle))
      msg += chr(int(stopNeedle))
      msg += chr(int(startLine))
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
