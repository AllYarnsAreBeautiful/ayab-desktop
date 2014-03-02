# -*- coding: utf-8 -*-

import serial                     # serial communication


class machine_com(object):
	def __init__(self):
		print "construct"
		
	def openSerial(self, interface):
		self.__ser = serial.Serial('/dev/ttyACM0', 115200)
		
	def closeSerial(self):
		self.__ser.close
				
	def fsm(self):
		print "fsm"
		
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
