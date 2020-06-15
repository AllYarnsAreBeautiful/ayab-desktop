# -*- coding: utf-8 -*-
# This file is part of AYAB.
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
#    Copyright 2013-2020 Sebastian Oliva, Christian Obersteiner,
#    Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop


from .ayab_communication import AyabCommunication
from .ayab_communication_mockup import AyabCommunicationMockup

import logging

from bitarray import bitarray
from enum import Enum

MACHINE_WIDTH = 200
BLOCK_LENGTH = 256

class KnittingState(Enum):
    NONE = 0
    SETUP = 1
    INIT = 2
    WAIT_FOR_INIT = 3
    START = 4
    OPERATE = 5
    FINISHED = 6


class AYABControlKnitResult(Enum):
    NONE = 0
    ERROR_INVALID_SETTINGS = 1
    ERROR_SERIAL_PORT = 2
    CONNECTING_TO_MACHINE = 3
    WAIT_FOR_INIT = 4
    ERROR_WRONG_API = 5
    PLEASE_KNIT = 6
    DEVICE_NOT_READY = 7
    FINISHED = 8


class KnittingMode(Enum):
    SINGLEBED = 0
    CLASSIC_RIBBER_1 = 1  # Classic Ribber 1
    # CLASSIC_RIBBER_2 = 2            # Classic Ribber 2
    MIDDLECOLORSTWICE_RIBBER = 2  # Middle-Colors-Twice Ribber
    HEARTOFPLUTO_RIBBER = 3  # Heart-of-Pluto Ribber
    CIRCULAR_RIBBER = 4  # Circular Ribber


def even(x):
    return x % 2 == 0

def odd(x):
    return x % 2 == 1

