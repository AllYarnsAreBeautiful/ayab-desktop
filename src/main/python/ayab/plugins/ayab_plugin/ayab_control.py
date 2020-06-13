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
import pprint
from bitarray import bitarray

from enum import Enum

MACHINE_WIDTH = 200

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
        if self.__knitting_mode == KnittingMode.SINGLEBED.value and self.__numColors == 2:
            self.__knit_func = self.__singlebed_2col
        elif self.__knitting_mode == KnittingMode.CLASSIC_RIBBER_1.value and self.__numColors == 2:
            self.__knit_func = self.__doublebed_2col
        elif self.__knitting_mode == KnittingMode.CLASSIC_RIBBER_1.value and self.__numColors > 2:
            self.__knit_func = self.__doublebed_multicol
        elif self.__knitting_mode == KnittingMode.MIDDLECOLORSTWICE_RIBBER.value:
            self.__knit_func = self.__middlecoltwice
        elif self.__knitting_mode == KnittingMode.HEARTOFPLUTO_RIBBER.value and self.__numColors >= 2:
            self.__knit_func = self.__heartofpluto
        elif self.__knitting_mode == KnittingMode.CIRCULAR_RIBBER.value and self.__numColors == 2:
            self.__knit_func = self.__circular_ribber
        else:
            self.__logger.error("Fallthrough error in __cnfLine: knitting mode not recognized.")
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
        imgHeight = self.__image.imgHeight()
        lenImgExpanded = len(self.__image.imageExpanded())

        # initialize bitarray to 0x00
        bits = bitarray([False] * MACHINE_WIDTH, endian="little")

        if lineNumber < 256:
            # TODO some better algorithm for block wrapping
            # if the last requested line number was 255, wrap to next block of
            # lines
            if self.__formerRequest == 255 and lineNumber == 0:
                self.__lineBlock += 1

            # store requested line number for next request
            self.__formerRequest = lineNumber
            requestedLine = lineNumber

            # adjust lineNumber with current block
            lineNumber = lineNumber + 256 * self.__lineBlock

            # work out which line of data to send
            color, imgRow, indexToSend, sendBlankLine, lastLine = self.__knit_func(lineNumber, imgHeight, lenImgExpanded)

            # assign pixeldata
            imgStartNeedle = self.__image.imgStartNeedle()
            if imgStartNeedle < 0:
                imgStartNeedle = 0

            imgStopNeedle = self.__image.imgStopNeedle()
            if imgStopNeedle > MACHINE_WIDTH - 1:
                imgStopNeedle = MACHINE_WIDTH - 1

            # set the bitarray
            if (color == 0 and self.__knitting_mode == KnittingMode.CLASSIC_RIBBER_1.value) \
                    or (color == self.__numColors - 1
                        and (self.__knitting_mode == KnittingMode.MIDDLECOLORSTWICE_RIBBER.value
                             or self.__knitting_mode == KnittingMode.HEARTOFPLUTO_RIBBER.value)):

                for col in range(0, MACHINE_WIDTH):
                    if col < imgStartNeedle \
                            or col > imgStopNeedle:
                        bits[col] = True

            for col in range(0, self.__image.imgWidth()):
                pxl = (self.__image.imageExpanded())[indexToSend][col]
                # take the image offset into account
                if pxl == 1 and sendBlankLine is False:
                    pxlNumber = col + self.__image.imgStartNeedle()
                    # TODO implement for generic machine width
                    if 0 <= pxlNumber and pxlNumber < MACHINE_WIDTH:
                        bits[pxlNumber] = True

            # TODO implement CRC8
            crc8 = 0x00

            # send line to machine
            if self.__infRepeat:
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
                # msg += ' ' + str((self.__image.imageExpanded())[indexToSend])
            self.__logger.debug(msg)

            if self.__knitting_mode == KnittingMode.SINGLEBED.value:
                self._progress["color"] = ""
                pass
            elif sendBlankLine is True:
                pass
            else:
                self._progress["color"] = colorNames[color]
                pass

            # sending line progress to gui
            self._progress["current_row"] = imgRow + 1
            self._progress["total_rows"] = imgHeight
            self._progress["repeats"] = self.__infRepeat_repeats

        else:
            self.__logger.error("requested lineNumber out of range")

        if lastLine:
            if self.__infRepeat:
                self.__infRepeat_repeats += 1
                return False # keep knitting
            else:
                return True  # image finished
        else:
            return False     # keep knitting

    # singlebed, 2 color
    def __singlebed_2col(self, lineNumber, imgHeight, lenImgExpanded):

        # when knitting infinitely, keep the requested
        # lineNumber in its limits
        if self.__infRepeat:
            lineNumber = lineNumber % imgHeight

        # color is always 0 in singlebed,
        # because both colors are knitted at once
        color = 0

        # calculate imgRow
        imgRow = (self.__startLine + lineNumber) % imgHeight

        # 0   1   2   3   4 .. (imgRow)
        # |   |   |   |   |
        # 0 1 2 3 4 5 6 7 8 .. (imageExpanded)
        indexToSend = 2 * imgRow

        # Check if the last line of the image was requested
        lastLine = (imgRow == imgHeight - 1)

        sendBlankLine = False
        return color, imgRow, indexToSend, sendBlankLine, lastLine

    # doublebed, 2 color
    def __doublebed_2col(self, lineNumber, imgHeight, lenImgExpanded):

        # when knitting infinitely, keep the requested
        # lineNumber in its limits
        if self.__infRepeat:
            lineNumber = lineNumber % lenImgExpanded

        # calculate imgRow
        imgRow = (self.__startLine + lineNumber // 2) % imgHeight

        # 0 0 1 1 2 2 3 3 4 4 .. (imgRow)
        # 0 1 2 3 4 5 6 7 8 9 .. (lineNumber)
        # | |  X  | |  X  | |
        # 0 1 3 2 4 5 7 6 8 9 .. (imageExpanded)
        # A B B A A B B A A B .. (color)

        i = lineNumber % 4
        color = [0,1,1,0][i] # 0 = A, 1 = B

        indexToSend = (2 * self.__startLine + lineNumber + [0,0,1,-1][i]) % lenImgExpanded

        lastLine = (imgRow == imgHeight - 1) and (lineNumber % 4 == 1 or lineNumber % 4 == 3)

        sendBlankLine = False
        return color, imgRow, indexToSend, sendBlankLine, lastLine

    # doublebed, multicolor
    def __doublebed_multicol(self, lineNumber, imgHeight, lenImgExpanded):

        # when knitting infinitely, keep the requested
        # lineNumber in its limits
        if self.__infRepeat:
            # *2 because of BLANK lines in between
            lineNumber = lineNumber % (2 * lenImgExpanded)

        # calculate imgRow
        imgRow = (self.__startLine + lineNumber // (2 * self.__numColors)) % imgHeight

        color = (lineNumber // 2) % self.__numColors

        # indexToSend = self.__startLine * self.__numColors
        indexToSend = (color + imgRow * self.__numColors) % lenImgExpanded

        if lineNumber % 2 == 1:
            sendBlankLine = True
        else:
            sendBlankLine = False
            self.__logger.debug("COLOR" + str(color))

        lastLine = (indexToSend == lenImgExpanded - 1) and (sendBlankLine is True)

        return color, imgRow, indexToSend, sendBlankLine, lastLine

    # Ribber, Middle-Colors-Twice
    def __middlecoltwice(self, lineNumber, imgHeight, lenImgExpanded):

        # doublebed middle-colors-twice multicolor
        # 0-00 1-11 2-22 3-33 4-44 5-55 .. (imgRow)
        # 0123 4567 8911 1111 1111 2222.. (lineNumber)
        #             01 2345 6789 0123
        #
        # 0-21 4-53 6-87 1-19 1-11 1-11 .. (imageExpanded)
        #                0 1  2 43 6 75
        #
        # A-CB B-CA A-CB B-CA A-CB B-CA .. (color)

        # Double the line minus the 2 you save on the begin
        # and end of each imgRow
        passesPerRow = 2 * self.__numColors - 2

        imgRow = self.__startLine + lineNumber // passesPerRow

        if self.__infRepeat:
            imgRow = imgRow % imgHeight

        if imgRow % 2 != 0:
            color = ((lineNumber % passesPerRow) + 1) // 2
        else:
            color = (passesPerRow - (lineNumber % passesPerRow)) // 2

        indexToSend = imgRow * self.__numColors + color

        sendBlankLine = not (lineNumber % passesPerRow == 0) and not ((lineNumber + 1) % passesPerRow == 0) and not (lineNumber % 2 == 0)

        lastLine = (imgRow == imgHeight - 1) and (lineNumber % passesPerRow == passesPerRow - 1)

        return color, imgRow, indexToSend, sendBlankLine, lastLine

    # doublebed, multicolor <3 of pluto
    # advances imgRow as soon as possible
    def __heartofpluto(self, lineNumber, imgHeight, lenImgExpanded):

        # Double the line minus the 2 you save from
        # early advancing to next row
        passesPerRow = 2 * self.__numColors - 2

        imgRow = self.__startLine + lineNumber // passesPerRow

        if self.__infRepeat:
            imgRow = imgRow % imgHeight

        indexToSend = imgRow * self.__numColors

        # check if it's time to send a blank line
        if lineNumber % passesPerRow != 0 and lineNumber % 2 == 0:
            color = 0
            sendBlankLine = True
        else:
            # if not set a color
            color = self.__numColors - 1 - ((lineNumber + 1) % (self.__numColors * 2)) // 2
            # use color to adjust index
            indexToSend += color
            sendBlankLine = False

        lastLine = (imgRow == imgHeight - 1) and (lineNumber % passesPerRow == passesPerRow - 1)

        return color, imgRow, indexToSend, sendBlankLine, lastLine

    # Ribber, Circular
    def __circular_ribber(self, lineNumber, imgHeight, lenImgExpanded):

        # when knitting infinitely, keep the requested
        # lineNumber in its limits
        if self.__infRepeat:
            # *2 because of BLANK lines in between
            lineNumber = lineNumber % (2 * lenImgExpanded)

        color = 0

        imgRow = (self.__startLine + lineNumber // 4) % imgHeight

        # Color      A B  A B  A B
        # ImgRow     0-0- 1-1- 2-2-
        # Index2Send 0 1  2 3  4 5
        # LineNumber 0123 4567 8911
        #                        01

        indexToSend = (self.__startLine * self.__numColors + lineNumber // 2) % lenImgExpanded

        sendBlankLine = (lineNumber % 2 == 1)

        lastLine = (indexToSend == lenImgExpanded - 1) and (sendBlankLine is True)

        return color, imgRow, indexToSend, sendBlankLine, lastLine

    def knit(self, pImage, pOptions):
        '''Finite State Machine'''
        result = AYABControlKnitResult.NONE

        if self._current_state != KnittingState.SETUP:
            rcvMsg, rcvParam = self.__checkSerial()

        if self._current_state == KnittingState.SETUP:
            self.__formerRequest = 0
            self.__lineBlock = 0
            self.__image = pImage
            self.__startLine = pImage.startLine()

            self.__numColors = pOptions["num_colors"]
            self.__knitting_mode = pOptions["knitting_mode"]
            self.__infRepeat = pOptions["inf_repeat"]

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
                    self.__ayabCom.req_start(self.__image.knitStartNeedle(),
                                             self.__image.knitStopNeedle(),
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
