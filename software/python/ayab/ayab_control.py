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

from ayab_communication import AyabCommunication
import time

class ayabControl(object):
    def __init__(self, pCallback):
        self.__callback     = pCallback
        self.__API_VERSION  = 0x03
        self.__ayabCom      = AyabCommunication()

        self.__formerRequest = 0
        self.__lineBlock     = 0

    def __printDebug(self, pString):
        self.__callback(self, pString, "debug")

    def __printPrompt(self, pString):
        self.__callback(self, pString, "prompt")

    def __printStream(self, pString):
        self.__callback(self, pString, "stream")

    def __printError(self, pString):
        self.__callback(self, pString, "error")


    def __setBit(self, int_type, offset):
        mask = 1 << offset
        return(int_type | mask)

    def __setPixel(self, bytearray, pixel):
        numByte = int(pixel/8)
        bytearray[numByte] = self.__setBit(int(bytearray[numByte]),pixel-(8*numByte))
        return bytearray

    def __checkSerial(self):
        time.sleep(1) #TODO if problems in communication, tweak here

        line = self.__ayabCom.read_line()

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
                self.__printError("unknown message: " + line[:]) #drop crlf
                return ("unknown", 0)
        return("none", 0)


    def __cnfLine(self, lineNumber):
        imgHeight = self.__image.imgHeight()
        color         = 0
        indexToSend   = 0
        sendBlankLine = False
        lastLine      = 0x00

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
            # store requested line number for next request
            self.__formerRequest = lineNumber
            reqestedLine         = lineNumber

            # adjust lineNumber with current block
            lineNumber = lineNumber \
                            + (self.__lineBlock*256)

            #########################
            # decide which line to send according to machine type and amount of colors
            # singlebed, 2 color
            if self.__machineType == 'single' \
                    and self.__numColors == 2:

                # color is always 0 in singlebed,
                # because both colors are knitted at once
                color = 0

                # calculate imgRow
                imgRow = lineNumber + self.__startLine

                # 0   1   2   3   4 .. (imgRow)
                # |   |   |   |   |
                # 0 1 2 3 4 5 6 7 8 .. (imageExpanded)
                indexToSend = imgRow * 2

                # Check if the last line of the image was requested
                if imgRow == imgHeight-1:
                    lastLine = 0x01

            # doublebed, 2 color
            elif self.__machineType == 'double' \
                    and self.__numColors == 2:

                # calculate imgRow
                imgRow = int(lineNumber/2) + self.__startLine

                # 0 0 1 1 2 2 3 3 4 4 .. (imgRow)
                # 0 1 2 3 4 5 6 7 8 9 .. (lineNumber)
                # | |  X  | |  X  | |
                # 0 1 3 2 4 5 7 6 8 9 .. (imageExpanded)
                lenImgExpanded = len(self.__image.imageExpanded())
                indexToSend = self.__startLine*2

                # TODO more beautiful algo
                if lineNumber%4 == 1 or lineNumber%4 == 2:
                    color = 1
                else:
                    color = 0

                if (lineNumber-2)%4 == 0:
                    indexToSend += lineNumber+1

                elif (lineNumber-2)%4 == 1:
                    indexToSend += lineNumber-1
                    if (imgRow == imgHeight-1) \
                        and (indexToSend == lenImgExpanded-2):
                        lastLine = 0x01
                else:
                    indexToSend += lineNumber
                    if (imgRow == imgHeight-1) \
                        and (indexToSend == lenImgExpanded-1):
                        lastLine = 0x01

            # doublebed, multicolor
            elif self.__machineType == 'double' \
                    and self.__numColors > 2:

                # calculate imgRow
                imgRow = int(lineNumber/(self.__numColors*2)) + self.__startLine

                if (lineNumber % 2) == 0:
                    color = (lineNumber/2) % self.__numColors
                    indexToSend = (imgRow * self.__numColors) + color
                    self.__printPrompt("COLOR" + str(color))
                else:
                    sendBlankLine = True

                # TODO Check assignment
                if imgRow == imgHeight-1 \
                    and (indexToSend == lenImgExpanded-1):
                    lastLine = 0x01
            #########################

            # assign pixeldata
            imgStartNeedle = self.__image.imgStartNeedle()
            imgStopNeedle  = self.__image.imgStopNeedle()


            # set the bitarray
            for col in range(0, 200):
                if color == 0 \
                and self.__machineType == 'double':
                    if col < imgStartNeedle \
                        or col > imgStopNeedle:
                        bytes = self.__setPixel(bytes,col)


            for col in range(0, self.__image.imgWidth()):
                pxl = (self.__image.imageExpanded())[indexToSend][col]
                # take the image offset into account
                if pxl == True and sendBlankLine == False:
                    bytes = self.__setPixel(bytes,col+self.__image.imgStartNeedle())

            # TODO implement CRC8
            crc8 = 0x00

            # send line to machine
            self.__ayabCom.cnf_line(reqestedLine, bytes, lastLine, crc8)

            # screen output
            msg = str((self.__image.imageExpanded())[indexToSend])
            msg += ' Image Row: ' + str(imgRow)
            msg += ' (indexToSend: ' + str(indexToSend)
            msg += ', reqLine: ' + str(reqestedLine)
            msg += ', lineNumber: ' + str(lineNumber)
            msg += ', lineBlock:' + str(self.__lineBlock) + ')'
            self.__printStream(msg)
        else:
            self.__printError("requested lineNumber out of range")

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

        if self.__ayabCom.open_serial(pOptions.portname) == False:
            self.__printError("Could not open serial port")
            return

        while True:
            # TODO catch keyboard interrupts to abort knitting
            rcvMsg, rcvParam = self.__checkSerial()
            if curState == 's_init':
                if oldState != curState:
                    self.__ayabCom.req_info()

                if rcvMsg == 'cnfInfo':
                    if rcvParam == API_VERSION:
                        curState = 's_start'
                        self.__printPrompt("Please init machine")
                    else:
                        self.__printError("wrong API version: " + str(rcvParam) \
                            + (" (expected: )") + str(API_VERSION))
                        return

            if curState == 's_start':
                if oldState != curState:
                    self.__ayabCom.req_start(self.__image.knitStartNeedle(), \
                        self.__image.knitStopNeedle() )

                if rcvMsg == 'cnfStart':
                    if rcvParam == 1:
                        curState = 's_operate'
                        self.__printPrompt("Ready to Operate")
                    else:
                        self.__printError("device not ready")
                        return

            if curState == 's_operate':
                if rcvMsg == 'reqLine':
                    imageFinished = self.__cnfLine(rcvParam)
                    if imageFinished:
                        curState = 's_finished'

            if curState == 's_finished':
                self.__printPrompt("Image finished")
                return

            oldState = curState

        return


