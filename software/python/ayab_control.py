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


    def __checkSerial(self):
        time.sleep(0.5) #TODO if problems in communication, tweak here

        line = self.__ayabCom.readLine()

        if line != '':
            msgId = ord(line[0])            
            if msgId == 0xC1:    # cnfStart
                print "> cnfStart: " + str(ord(line[1]))
                return ("cnfStart", ord(line[1]))            

            elif msgId == 0xC3: # cnfInfo
                print "> cnfInfo: Version=" + str(ord(line[1]))
                return ("cnfInfo", ord(line[1]))

            elif msgId == 0x82: #reqLine            
                print "> reqLine: " + str(ord(line[1]))
                return ("reqLine", ord(line[1]))
                
            else:
                print "> unknown message: " + line[:] #drop crlf
                return ("unknown", 0)
        return("none", 0)


    def __cnfLine(self, lineNumber):  
        imgHeight = self.__image.imgHeight()
        #TODO optimize performance
        #initialize bytearray to 0x00
        bytes = bytearray(25)
        for x in range(0,25):
            bytes[x] = 0x00

        if lineNumber < 256:
            #TODO some better algorithm for block wrapping
            # if the last requested line number was 255, wrap to next block of lines 
            if self.__formerRequest == 255 and lineNumber == 0:
                self.__lineBlock += 1
            # store requested line number for next request
            self.__formerRequest = lineNumber

            # TODO decide which line to send according to machine type and amount of colors
            #
            #

            # adjust actual line number according to current block
            imgLineNumber = lineNumber
            imgLineNumber += self.__lineBlock*256

            # build output message and screen output
            msg = ''
            for col in range(0, self.__image.imgWidth()):
                pxl = (self.__image.imageIntern())[imgLineNumber][col] 
                
                # take the image offset into account
                #setPixel(bytes,x+ImgStartNeedle)
                msg += str(pxl)

            msg += str(imgLineNumber)
            msg += ' '
            msg += str(lineNumber)
            msg += ' '
            print msg + str(self.__lineBlock)

            if imgLineNumber == imgHeight-1:
                lastLine = 0x01
            else:
                lastLine = 0x00

            # TODO implement CRC8
            crc8 = 0x00

            self.__ayabCom.cnfLine(lineNumber, bytes, lastLine, crc8)
        else:
            print "requested lineNumber out of range"

        if lineNumber == imgHeight-1:
            return 1 # image finished 
        else:
            return 0


    def knitImage(self, pImage):
        self.__formerRequest = 0
        self.__image         = pImage
        self.__lineBlock     = pImage.startBlock()
        
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
                        curState == 's_start' 
                    else:
                        print "E: wrong API version: " + str(rcvParam) \
                            + (" (expected: )") + str(API_VERSION)
                        raw_input("press Enter")
                        return

            if curState == 's_start':
                if oldState != curState:
                    self.__ayabCom.reqStart(self.__image.knitStartNeedle(), \
                        self.__image.knitStopNeedle() ,
                        self.__image.startLine() )

                if rcvMsg == 'cnfStart':
                    if rcvParam == 1:
                        curState = 's_operate'
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


