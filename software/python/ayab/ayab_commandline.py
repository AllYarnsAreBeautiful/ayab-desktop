#!/usr/bin/python
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

import os
import sys
import serial
import serial.tools.list_ports

from optparse import OptionParser

import ayab_image
import ayab_control

VERSION = "1.2"

def getSerialPorts():
  """
  Returns a generator for all available serial ports
  """
  if os.name == 'nt':
   # windows
   for i in range(256):
      try:
         s = serial.Serial(i)
         s.close()
         yield 'COM' + str(i + 1)
      except serial.SerialException:
         pass
  else:
   # unix
   for port in serial.tools.list_ports.comports():
      yield port[0]


def showImage(image):
    """
    show the image in ASCII
    """
    for row in range(0, image.imgHeight()):
        msg = ''
        for col in range(0, image.imgWidth()):
            # TODO Mapping of color numbers to
            #      fancy ascii representation
            msg += str((image.imageIntern())[row][col])
        print msg
    raw_input("press Enter")


def showImagePosition(image):
      """
      show the current positioning of the image
      """
      imgStartNeedle = image.imgStartNeedle()
      imgStopNeedle  = image.imgStopNeedle()
      knitStartNeedle = image.knitStartNeedle()
      knitStopNeedle  = image.knitStopNeedle()

      print "Image Start: ", imgStartNeedle
      print "Image Stop : ", imgStopNeedle
      print ""

      # print markers for active area and knitted image
      msg = '|'
      for i in range(0,200):
          if i >= knitStartNeedle and i <= knitStopNeedle:
              if i >= imgStartNeedle and i <= imgStopNeedle:
                  msg += 'x'
              else:
                  msg += '-'
          else:
              msg += '_'
      msg += '|'
      print msg

      # print markers at multiples of 10
      msg = '|'
      for i in range(0,200):
          if i == 100:
              msg += '|'
          else:
              if (i % 10) == 0:
                  msg += '^'
              else:
                  msg += ' '
      msg += '|'
      print msg
      raw_input("press Enter")


def resizeImage(image):
  image.resizeImage(int(raw_input("New Width (pixel): ")))

def setKnitNeedles(image):
  # TODO Change to Green/Orange 100-0-100 range
  startNeedle = int(raw_input("Start Needle (0 <= x <= 198): "))
  stopNeedle  = int(raw_input("Stop Needle  (1 <= x <= 199): "))
  image.setKnitNeedles(startNeedle,stopNeedle)

def setImagePosition(image):
  print "Allowed options:"
  print ""
  print "center"
  print "left"
  print "right"
  print "<position from left>"
  print ""
  image.setImagePosition(raw_input("Image Position: "))


def setStartLine(image):
  image.setStartLine(int(raw_input("Start Line: ")))


def mainCallback(pSource, pString, pType):
  if pType == "stream":
    print pString
    return

  if pType == "error":
    print "E: " + pString
  elif pType == "debug":
    print "D: " + pString
  elif pType == "prompt":
    print pString

  raw_input("Press Enter")
  return


def print_main_menu(image):
    """Print the main menu"""
    print "======================"
    print "=    AYAB CONTROL    ="
    print "======================"
    print "Version: " + VERSION
    print "Distributed under GPL"
    print ""
    print "IMAGE TOOLS"
    print " 1 - show"
    print " 2 - invert"
    print " 3 - resize"
    print " 4 - rotate"
    print ""
    print "KNITTING"
    print " 5 - set start and stop needle"
    print " 6 - set image position"
    print " 7 - set start line"
    print " 8 - show image position"
    print ""
    print " 9 - knit image with current settings"
    print ""
    print " 0 - Exit"
    print ""
    print "INFORMATION"
    print "Machine Type  : ", options.machine_type
    print "Colors        : ", options.num_colors
    print "Filename      : ", image.filename()
    print "Width         : ", image.imgWidth()
    print "Height        : ", image.imgHeight()
    print ""
    print "Start Needle  : ", image.knitStartNeedle()
    print "Stop Needle   : ", image.knitStopNeedle()
    print "Start Line    : ", image.startLine()
    print "Image position: ", image.imgPosition()


def no_such_action():
    print "Please make a valid selection"


def mainFunction(options):
    """main"""
    if options.machine_type != 'single' \
          and options.machine_type != 'double':
      return "E: invalid machine type"
    if options.machine_type == 'single' \
          and options.num_colors != 2:
      print "E: singlebed only supports 2 color knitting"
      return


    image = ayab_image.ayabImage(options.filename, \
                                  options.num_colors)

    ayabControl = ayab_control.ayabControl(mainCallback)


    actions = {"1": "showImage(image)",
                "2": "image.invertImage()",
                "3": "resizeImage(image)",
                "4": "image.rotateImage()",
                "5": "setKnitNeedles(image)",
                "6": "setImagePosition(image)",
                "7": "setStartLine(image)",
                "8": "showImagePosition(image)",
                "9": "ayabControl.knitImage(image, options)"
                }
    while True:
        os.system('cls' if os.name=='nt' else 'clear')

        print_main_menu(image)
        print ""
        selection = raw_input("Your selection: ")
        print ""
        if "0" == selection:
            exit()
            return
        toDo = actions.get(selection, "no_such_action")
        eval(toDo)

    return


if __name__ == '__main__':

    # Parse command line options
    parser = OptionParser("%prog [filename] [options]", \
        description = "AYAB Control Commandline Version")
    parser.add_option("-p", "--port", \
        dest    = "portname", \
        metavar = "PORT", \
        default = "/dev/ttyACM0", \
        help    = "Serial Port used for communication" \
        " with the machine [default: %default]")
    parser.add_option("-c", "--colors", \
        dest    = "num_colors", \
        metavar = "COLORS", \
        type    = "int", \
        default = 2, \
        help    = "Number of Colors of your image [default: %default]")
    parser.add_option("-t", "--type", \
        dest    = "machine_type", \
        metavar = "TYPE", \
        default = "single", \
        help    = "Set the type of the machine (single/double bed) [default: %default]")
    parser.add_option("-l", "--list", \
        dest    = "list", \
        action  ="store_true", \
        default = False, \
        help    = "List all available serial ports and exit [default: %default]")

    (options, args) = parser.parse_args()

    if options.list:
      print str(list(getSerialPorts()))
      sys.exit(0)

    if len(args):
      options.filename = args[0]
      mainFunction(options)

    sys.exit(0)