class AYABControl(object):
    def __init__(self):
        self.__logger = logging.getLogger(type(self).__name__)

        self._API_VERSION = 0x05

        self._current_state = KnittingState.SETUP
        self._progress = dict(current_row=0,
                              total_rows=0,
                              repeats=0,
                              color="",
                              hall_l=0,
                              hall_r=0,
                              carriage_type="",
                              carriage_position=0)

    def close(self):
        self.__ayabCom.close_serial()

    def get_progress(self):
        return self._progress

    def __get_knit_func(self):
        '''Select function that decides which line of data to send according to the machine type and number of colors'''
        if self._knitting_mode == KnittingMode.SINGLEBED.value and self._numColors == 2:
            self._knit_func = self._singlebed_2col
        elif self._knitting_mode == KnittingMode.CLASSIC_RIBBER_1.value and self._numColors == 2:
            self._knit_func = self._doublebed_2col
        elif self._knitting_mode == KnittingMode.CLASSIC_RIBBER_1.value and self._numColors > 2:
            self._knit_func = self._doublebed_multicol
        elif self._knitting_mode == KnittingMode.MIDDLECOLORSTWICE_RIBBER.value and self._numColors >= 2:
            self._knit_func = self._middlecoltwice
        elif self._knitting_mode == KnittingMode.HEARTOFPLUTO_RIBBER.value and self._numColors >= 2:
            self._knit_func = self._heartofpluto
        elif self._knitting_mode == KnittingMode.CIRCULAR_RIBBER.value: # not restricted to 2 colors
            self._knit_func = self._circular_ribber
        else:
            self.__logger.error("Fallthrough error in __get_knit_func: invalid knitting options")
            return False # knit function not found
        return True

    def _set_bit(self, number: int, position: int) -> int:
        """ Helper to set a bit within an integer number """
        if number < 0:
            raise(ValueError)
        mask = 1 << int(position)
        return (number | mask)

    def _set_pixel(self, line: bytearray, pixel: int):
        """ Helper to set a Pixel within a line """
        numByte = int(pixel / 8)
        line[numByte] = self._set_bit(int(line[numByte]),
                                      pixel - (8 * numByte))
        return

    def __checkSerial(self):
        msg, token, param = self.__ayabCom.update()

        if token == "cnfInfo":
            self.__log_cnfInfo(msg)

        elif token == "indState":
            self.__get_carriage_info(msg)

        return token, param

    def __log_cnfInfo(self, msg):
        api = msg[1]
        log = "API v" + str(api)

        if api >= 5:
            log += ", FW v" + str(msg[2]) + "." + str(msg[3])

        self.__logger.info(log)
        return

    def __get_carriage_info(self, msg):
        hall_l = int((msg[2] << 8) + msg[3])
        hall_r = int((msg[4] << 8) + msg[5])

        if msg[6] == 1:
            carriage_type = "K Carriage"
        elif msg[6] == 2:
            carriage_type = "L Carriage"
        elif msg[6] == 3:
            carriage_type = "G Carriage"
        else:
            carriage_type = ""

        carriage_position = int(msg[7])

        self._progress["hall_l"] = hall_l
        self._progress["hall_r"] = hall_r
        self._progress["carriage_type"] = carriage_type
        self._progress["carriage_position"] = carriage_position
        return

    def __cnfLine(self, lineNumber):
        if lineNumber >= BLOCK_LENGTH:
            self.__logger.error("requested lineNumber out of range")
            return True # stop knitting
        else:
            # TODO some better algorithm for block wrapping
            if self.__formerRequest == BLOCK_LENGTH - 1 and lineNumber == 0:
                # wrap to next block of lines
                self.__lineBlock += 1

            # store requested line number for next request
            self.__formerRequest = lineNumber
            requestedLine = lineNumber

            # adjust lineNumber with current block
            lineNumber += BLOCK_LENGTH * self.__lineBlock

            imgHeight = self._image.imgHeight()
        
            # work out which line of data to send
            imgRow, color, indexToSend, sendBlankLine, lastLine = self._knit_func(lineNumber, imgHeight)
            
            # create bitarray
            bits = self._select_needles(color, indexToSend, sendBlankLine)

            # TODO implement CRC8
            crc8 = 0x00

            # send line to machine
            if self._infRepeat:
                self.__ayabCom.cnf_line(requestedLine, bits.tobytes(), 0, crc8)
            else:
                self.__ayabCom.cnf_line(requestedLine, bits.tobytes(), lastLine, crc8)

            # screen output
            colorNames = "A", "B", "C", "D"
            msg = str(self.__lineBlock)  # Block
            msg += ' ' + str(lineNumber)  # Total Line Number
            msg += ' reqLine: ' + str(requestedLine)
            msg += ' imgRow: ' + str(imgRow)
            msg += ' color: ' + colorNames[color]
            if sendBlankLine is True:
                msg += ' BLANK LINE'
            else:
                msg += ' indexToSend: ' + str(indexToSend)
                msg += ' color: ' + str(color)
                # msg += ' ' + str((self._image.imageExpanded())[indexToSend])
                self._progress["color"] = colorNames[color]
            self.__logger.debug(msg)

            if self._knitting_mode == KnittingMode.SINGLEBED.value:
                self._progress["color"] = ""

            # sending line progress to gui
            self._progress["current_row"] = imgRow + 1
            self._progress["total_rows"] = imgHeight
            self._progress["repeats"] = self.__infRepeat_repeats

        if not lastLine:
            return False # keep knitting
        elif self._infRepeat:
            self.__infRepeat_repeats += 1
            return False # keep knitting
        else:
            return True  # image finished

    def _select_needles(self, color, indexToSend, sendBlankLine):
        bits = bitarray([False] * MACHINE_WIDTH, endian="little")
        firstneedle = max(0, self._image.imgStartNeedle())
        lastneedle = min(self._image.imgWidth() + self._image.imgStartNeedle(), MACHINE_WIDTH)

        if (color == 0 and self._knitting_mode == KnittingMode.CLASSIC_RIBBER_1.value) \
                or (color == self._numColors - 1
                    and (self._knitting_mode == KnittingMode.MIDDLECOLORSTWICE_RIBBER.value
                         or self._knitting_mode == KnittingMode.HEARTOFPLUTO_RIBBER.value)):
            bits[0:firstneedle] = True
            bits[lastneedle:MACHINE_WIDTH] = True

        if not sendBlankLine:
            firstpixel = firstneedle - self._image.imgStartNeedle()
            lastpixel = lastneedle - self._image.imgStartNeedle()
            bits[firstneedle:lastneedle] = (self._image.imageExpanded())[indexToSend][firstpixel:lastpixel]

        return bits
    
    # singlebed, 2 color
    def _singlebed_2col(self, lineNumber, imgHeight):
        lineNumber += self._startLine

        # when knitting infinitely, keep the requested
        # lineNumber in its limits
        if self._infRepeat:
            lineNumber = lineNumber % imgHeight

        imgRow = lineNumber

        # 0   1   2   3   4 .. (imgRow)
        # |   |   |   |   |
        # 0 1 2 3 4 5 6 7 8 .. (imageExpanded)

        # color is always 0 in singlebed,
        # because both colors are knitted at once
        color = 0

        indexToSend = 2 * imgRow

        sendBlankLine = False

        # Check if the last line of the image was requested
        lastLine = (imgRow == imgHeight - 1)

        return imgRow, color, indexToSend, sendBlankLine, lastLine

    # doublebed, 2 color
    def _doublebed_2col(self, lineNumber, imgHeight):
        lenImgExpanded = 2 * imgHeight
        
        lineNumber += 2 * self._startLine

        # calculate line number index for colors
        i = lineNumber % 4

        # when knitting infinitely, keep the requested
        # lineNumber in its limits
        if self._infRepeat:
            lineNumber = lineNumber % lenImgExpanded

        imgRow = lineNumber // 2

        # 0 0 1 1 2 2 3 3 4 4 .. (imgRow)
        # 0 1 2 3 4 5 6 7 8 9 .. (lineNumber)
        # | |  X  | |  X  | |
        # 0 1 3 2 4 5 7 6 8 9 .. (indexToSend)
        # A B B A A B B A A B .. (color)

        color = [0,1,1,0][i] # 0 = A, 1 = B

        indexToSend = (lineNumber + [0,0,1,-1][i]) % lenImgExpanded

        sendBlankLine = False

        lastLine = (imgRow == imgHeight - 1) and (i == 1 or i == 3)

        return imgRow, color, indexToSend, sendBlankLine, lastLine

    # doublebed, multicolor
    def _doublebed_multicol(self, lineNumber, imgHeight):
        lenImgExpanded = self._numColors * imgHeight
        
        # halve lineNumber because every second line is BLANK
        sendBlankLine = odd(lineNumber)
        h = lineNumber // 2

        h += self._numColors * self._startLine

        # when knitting infinitely, keep the
        # half lineNumber within its limits
        if self._infRepeat:
            h = h % lenImgExpanded

        imgRow, color = divmod(h, self._numColors)

        indexToSend = imgRow * self._numColors + color

        lastLine = (indexToSend == lenImgExpanded - 1) and sendBlankLine

        if not sendBlankLine:
            self.__logger.debug("COLOR" + str(color))

        return imgRow, color, indexToSend, sendBlankLine, lastLine

    # Ribber, Middle-Colors-Twice
    def _middlecoltwice(self, lineNumber, imgHeight):

        # doublebed middle-colors-twice multicolor
        # 0-00 1-11 2-22 3-33 4-44 5-55 .. (imgRow)
        # 0123 4567 8911 1111 1111 2222 .. (lineNumber)
        #             01 2345 6789 0123
        #
        # 0-21 4-53 6-87 1-19 1-11 1-11 .. (indexToSend)
        #                0 1  2 43 6 75
        #
        # A-CB B-CA A-CB B-CA A-CB B-CA .. (color)

        # Double the line minus the 2 you save on the begin
        # and end of each imgRow
        passesPerRow = 2 * self._numColors - 2

        lineNumber += passesPerRow * self._startLine

        imgRow, r = divmod(lineNumber, passesPerRow)

        firstCol = (r == 0)
        lastCol = (r == passesPerRow - 1)

        if firstCol or lastCol:
            color = (lastCol + imgRow) % 2
        else:
            color = (r + 3) // 2

        if self._infRepeat:
            imgRow = imgRow % imgHeight

        indexToSend = self._numColors * imgRow + color

        sendBlankLine = not firstCol and not lastCol and odd(lineNumber)

        lastLine = (imgRow == imgHeight - 1) and lastCol

        return imgRow, color, indexToSend, sendBlankLine, lastLine

    # doublebed, multicolor <3 of pluto
    # rotates middle colors
    def _heartofpluto(self, lineNumber, imgHeight):
        
        # doublebed <3 of pluto multicolor
        # 0000 1111 2222 3333 4444 5555 .. (imgRow)
        # 0123 4567 8911 1111 1111 2222 .. (lineNumber)
        #             01 2345 6789 0123
        #
        # 02-1 35-4 76-8 11-9 11-1 11-1 .. (indexToSend)
        #                10   24 3 65 7
        #
        # CB-A AC-B BA-C CB-A AC-B BA-C .. (color)

        # Double the number of colors minus the 2 you save from
        # early advancing to next row
        passesPerRow = 2 * self._numColors - 2

        lineNumber += passesPerRow * self._startLine

        imgRow, r = divmod(lineNumber, passesPerRow)

        if self._infRepeat:
            imgRow = imgRow % imgHeight

        firstCol = (r == 0)
        lastCol = (r == passesPerRow - 1)

        color = self._numColors - 1 - ((lineNumber + 1) % (2 * self._numColors)) // 2

        indexToSend = self._numColors * imgRow + color

        sendBlankLine = not firstCol and not lastCol and even(lineNumber)

        lastLine = (imgRow == imgHeight - 1) and lastCol

        return imgRow, color, indexToSend, sendBlankLine, lastLine

    # Ribber, Circular
    # not restricted to 2 colors
    def _circular_ribber(self, lineNumber, imgHeight):
        lenImgExpanded = self._numColors * imgHeight
        
        # A B  A B  A B  .. (color)
        # 0-0- 1-1- 2-2- .. (imgRow)
        # 0 1  2 3  4 5  .. (indexToSend)
        # 0123 4567 8911 .. (lineNumber)
        #             01

        # halve lineNumber because every second line is BLANK
        sendBlankLine = odd(lineNumber)
        h = lineNumber // 2

        h += self._numColors * self._startLine

        if self._infRepeat:
            h  = h % lenImgExpanded

        imgRow, color = divmod(h, self._numColors)

        indexToSend = h

        lastLine = (indexToSend == lenImgExpanded - 1) and sendBlankLine

        return imgRow, color, indexToSend, sendBlankLine, lastLine

    def knit(self, pImage, pOptions):
        '''Finite State Machine'''
        result = AYABControlKnitResult.NONE

        if self._current_state != KnittingState.SETUP:
            rcvMsg, rcvParam = self.__checkSerial()

        if self._current_state == KnittingState.SETUP:
            self.__formerRequest = 0
            self.__lineBlock = 0
            self._image = pImage
            self._startLine = pImage.startLine()

            self._numColors = pOptions["num_colors"]
            self._knitting_mode = pOptions["knitting_mode"]
            self._infRepeat = pOptions["inf_repeat"]

            self.__infRepeat_repeats = 0

            if not self.__get_knit_func():
                result = AYABControlKnitResult.ERROR_INVALID_SETTINGS
            else:
                if pOptions["portname"] == "Simulation":
                    self.__ayabCom = AyabCommunicationMockup()
                else:
                    self.__ayabCom = AyabCommunication()
 
                if not self.__ayabCom.open_serial(pOptions["portname"]):
                    self.__logger.error("Could not open serial port")
                    result = AYABControlKnitResult.ERROR_SERIAL_PORT
 
                self._current_state = KnittingState.INIT

        elif self._current_state == KnittingState.INIT:
            if rcvMsg == 'cnfInfo':
                if rcvParam == self._API_VERSION:
                    self._current_state = KnittingState.WAIT_FOR_INIT
                    result = AYABControlKnitResult.WAIT_FOR_INIT
                else:
                    self.__logger.error("wrong API version: " +
                                        str(rcvParam) + (" ,expected: ") +
                                        str(self._API_VERSION))
                    result = AYABControlKnitResult.ERROR_WRONG_API
            else:
                self.__ayabCom.req_info()
                result = AYABControlKnitResult.CONNECTING_TO_MACHINE

        elif self._current_state == KnittingState.WAIT_FOR_INIT:
            if rcvMsg == "indState":
                if rcvParam == 1:
                    self.__ayabCom.req_start(self._image.knitStartNeedle(),
                                             self._image.knitStopNeedle(),
                                             pOptions["continuousReporting"])
                    self._current_state = KnittingState.START
                else:
                    self.__logger.debug("init failed")

        elif self._current_state == KnittingState.START:
            if rcvMsg == 'cnfStart':
                if rcvParam == 1:
                    self._current_state = KnittingState.OPERATE
                    result = AYABControlKnitResult.PLEASE_KNIT
                else:
                    self.__logger.error("device not ready")
                    result = AYABControlKnitResult.DEVICE_NOT_READY

        elif self._current_state == KnittingState.OPERATE:
            if rcvMsg == 'reqLine':
                imageFinished = self.__cnfLine(rcvParam)
                if imageFinished:
                    self._current_state = KnittingState.SETUP
                    result = AYABControlKnitResult.FINISHED

        return result
