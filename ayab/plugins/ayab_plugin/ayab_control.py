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
#    Copyright 2013, 2014 Sebastian Oliva, Christian Obersteiner, Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

from .ayab_communication import AyabCommunication
from . import ayab_image
import time
import logging
import os
import sys
from ayab.plugins.knitting_plugin import KnittingPlugin
from PyQt5 import QtGui, QtWidgets, QtCore

from .ayab_options import Ui_DockWidget
import serial.tools.list_ports

import pprint

class AyabPluginControl(KnittingPlugin):

  def onknit(self, e):
    logging.debug("called onknit on AyabPluginControl")
    self.__knitImage(self.__image, self.conf)
    self.finish()

  def onconfigure(self, e):
    logging.debug("called onconfigure on AYAB Knitting Plugin")
    #print ', '.join("%s: %s" % item for item in vars(e).items())
    #FIXME: substitute setting parent_ui from self.__parent_ui
    #self.__parent_ui = e.event.parent_ui
    parent_ui = self.__parent_ui

    #Start to knit with the bottom first
    pil_image = parent_ui.pil_image.rotate(180)

    conf = self.get_configuration_from_ui(parent_ui)
    #TODO: detect if previous conf had the same image to avoid re-generating.

    try:
        self.__image = ayab_image.ayabImage(pil_image, self.conf["num_colors"])
    except:
        self.__notify_user("You need to set an image.", "error")
        return

    if self.validate_configuration(conf):
        parent_ui.ui.widget_knitcontrol.setEnabled(True)
        parent_ui.ui.knit_button.setEnabled(True)

        if conf.get("start_needle") and conf.get("stop_needle"):
            self.__image.setKnitNeedles(conf.get("start_needle"),
                                        conf.get("stop_needle"))
        if conf.get("alignment"):
            self.__image.setImagePosition(conf.get("alignment"))
        if conf.get("start_line"):
            self.__image.setStartLine(conf.get("start_line"))
            self.__emit_progress(conf.get("start_line")+1,
                                 self.__image.imgHeight())
    else:
        parent_ui.ui.widget_knitcontrol.setEnabled(False)
        parent_ui.ui.knit_button.setEnabled(False)

    return

  def validate_configuration(self, conf):
    if conf.get("start_needle") and conf.get("stop_needle"):
      if conf.get("start_needle") > conf.get("stop_needle"):
        self.__notify_user("Invalid needle start and end.", "warning")
        return False
    if conf.get("start_line") > self.__image.imgHeight():
      self.__notify_user("Start Line is larger than the image.")
      return False

    if conf.get("portname") == '':
      self.__notify_user("Please choose a valid port.")
      return False

    if conf.get("machine_type") == 'single' \
            and conf.get("num_colors") >= 3:
        self.__notify_user("Single bed knitting currently supports only 2 colors", "warning")
        return False

    if conf.get("machine_type") == 'circular' \
            and conf.get("num_colors") >= 3:
        self.__notify_user("Circular knitting supports only 2 colors", "warning")
        return False

    return True

  def onfinish(self, e):
    logging.info("Finished Knitting.")
    self.__close_serial()
    self.__parent_ui.resetUI()
    self.__parent_ui.signalUpdateProgress.emit(0, 0)

  def cancel(self):
    self.__updateNotification("Knitting cancelled")
    self._knitImage = False

  def __close_serial(self):
    self.__ayabCom.close_serial()

  def onerror(self, e):
    #TODO add message info from event
    logging.error("Error while Knitting.")
    self.__close_serial()

  def __wait_for_user_action(self, message="", message_type="info"):
    """Sends the display_blocking_pop_up_signal QtSignal to main GUI thread, blocking it."""
    self.__parent_ui.signalDisplayBlockingPopUp.emit(message, message_type)

  def __notify_user(self, message="", message_type="info"):
    """Sends the display_pop_up_signal QtSignal to main GUI thread, not blocking it."""
    self.__parent_ui.signalDisplayPopUp.emit(message, message_type)

  def __updateNotification(self, message=""):
    """Sends the signalUpdateNotification signal"""
    self.__parent_ui.signalUpdateNotification.emit(message)

  def __emit_progress(self, row, total = 0):
    """Sends the updateProgress QtSignal."""
    self.__parent_ui.signalUpdateProgress.emit(int(row), int(total))

  def __emit_needles(self):
    """Sends the updateNeedles QtSignal."""

    start_needle_text = self.options_ui.start_needle_edit.value()
    start_needle_color = self.options_ui.start_needle_color.currentText()
    start_needle = self.readNeedleSettings(
        start_needle_color,
        start_needle_text)

    stop_needle_text = self.options_ui.stop_needle_edit.value()
    stop_needle_color = self.options_ui.stop_needle_color.currentText()
    stop_needle = self.readNeedleSettings(
        stop_needle_color,
        stop_needle_text)

    self.__parent_ui.signalUpdateNeedles.emit(start_needle, stop_needle)

  def __emit_alignment(self):
    """Sends the updateAlignment QtSignal"""
    alignment_text = self.options_ui.alignment_combo_box.currentText()
    self.__parent_ui.signalUpdateAlignment.emit(alignment_text)

  def slotSetImageDimensions(self, width, height):
    """Called by Main UI on loading of an image to set Start/Stop needle
    to image width. Updates the maximum value of the Start Line UI element"""
    right_side = int(width/2)
    self.options_ui.start_needle_edit.setValue(width - right_side)
    self.options_ui.stop_needle_edit.setValue(right_side)
    self.options_ui.start_line_edit.setMaximum(height)

  def __onStartLineChanged(self):
    """ """
    start_line_edit = self.options_ui.start_line_edit.value()
    self.__emit_progress(start_line_edit, 0)

  def setup_ui(self, parent_ui):
    """Sets up UI elements from ayab_options.Ui_DockWidget in parent_ui."""
    self.set_translator()
    self.__parent_ui = parent_ui
    self.options_ui = Ui_DockWidget()
    self.dock = parent_ui.ui.knitting_options_dock  # findChild(QtGui.QDockWidget, "knitting_options_dock")
    self.options_ui.setupUi(self.dock)
    self.setup_behaviour_ui()

  def set_translator(self):
    dirname = os.path.dirname(__file__)
    self.translator = QtCore.QTranslator()
    self.translator.load(QtCore.QLocale.system(), "ayab_options", ".", dirname, ".qm")
    app = QtCore.QCoreApplication.instance()
    app.installTranslator(self.translator)

  def unset_translator(self):
    app = QtCore.QCoreApplication.instance()
    app.removeTranslator(self.translator)

  def populate_ports(self, combo_box=None, port_list=None):
    if not combo_box:
        combo_box = self.__parent_ui.findChild(QtWidgets.QComboBox,
                                               "serial_port_dropdown")
    if not port_list:
        port_list = self.getSerialPorts()

    combo_box.clear()

    def populate(combo_box, port_list):
        for item in port_list:
          #TODO: should display the info of the device.
          combo_box.addItem(item[0])
    populate(combo_box, port_list)


  def setup_behaviour_ui(self):
    """Connects methods to UI elements."""
    conf_button = self.options_ui.configure_button  # Used instead of findChild(QtGui.QPushButton, "configure_button")
    conf_button.clicked.connect(self.conf_button_function)

    self.populate_ports()
    refresh_ports = self.options_ui.refresh_ports_button
    refresh_ports.clicked.connect(self.populate_ports)

    start_needle_edit = self.options_ui.start_needle_edit
    start_needle_edit.valueChanged.connect(self.__emit_needles)
    stop_needle_edit = self.options_ui.stop_needle_edit
    stop_needle_edit.valueChanged.connect(self.__emit_needles)

    start_needle_color = self.options_ui.start_needle_color
    start_needle_color.currentIndexChanged.connect(self.__emit_needles)
    stop_needle_color = self.options_ui.stop_needle_color
    stop_needle_color.currentIndexChanged.connect(self.__emit_needles)

    alignment_combo_box = self.options_ui.alignment_combo_box
    alignment_combo_box.currentIndexChanged.connect(self.__emit_alignment)

    start_line_edit = self.options_ui.start_line_edit
    start_line_edit.valueChanged.connect(self.__onStartLineChanged)

  def conf_button_function(self):
    self.configure()

  def cleanup_ui(self, parent_ui):
    """Cleans up UI elements inside knitting option dock."""
    #dock = parent_ui.knitting_options_dock
    dock = self.dock
    cleaner = QtCore.QObjectCleanupHandler()
    cleaner.add(dock.widget())
    self.__qw = QtGui.QWidget()
    dock.setWidget(self.__qw)
    self.unset_translator()

  def readNeedleSettings(self, color, needle):
    '''Reads the Needle Settings UI Elements and normalizes'''
    if(color == "orange"):
        return 100 - int(needle)
    elif(color == "green"):
        return 99 + int(needle)

  def get_configuration_from_ui(self, ui):
    """Creates a configuration dict from the ui elements.

    Returns:
      dict: A dict with configuration.

    """

    self.conf = {}
    tab_widget = ui.findChild(QtWidgets.QTabWidget, "tabWidget")
    if tab_widget.currentIndex() == 1:
        self.conf["testmode"] = True
    else:
        self.conf["testmode"] = False

    color_line_text = ui.findChild(QtWidgets.QSpinBox, "color_edit").value()
    self.conf["num_colors"] = int(color_line_text)

    # Internally, we start counting from zero (for easier handling of arrays)
    start_line_text = ui.findChild(QtWidgets.QSpinBox, "start_line_edit").value()
    self.conf["start_line"] = int(start_line_text) - 1

    start_needle_color = ui.findChild(QtWidgets.QComboBox, "start_needle_color").currentText()
    start_needle_text = ui.findChild(QtWidgets.QSpinBox, "start_needle_edit").value()

    self.conf["start_needle"] = self.readNeedleSettings(
        start_needle_color,
        start_needle_text)

    stop_needle_color = ui.findChild(QtWidgets.QComboBox, "stop_needle_color").currentText()
    stop_needle_text = ui.findChild(QtWidgets.QSpinBox, "stop_needle_edit").value()

    self.conf["stop_needle"] = self.readNeedleSettings(
        stop_needle_color,
        stop_needle_text)

    alignment_text = ui.findChild(QtWidgets.QComboBox, "alignment_combo_box").currentText()
    self.conf["alignment"] = alignment_text

    self.conf["inf_repeat"] = \
        int(ui.findChild(QtWidgets.QCheckBox, "infRepeat_checkbox").isChecked())

    machine_type_text = ui.findChild(QtWidgets.QComboBox, "machine_type_box").currentText()
    self.conf["machine_type"] = str(machine_type_text)

    serial_port_text = ui.findChild(QtWidgets.QComboBox, "serial_port_dropdown").currentText()
    self.conf["portname"] = str(serial_port_text)

    # getting file location from textbox
    filename_text = ui.findChild(QtWidgets.QLineEdit, "filename_lineedit").text()
    self.conf["filename"] = str(filename_text)

    logging.debug(self.conf)
    ## Add more config options.
    return self.conf

  def getSerialPorts(self):
        """
        Returns a list of all USB Serial Ports
        """
        return list(serial.tools.list_ports.grep("USB"))

  def __init__(self):
    super(AyabPluginControl, self).__init__({})
    # KnittingPlugin.__init__(self)

    #Copying from ayab_control
    self.__API_VERSION = 0x04
    self.__ayabCom = AyabCommunication()

    self.__formerRequest = 0
    self.__lineBlock = 0

  def __del__(self):
    self.__close_serial()

