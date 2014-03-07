# -*- coding: utf-8 -*-

import ayab_communication
import time

class ayabControl(object):
    def __init__(self, options):
        self.__API_VERSION  = 0x02
        self.__ayabCom = ayab_communication.ayabCommunication(options.portname)


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


    # def __cnfLine(lineNumber):  
    #     #TODO optimize performance
    #     global LastRequest  
    #     global LineBlock
    #     #initialize bytearray to 0x00
    #     bytes = bytearray(25)
    #     for x in range(0,25):
    #         bytes[x] = 0x00

    #     if lineNumber < 256:
    #         #TODO some better algorithm for block wrapping
    #         # if the last requested line number was 255, wrap to next block of lines 
    #         if LastRequest == 255 and lineNumber == 0:
    #             LineBlock += 1
    #         # store requested line number for next request
    #         LastRequest = lineNumber
    #         # adjust actual line number according to current block
    #         imgLineNumber = lineNumber
    #         imgLineNumber += LineBlock*256

    #         # build output message and screen output
    #         msg = ''
    #         for x in range(0, knit_img_width):
    #             pxl = knit_img.getpixel((x, imgLineNumber))            
    #             if pxl == 255: # contrast color
    #                 # take the image offset into account
    #                 setPixel(bytes,x+ImgStartNeedle)
    #                 msg += "#"
    #             else:
    #                 msg += '-'
    #         msg += str(imgLineNumber)
    #         msg += ' '
    #         msg += str(lineNumber)
    #         msg += ' '
    #         print msg + str(LineBlock)

    #         if imgLineNumber == knit_img_height-1:
    #             lastLine = 0x01
    #         else:
    #             lastLine = 0x00

    #         # TODO implement CRC8
    #         crc8 = 0x00

    #         serial_cnfLine(lineNumber, bytes, lastLine, crc8)
    #     else:
    #         print "requested lineNumber out of range"

    #     if lineNumber == knit_img_height-1:
    #         return 1 # image finished 
    #     else:
    #         return 0


    def knitImage(self, pImage):
        curState = 's_init'
        oldState = 'none'
        reqSent  = 0

        if self.__ayabCom.openSerial() == False:
            return

        while True:
            # TODO catch keyboard interrupts
            rcvMsg, rcvParam = self.__checkSerial()

            if curState == 's_init':
                if oldState != curState:
                    self.__ayabCom.reqInfo()

                if rcvMsg == 'cnfInfo':
                    if rcvParam == API_VERSION:
                        curState == 's_start' 
                    else:
                        print "E: wrong API version: " + str(rcvParam) + (" (expected: )") + str(API_VERSION)
                        return

            if curState == 's_start':
                if oldState != curState:
                    self.__ayabCom.reqStart()

                if rcvMsg == 'cnfStart':
                    if rcvParam == 1:
                        curState = 's_operate'
                    else:
                        print "E: device not ready"
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


