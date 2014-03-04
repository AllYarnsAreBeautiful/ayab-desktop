# -*- coding: utf-8 -*-

import serial                     # serial communication


class machine_com(object):
	def __init__(self,pInterface):
		self.__ser = serial.Serial('/dev/ttyACM0', 115200)
		print "construct"
	
	def __del__(self):
		self.__ser.close
		print "delete"
				
	def parseSerial(self):
		#TODO only parse response and return message name and parameter?
	    print "parse serial"
	    time.sleep(0.5) #TODO if problems in communication, tweak here
		line = ''
		while self.__ser.inWaiting() > 0:
			line += self.__ser.read(1)
			#line = ser.readline()    

		if line != '':
			msgId = ord(line[0])            
			if msgId == 0xC1:    # cnfStart
				msg = "> cnfStart: "

				# reqStart was successful, proceed to next state
				if curState == 's_start' and ord(line[1]) == 1:
					curState = 's_operate'
					print "-----Ready to operate-----"
				else:
					curState = 's_abort'
					print "failed"

			elif msgId == 0xC3: # cnfInfo
				print "> cnfInfo: Version=" + str(ord(line[1]))
				# reqInfo showed the right version, proceed to next state            
				if curState == 's_init' and ord(line[1]) == API_VERSION:
					curState = 's_start'
				else:
					curState = 's_abort'

			elif msgId == 0x82: #reqLine            
				msg = "> reqLine: "
				msg += str(ord(line[1]))
				print msg
				
				if curState == 's_operate':
					_imgFinished = cnfLine(ord(line[1]))
					if _imgFinished:
						curState = 's_finished'
			else:
				print "unknown message: "
				print line[:] #drop crlf
				curState = 's_abort'

		return curState
		
		
	def reqStart(self):
		msg = chr(0x01)                     # msg id
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