###Copied from ayab_control
#####################################

  def __setBit(self, int_type, offset):
      mask = 1 << int(offset)
      return(int_type | mask)

  def __setPixel(self, bytearray_, pixel):
      numByte = int(pixel / 8)
      bytearray_[numByte] = self.__setBit(
          int(bytearray_[numByte]), pixel - (8 * numByte))
      return bytearray_

  def __checkSerial(self):
        time.sleep(1)  # TODO if problems in communication, tweak here

        line = self.__ayabCom.read_line()

        if len(line) > 0:
            msgId = line[0]
            if msgId == 0xC1:    # cnfStart
                # print "> cnfStart: " + str(ord(line[1]))
                return ("cnfStart", line[1])

            elif msgId == 0xC3:  # cnfInfo
                # print "> cnfInfo: Version=" + str(ord(line[1]))
                api = line[1]
                msg = "API v" + str(api)

                if api >= 4:
                    msg += ", FW v" + str(line[2]) + "." + str(line[3])

                logging.info(msg)
                return ("cnfInfo", line[1])

            elif msgId == 0x82:  # reqLine
                # print "> reqLine: " + str(ord(line[1]))
                return ("reqLine", line[1])

            elif msgId == 0xC4:  # cnfTest
                return ("cnfTest", line[1])

            elif msgId == 0x84:
                hall_l = (line[2] << 8) + line[3]
                hall_r = (line[4] << 8) + line[5]

                self.options_ui.progress_hall_l.setValue(hall_l)
                self.options_ui.progress_hall_r.setValue(hall_r)
                self.options_ui.slider_position.setValue(line[7])
                carriage = line[6]
                if carriage == 1:
                    self.options_ui.label_carriage.setText("K Carriage")
                elif carriage == 2:
                    self.options_ui.label_carriage.setText("L Carriage")

                return ("indState", line[1])

            else:
                logging.debug("unknown message: ") # drop crlf
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(line)
                return ("unknown", 0)
        return("none", 0)

  def __cnfLine(self, lineNumber):
        imgHeight = self.__image.imgHeight()
        lenImgExpanded = len(self.__image.imageExpanded())
        color = 0
        indexToSend = 0
        sendBlankLine = False
        lastLine = 0x00

        # TODO optimize performance
        # initialize bytearray to 0x00
        bytes = bytearray(25)
        for x in range(0, 25):
            bytes[x] = 0x00

        if lineNumber < 256:
            # TODO some better algorithm for block wrapping
            # if the last requested line number was 255, wrap to next block of
            # lines
            if self.__formerRequest == 255 and lineNumber == 0:
                self.__lineBlock += 1
            # store requested line number for next request
            self.__formerRequest = lineNumber
            reqestedLine = lineNumber

            # adjust lineNumber with current block
            lineNumber = lineNumber \
                + (self.__lineBlock * 256)

            #########################
            # decide which line to send according to machine type and amount of colors
            # singlebed, 2 color
            if self.__machineType == 'single' \
                    and self.__numColors == 2:

                # when knitting infinitely, keep the requested
                # lineNumber in its limits
                if self.__infRepeat:
                    lineNumber = lineNumber % imgHeight

                # color is always 0 in singlebed,
                # because both colors are knitted at once
                color = 0

                # calculate imgRow
                imgRow = (lineNumber + self.__startLine) % imgHeight

                # 0   1   2   3   4 .. (imgRow)
                # |   |   |   |   |
                # 0 1 2 3 4 5 6 7 8 .. (imageExpanded)
                indexToSend = imgRow * 2
                # Check if the last line of the image was requested
                if imgRow == imgHeight - 1:
                    lastLine = 0x01

            # doublebed, 2 color
            elif self.__machineType == 'ribber' \
                    and self.__numColors == 2:

                # when knitting infinitely, keep the requested
                # lineNumber in its limits
                if self.__infRepeat:
                    lineNumber = lineNumber % lenImgExpanded

                # calculate imgRow
                imgRow = (int(lineNumber / 2) + self.__startLine) % imgHeight

                # 0 0 1 1 2 2 3 3 4 4 .. (imgRow)
                # 0 1 2 3 4 5 6 7 8 9 .. (lineNumber)
                # | |  X  | |  X  | |
                # 0 1 3 2 4 5 7 6 8 9 .. (imageExpanded)
                # A B B A A B B A A B .. (color)
                indexToSend = self.__startLine * 2

                color = 0  # A
                if reqestedLine % 4 == 1 or reqestedLine % 4 == 2:
                    color = 1  # B

                # Decide if lineNumber has to be switched or not
                if reqestedLine % 4 == 2:
                    indexToSend += lineNumber + 1
                elif reqestedLine % 4 == 3:
                    indexToSend += lineNumber - 1
                else:
                    indexToSend += lineNumber

                indexToSend = indexToSend % lenImgExpanded

                # Decide whether to send lastLine Flag
                if (imgRow == imgHeight - 1) \
                        and (lineNumber % 4 == 1 or lineNumber % 4 == 3):
                    lastLine = 0x01

            # doublebed, multicolor
            elif self.__machineType == 'ribber' \
                    and self.__numColors > 2:

                # when knitting infinitely, keep the requested
                # lineNumber in its limits
                if self.__infRepeat:
                    # *2 because of BLANK lines in between
                    lineNumber = lineNumber % (2*lenImgExpanded)

                # calculate imgRow
                imgRow = (int(
                    lineNumber / (self.__numColors * 2)) + self.__startLine) % imgHeight

                if (lineNumber % 2) == 1:
                    sendBlankLine = True
                else:
                    logging.debug("COLOR" + str(color))

                color = (lineNumber / 2) % self.__numColors

                #indexToSend = self.__startLine * self.__numColors
                indexToSend = int((imgRow * self.__numColors) + color)

                indexToSend = indexToSend % lenImgExpanded

                if (indexToSend == (lenImgExpanded-1)) \
                        and (sendBlankLine == True):
                    lastLine = 0x01

            elif self.__machineType == 'circular' \
                    and self.__numColors == 2:

                # when knitting infinitely, keep the requested
                # lineNumber in its limits
                if self.__infRepeat:
                    # *2 because of BLANK lines in between
                    lineNumber = lineNumber % (2*lenImgExpanded)

                imgRow = (int(lineNumber / 4) + self.__startLine) % imgHeight

                # Color      A B  A B  A B
                # ImgRow     0-0- 1-1- 2-2-
                # Index2Send 0 1  2 3  4 5
                # LineNumber 0123 4567 8911
                #                        01

                if (lineNumber % 2) == 1:
                    sendBlankLine = True

                indexToSend = self.__startLine * self.__numColors
                indexToSend += lineNumber / 2
                indexToSend = int(indexToSend)

                indexToSend = indexToSend % lenImgExpanded

                if (indexToSend == (lenImgExpanded-1)) \
                        and (sendBlankLine == True):
                    lastLine = 0x01

            #########################

            # assign pixeldata
            imgStartNeedle = self.__image.imgStartNeedle()
            if imgStartNeedle < 0:
                imgStartNeedle = 0

            imgStopNeedle = self.__image.imgStopNeedle()
            if imgStopNeedle > 199:
                imgStopNeedle = 199

            # set the bitarray
            if color == 0 \
                    and self.__machineType == 'ribber':
                for col in range(0, 200):
                    if col < imgStartNeedle \
                            or col > imgStopNeedle:
                        bytes = self.__setPixel(bytes, col)

            for col in range(0, self.__image.imgWidth()):
                pxl = (self.__image.imageExpanded())[indexToSend][col]
                # take the image offset into account
                if pxl == True and sendBlankLine == False:
                    pxlNumber = col + self.__image.imgStartNeedle()
                    if pxlNumber < 200: # TODO implement for generic machine width
                        bytes = self.__setPixel(
                            bytes, pxlNumber)

            # TODO implement CRC8
            crc8 = 0x00

            # send line to machine
            if self.__infRepeat:
              self.__ayabCom.cnf_line(reqestedLine, bytes, 0, crc8)
            else:
              self.__ayabCom.cnf_line(reqestedLine, bytes, lastLine, crc8)

            # screen output
            msg = str(self.__lineBlock) # Block
            msg += ' ' + str(lineNumber) # Total Line Number
            msg += ' reqLine: ' + str(reqestedLine)
            msg += ' imgRow: ' + str(imgRow)
            if sendBlankLine == True:
                msg += ' BLANK LINE'
            else:
                msg += ' indexToSend: ' + str(indexToSend)
                msg += ' ' + str((self.__image.imageExpanded())[indexToSend])
            logging.debug(msg)

            #sending line progress to gui
            self.__emit_progress(imgRow+1, imgHeight)

        else:
            logging.error("requested lineNumber out of range")

        if lastLine:
          if self.__infRepeat:
              return 0  # keep knitting
          else:
              return 1  # image finished
        else:
            return 0  # keep knitting

  def __knitImage(self, pImage, pOptions):
      self.__formerRequest = 0
      self.__image = pImage
      self.__startLine = pImage.startLine()

      self.__numColors = pOptions["num_colors"]
      self.__machineType = pOptions["machine_type"]
      self.__infRepeat = pOptions["inf_repeat"]

      API_VERSION = self.__API_VERSION
      curState = 's_init'
      oldState = 'none'

      if not self.__ayabCom.open_serial(pOptions["portname"]):
          logging.error("Could not open serial port")
          return

      self._knitImage = True
      while self._knitImage:
          # TODO catch keyboard interrupts to abort knitting
          # TODO: port to state machine or similar.
          rcvMsg, rcvParam = self.__checkSerial()
          if curState == 's_init':
              if oldState != curState:
                  self.__ayabCom.req_info()

              if rcvMsg == 'cnfInfo':
                  if rcvParam == API_VERSION:
                      if pOptions["testmode"]:
                        curState = 's_start'
                      else:
                        curState = 's_waitForInit'
                        self.__updateNotification("Please init machine. (Set the carriage to mode KC-I or KC-II and move the carriage over the left turn mark).")
                  else:
                      self.__notify_user("Wrong Arduino Firmware Version. "
                                         + "Please check if you have flashed "
                                         + "the latest version. ("
                                         + str(rcvParam) + "/"
                                         + str(API_VERSION) + ")")
                      logging.error("wrong API version: " + str(rcvParam)
                                        + (" (expected: )") + str(API_VERSION))
                      return

          if curState == 's_waitForInit':
              if rcvMsg == "indState":
                if rcvParam == 1:
                    curState = 's_start'
                else:
                    logging.debug("init failed")

          if curState == 's_start':
              if oldState != curState:
                if pOptions["testmode"]:
                    self.__ayabCom.req_test()
                else:
                    self.__ayabCom.req_start(self.__image.knitStartNeedle(),
                                             self.__image.knitStopNeedle())

              if rcvMsg == 'cnfTest':
                if rcvParam == 1:
                    self.__updateNotification("Testmode")
                else:
                    self.__updateNotification()
                    logging.error("Starting Testmode failed")
                    return

              if rcvMsg == 'cnfStart':
                  if rcvParam == 1:
                      curState = 's_operate'
                      self.__updateNotification("Please Knit")
                  else:
                      self.__updateNotification()
                      self.__wait_for_user_action("Device not ready, configure and try again.")
                      logging.error("device not ready")
                      return

          if curState == 's_operate':
              if rcvMsg == 'reqLine':
                  imageFinished = self.__cnfLine(rcvParam)
                  if imageFinished:
                      curState = 's_finished'

          if curState == 's_finished':
              self.__updateNotification("Image transmission finished. Please knit until you hear the double beep sound.")
              return

          oldState = curState

      self.options_ui.label_carriage.setText("No carriage detected")
      return
