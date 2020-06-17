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


from .ayab_progress import Progress
from .ayab_communication import AyabCommunication
from .ayab_communication_mockup import AyabCommunicationMockup
from . import ayab_image
import numpy as np
import logging
from PIL import Image
# from time import sleep

from bitarray import bitarray
from enum import Enum

MACHINE_WIDTH = 200
BLOCK_LENGTH = 256
COLOR_SYMBOLS = "A", "B", "C", "D"


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
    CLASSIC_RIBBER = 1  # Classic Ribber
    # CLASSIC_RIBBER_2 = 2            # Classic Ribber 2
    MIDDLECOLORSTWICE_RIBBER = 2  # Middle-Colors-Twice Ribber
    HEARTOFPLUTO_RIBBER = 3  # Heart-of-Pluto Ribber
    CIRCULAR_RIBBER = 4  # Circular Ribber

    def row_multiplier(self, ncolors):
        if self.name == "SINGLEBED":
            return 1
        elif (self.name == "CLASSIC_RIBBER" and ncolors > 2) \
            or self.name == "CIRCULAR_RIBBER":
            # every second line is blank
            return 2 * ncolors
        elif self.name == "MIDDLECOLORSTWICE_RIBBER" \
            or self.name == "HEARTOFPLUTO_RIBBER":
            # only middle lines doubled
            return 2 * ncolors - 2
        else:
            # one line per color
            return ncolors

    def good_ncolors(self, ncolors):
        if self.name == "SINGLEBED" or self.name == "CIRCULAR_RIBBER":
            return ncolors == 2
        else:
            # no maximum
            return ncolors >= 2

    def knit_func(self, ncolors):
        method = "_" + self.name.lower()
        if self.name == "CLASSIC_RIBBER":
            method += ["2col", "multicol"][ncolors > 2]
        return method

    def flanking_needles(self, color, ncolors):
        return (color == 0 and self.name == "CLASSIC_RIBBER") \
            or (color == ncolors - 1
                and (self.name == "MIDDLECOLORSTWICE_RIBBER"
                    or self.name == "HEARTOFPLUTO_RIBBER"))


class KnitRow:

    def __init__(self, ayab_control):
        self.ayab_control = ayab_control
        self.carriage = ""
        self.swipe = 0
        self.dir = 0
        self.symbol = 0
        self.lineNumber = -1
        self.lineBlock = 0

    def get_row(self, lineNumber):
        self.lineNumber = lineNumber
        self.imgRow, self.color, self.indexToSend, self.sendBlankLine, self.lastLine = self.ayab_control._knit_func(lineNumber)
        self.bits = self.ayab_control._choose_needles(self.color, self.indexToSend, self.sendBlankLine)



def even(x):
    return x % 2 == 0

def odd(x):
    return x % 2 == 1


