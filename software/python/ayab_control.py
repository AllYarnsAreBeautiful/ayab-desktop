# -*- coding: utf-8 -*-

import ayab_communication
import time

# TODO insert logging

class ayabControl(object):
    def __init__(self, options):
        self.__API_VERSION  = 0x02
        self.__ayabCom = ayab_communication.ayabCommunication(options.portname)

        self.__formerRequest = 0
        self.__lineBlock     = 0

    # TODO decision: callback vs. python logger
    # http://stackoverflow.com/questions/1904351/python-observer-pattern-examples-tips
    # vs.
    # http://docs.python.org/2/library/logging.html
    #     self.callbacks = []

    # def subscribe(self, callback):
    #     self.callbacks.append(callback)

    def __setBit(self, int_type, offset):
        mask = 1 << offset
        return(int_type | mask)

    def __setPixel(self, bytearray, pixel):
        numByte = int(pixel/8)
        bytearray[numByte] = self.__setBit(int(bytearray[numByte]),pixel-(8*numByte))
        return bytearray

    def __checkSerial(self):
        time.sleep(0.5) #TODO if problems in communication, tweak here

        line = self.__ayabCom.readLine()

        if line != '':
            msgId = ord(line[0])            
            if msgId == 0xC1:    # cnfStart
                #print "> cnfStart: " + str(ord(line[1]))
                return ("cnfStart", ord(line[1]))            

            elif msgId == 0xC3: # cnfInfo
                #print "> cnfInfo: Version=" + str(ord(line[1]))
                return ("cnfInfo", ord(line[1]))

            elif msgId == 0x82: #reqLine            
                #print "> reqLine: " + str(ord(line[1]))
                return ("reqLine", ord(line[1]))
                
            else:
                print "> unknown message: " + line[:] #drop crlf
                return ("unknown", 0)
        return("none", 0)


    def __cnfLine(self, lineNumber):  
        imgHeight = self.__image.imgHeight()

        sendBlankLine = False

        # TODO optimize performance
        # initialize bytearray to 0x00
        bytes = bytearray(25)
        for x in range(0,25):
            bytes[x] = 0x00

        if lineNumber < 256:
            # TODO some better algorithm for block wrapping
            # if the last requested line number was 255, wrap to next block of lines 
            if self.__formerRequest == 255 and lineNumber == 0:
                self.__lineBlock += 1

            # adjust actual line number according to current block
            imgLineNumber = lineNumber \
                            + (self.__lineBlock*256) \
                            + self.__startLine

            # store requested line number for next request
            self.__formerRequest = lineNumber

            #########################
            # decide which line to send according to machine type and amount of colors
            # singlebed, 2 color
            if self.__machineType == 'single' \
                    and self.__numColors == 2:
                # 0   1   2   3   4 .. (imgLineNumber)
                # |   |   |   |   | 
                # 0 1 2 3 4 5 6 7 8 .. (imageExpanded)
                lineToSend    = imgLineNumber * 2

            # doublebed, 2 color
            elif self.__machineType == 'double' \
                    and self.__numColors == 2:                
                # 0 1 2 3 4 5 6 7 8 9 .. (imgLineNumber)
                # | |  X  | |  X  | |
                # 0 1 3 2 4 5 7 6 8 9 .. (imageExpanded)
                if (imgLineNumber-2)%4 == 0:
                    lineToSend = imgLineNumber+1
                elif (imgLineNumber-2)%4 == 1:
                    lineToSend = imgLineNumber-1
                else:
                    lineToSend = imgLineNumber
            
            # doublebed, multicolor    
            elif self.__machineType == 'double' \
                    and self.__numColors > 2:

                color = (imgLineNumber/2) % self.__numColors
                block = imgLineNumber/(self.__numColors*2)
                lineToSend = (block * self.__numColors) + color

                if imgLineNumber % 2 == 0:
                    sendBlankLine = False
                else:
                    sendBlankLine = True
            #########################

            # build output message and screen output
            for col in range(0, self.__image.imgWidth()):
                pxl = (self.__image.imageExpanded())[lineToSend][col]                
                # take the image offset into account
                if pxl == True and sendBlankLine == False:
                    bytes = self.__setPixel(bytes,col+self.__image.imgStartNeedle())

            msg = str((self.__image.imageExpanded())[lineToSend])
            msg += ' Image Line: ' + str(imgLineNumber)
            msg += ' (lineToSend: ' + str(lineToSend)
            msg += ', internal Line: ' + str(lineNumber)
            msg += ', Block:' + str(self.__lineBlock) + ')'
            print msg

            # Check if the last line of the image was requested
            if imgLineNumber == imgHeight-1:
                lastLine = 0x01
            else:
                lastLine = 0x00

            # TODO implement CRC8
            crc8 = 0x00

            self.__ayabCom.cnfLine(lineNumber, bytes, lastLine, crc8)
        else:
            print "E: requested lineNumber out of range"

        if lastLine:
            return 1 # image finished 
        else:
            return 0 # keep knitting


    def knitImage(self, pImage, pOptions):
        self.__formerRequest = 0
        self.__image         = pImage
        self.__startLine     = pImage.startLine()

        self.__numColors     = pOptions.num_colors
        self.__machineType   = pOptions.machine_type
        
        API_VERSION = self.__API_VERSION
        curState = 's_init'
        oldState = 'none'

        if self.__ayabCom.openSerial() == False:
            return

        while True:
            # TODO catch keyboard interrupts to abort knitting
            rcvMsg, rcvParam = self.__checkSerial()
            if curState == 's_init':
                if oldState != curState:
                    self.__ayabCom.reqInfo()

                if rcvMsg == 'cnfInfo':
                    if rcvParam == API_VERSION:
                        curState = 's_start'                        
                        raw_input(">Please init machine")
                    else:
                        print "E: wrong API version: " + str(rcvParam) \
                            + (" (expected: )") + str(API_VERSION)
                        raw_input("press Enter")
                        return

            if curState == 's_start':
                if oldState != curState:
                    self.__ayabCom.reqStart(self.__image.knitStartNeedle(), \
                        self.__image.knitStopNeedle() , \
                        # TODO remove startLine from machine API
                        #self.__image.startLine() )
                        0 )

                if rcvMsg == 'cnfStart':
                    if rcvParam == 1:
                        curState = 's_operate'
                        print "================="
                        print ">Ready to Operate"
                        print "================="
                    else:
                        print "E: device not ready"
                        raw_input("press Enter")
                        return

            if curState == 's_operate':
                if rcvMsg == 'reqLine':
                    imageFinished = self.__cnfLine(rcvParam)
                    if imageFinished:
                        curState = 's_finished'

            if curState == 's_finished':
                print "Image finished"
                raw_input("press Enter")
                return

            oldState = curState
        
        return  


