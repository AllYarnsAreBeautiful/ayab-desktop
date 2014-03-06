# -*- coding: utf-8 -*-

import os
import serial
from serial.tools import list_ports


class ayabCommunication(object):
   def __init__(self):
      self.__API_VERSION  = 0x02
      self.__serInterface = 'ttyACM0'
      pass
      
   def openSerial(self):
      try:
        self.__ser = serial.Serial('/dev/'+self.__serInterface, 115200)
      except serial.SerialException:
        print "could not open serial port"
      
   def closeSerial(self):
      self.__ser.close
            
   def listSerialPorts(self):
       """
       Returns a generator for all available serial ports
       """
       if os.name == 'nt':
           # windows
           for i in range(256):
               try:
                   s = serial.Serial(i)
                   s.close()
                   yield 'COM' + str(i + 1)
               except serial.SerialException:
                   pass
       else:
           # unix
           for port in list_ports.comports():
               yield port[0]
   def setSerialPort(pInterface):
      self.__serInterface = pInterface


   def reqStart(self):
      msg = chr(0x01)                     #msg id
      msg += chr(int(StartNeedle))
      msg += chr(int(StopNeedle))
      msg += chr(int(StartLine))
      print "< reqStart"
      __ser.write(msg + '\n\r')
   
   def reqInfo(self):
      print "< reqInfo"
      __ser.write(chr(0x03) + '\n\r')
      
   def cnfLine(self,lineNumber, lineData, flags, crc8):
      msg  = chr(0x42)                    # msg id
      msg += chr(lineNumber)              # line number
      msg += lineData                     # line data
      msg += chr(flags)                   # flags
      msg += chr(crc8)                    # crc8
      print "< cnfLine"
      __ser.write(msg + '\n\r')