class AYABControl(object):

    def __init__(self):
        self.__logger = logging.getLogger(type(self).__name__)
        self.__API_VERSION = 0x05
        self.__ayabCom = AyabCommunication()
        self.__current_state = KnittingState.SETUP
        self.__progress = Progress()

    def close(self):
        self.__ayabCom.close_serial()

    def get_row_multiplier(self):
        return KnittingMode(self.__knitting_mode).row_multiplier(self.__numColors)

    def get_progress(self):
        return self.__progress

    def setImage(self, im: Image):
        self.__image = im

    def setKnittingMode(self, mode: int):
        self.__knitting_mode = mode

    def setNumColors(self, n: int):
        self.__numColors = n

    def setStartLine(self, n: int):
        self.__startLine = n

    def setInfRepeat(self, x: bool):
        self.__infRepeat = x

    def __get_knit_func(self):
        '''Select function that decides which line of data to send according to the machine type and number of colors'''
        if not self.__knitting_mode.good_ncolors(self.__numColors):
            self.__logger.error("Wrong number of colours for the knitting mode")
            return False
        # else
        func_name = self.__knitting_mode.knit_func(self.__numColors)
        if not hasattr(AYABControl, func_name):
            return False
        # else
        self.__knit_func = getattr(AYABControl, func_name)
        return True

    def _checkSerial(self):
        msg, token, param = self.__ayabCom.update()
        if token == "cnfInfo":
            self.__log_cnfInfo(msg)
        elif token == "indState":
            self.__progress.get_carriage_info(msg)
        return token, param

    def __log_cnfInfo(self, msg):
        api = msg[1]
        log = f"API v{api}"
        if api >= 5:
            log += ", FW v{msg[2]}.{msg[3]}"
        self.__logger.info(log)
        return

    def __cnfLine(self, lineNumber):
        if lineNumber < BLOCK_LENGTH:
            # TODO some better algorithm for block wrapping
            if self.__formerRequest == BLOCK_LENGTH - 1 and lineNumber == 0:
                # wrap to next block of lines
                self.__lineBlock += 1

            # store requested line number for next request
            self.__formerRequest = lineNumber
            requestedLine = lineNumber

            # adjust lineNumber with current block
            lineNumber += BLOCK_LENGTH * self.__lineBlock

            # get data for next line of knitting
            imgRow, color, indexToSend, sendBlankLine, lastLine = self.__knit_func(lineNumber)
            bits = self._select_needles(color, indexToSend, sendBlankLine)

            # send line to machine
            self.__ayabCom.cnf_line(requestedLine, bits.tobytes(), lastLine & self.__infRepeat)

            # screen output
            msg = f"{self.__lineBlock} {lineNumber} reqLine: {requestedLine} imgRow: {imgRow}"
            if sendBlankLine:
                msg += ' BLANK LINE'
            else:
                msg += f" indexToSend: {indexToSend} color: {COLOR_SYMBOLS[color]}"
            self.__logger.debug(msg)

            # get line progress to send to GUI
            self.__get_progress(imgRow, lineNumber, color, bits)

        else:
            self.__logger.error("Requested line number out of range")
            return True # stop knitting

        if not lastLine:
            return False # keep knitting
        elif self.__infRepeat:
            self.__infRepeat_repeats += 1
            return False # keep knitting
        else:
            return True  # image finished

    def __get_progress(self, imgRow, lineNumber, color, bits):
        self.__progress.current_row = imgRow + 1
        self.__progress.total_rows = self.__image.imgHeight()
        self.__progress.lineNumber = lineNumber
        if self.__infRepeat:
            self.progress.repeats = self.__infRepeat_repeats
        if self.__knitting_mode == KnittingMode.SINGLEBED.value:
            self.__progress.alt_color = self.__image.palette[1]
            self.__progress.colorSymbol = "A/B"
        else:
            self.__progress.alt_color = None
            self.__progress.colorSymbol = COLOR_SYMBOLS[color]
        self.__progress.color = self.__image.palette[color]
        self.__progress.bits = bits[self.__firstneedle:self.__lastneedle]

    def _select_needles(self, color, indexToSend, sendBlankLine):
        bits = bitarray([False] * MACHINE_WIDTH, endian="little")
        firstneedle = max(0, self.__image.imgStartNeedle())
        lastneedle = min(self.__image.imgWidth() + self.__image.imgStartNeedle(), MACHINE_WIDTH)

        if KnittingMode(self.__knitting_mode).flanking_needles(color, self.__numColors):
            bits[0:firstneedle] = True
            bits[lastneedle:MACHINE_WIDTH] = True

        if not sendBlankLine:
            firstpixel = firstneedle - self.__image.imgStartNeedle()
            lastpixel = lastneedle - self.__image.imgStartNeedle()
            bits[firstneedle:lastneedle] = (self.__image.imageExpanded())[indexToSend][firstpixel:lastpixel]

        self.__firstneedle = firstneedle
        self.__lastneedle = lastneedle
        return bits
    
    # singlebed, 2 color
    def _singlebed(self, lineNumber):
        imgHeight = self.__image.imgHeight()
        lineNumber += self.__startLine

        # when knitting infinitely, keep the requested
        # lineNumber in its limits
        if self.__infRepeat:
            lineNumber = lineNumber % imgHeight
        imgRow = lineNumber

        # 0   1   2   3   4 .. (imgRow)
        # |   |   |   |   |
        # 0 1 2 3 4 5 6 7 8 .. (indexToSend)

        # color is always 0 in singlebed,
        # because both colors are knitted at once
        color = 0

        indexToSend = 2 * imgRow

        sendBlankLine = False

        # Check if the last line of the image was requested
        lastLine = (imgRow == imgHeight - 1)

        return imgRow, color, indexToSend, sendBlankLine, lastLine

    # doublebed, 2 color
    def _classic_ribber_2col(self, lineNumber):
        imgHeight = self.__image.imgHeight()
        lenImgExpanded = 2 * imgHeight
        
        lineNumber += 2 * self.__startLine

        # calculate line number index for colors
        i = lineNumber % 4

        # when knitting infinitely, keep the requested
        # lineNumber in its limits
        if self.__infRepeat:
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
    def _classic_ribber_multicol(self, lineNumber):
        lenImgExpanded = self.__numColors * self.__image.imgHeight()
        
        # halve lineNumber because every second line is BLANK
        sendBlankLine = odd(lineNumber)
        h = lineNumber // 2

        h += self.__numColors * self.__startLine

        # when knitting infinitely, keep the
        # half lineNumber within its limits
        if self.__infRepeat:
            h = h % lenImgExpanded

        imgRow, color = divmod(h, self.__numColors)

        indexToSend = imgRow * self.__numColors + color

        lastLine = (indexToSend == lenImgExpanded - 1) and sendBlankLine

        if not sendBlankLine:
            self.__logger.debug("COLOR" + str(color))

        return imgRow, color, indexToSend, sendBlankLine, lastLine

    # Ribber, Middle-Colors-Twice
    def _middlecolorstwice_ribber(self, lineNumber):
        imgHeight = self.__image.imgHeight()

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
        passesPerRow = 2 * self.__numColors - 2

        lineNumber += passesPerRow * self.__startLine

        imgRow, r = divmod(lineNumber, passesPerRow)

        firstCol = (r == 0)
        lastCol = (r == passesPerRow - 1)

        if firstCol or lastCol:
            color = (lastCol + imgRow) % 2
        else:
            color = (r + 3) // 2

        if self.__infRepeat:
            imgRow = imgRow % imgHeight

        indexToSend = self.__numColors * imgRow + color

        sendBlankLine = not firstCol and not lastCol and odd(lineNumber)

        lastLine = (imgRow == imgHeight - 1) and lastCol

        return imgRow, color, indexToSend, sendBlankLine, lastLine

    # doublebed, multicolor <3 of pluto
    # rotates middle colors
    def _heartofpluto_ribber(self, lineNumber):
        imgHeight = self.__image.imgHeight()
        
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
        passesPerRow = 2 * self.__numColors - 2

        lineNumber += passesPerRow * self.__startLine

        imgRow, r = divmod(lineNumber, passesPerRow)

        if self.__infRepeat:
            imgRow = imgRow % imgHeight

        firstCol = (r == 0)
        lastCol = (r == passesPerRow - 1)

        color = self.__numColors - 1 - ((lineNumber + 1) % (2 * self.__numColors)) // 2

        indexToSend = self.__numColors * imgRow + color

        sendBlankLine = not firstCol and not lastCol and even(lineNumber)

        lastLine = (imgRow == imgHeight - 1) and lastCol

        return imgRow, color, indexToSend, sendBlankLine, lastLine

    # Ribber, Circular
    # not restricted to 2 colors
    def _circular_ribber(self, lineNumber):
        lenImgExpanded = self.__numColors * self.__image.imgHeight()
        
        # A B  A B  A B  .. (color)
        # 0-0- 1-1- 2-2- .. (imgRow)
        # 0 1  2 3  4 5  .. (indexToSend)
        # 0123 4567 8911 .. (lineNumber)
        #             01

        # halve lineNumber because every second line is BLANK
        sendBlankLine = odd(lineNumber)
        h = lineNumber // 2

        h += self.__numColors * self.__startLine

        if self.__infRepeat:
            h  = h % lenImgExpanded

        imgRow, color = divmod(h, self.__numColors)

        indexToSend = h

        lastLine = (indexToSend == lenImgExpanded - 1) and sendBlankLine

        return imgRow, color, indexToSend, sendBlankLine, lastLine

    def knit(self, pImage, pOptions):
        '''Finite State Machine'''
        result = AYABControlKnitResult.NONE

        if self.__current_state != KnittingState.SETUP:
            rcvMsg, rcvParam = self._checkSerial()

        if self.__current_state == KnittingState.SETUP:
            self.__formerRequest = 0
            self.__lineBlock = 0
            self.__image = pImage
            self.__startLine = pImage.startLine()
            self.__numColors = pOptions["num_colors"]
            self.__knitting_mode = pOptions["knitting_mode"]
            self.__infRepeat = pOptions["inf_repeat"]
            self.__infRepeat_repeats = 0
            self.__progress.reset()

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
 
                self.__current_state = KnittingState.INIT

        elif self.__current_state == KnittingState.INIT:
            if rcvMsg == 'cnfInfo':
                if rcvParam == self.__API_VERSION:
                    self.__current_state = KnittingState.WAIT_FOR_INIT
                    result = AYABControlKnitResult.WAIT_FOR_INIT
                else:
                    self.__logger.error("wrong API version: " +
                                        str(rcvParam) + (" ,expected: ") +
                                        str(self.__API_VERSION))
                    result = AYABControlKnitResult.ERROR_WRONG_API
            else:
                self.__ayabCom.req_info()
                result = AYABControlKnitResult.CONNECTING_TO_MACHINE

        elif self.__current_state == KnittingState.WAIT_FOR_INIT:
            if rcvMsg == "indState":
                if rcvParam == 1:
                    self.__ayabCom.req_start(self.__image.knitStartNeedle(),
                                             self.__image.knitStopNeedle(),
                                             pOptions["continuousReporting"])
                    self.__current_state = KnittingState.START
                else:
                    self.__logger.debug("init failed")

        elif self.__current_state == KnittingState.START:
            if rcvMsg == 'cnfStart':
                if rcvParam == 1:
                    self.__current_state = KnittingState.OPERATE
                    result = AYABControlKnitResult.PLEASE_KNIT
                else:
                    self.__logger.error("device not ready")
                    result = AYABControlKnitResult.DEVICE_NOT_READY

        elif self.__current_state == KnittingState.OPERATE:
            if rcvMsg == 'reqLine':
                imageFinished = self.__cnfLine(rcvParam)
                if imageFinished:
                    self.__current_state = KnittingState.SETUP
                    result = AYABControlKnitResult.FINISHED

        return result
