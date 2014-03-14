# -*- coding: utf-8 -*-
import os
import sys
import serial

import ayab_image
import ayab_control

# Commandline Parameter Parsing
from optparse import OptionParser

VERSION = "1.1"

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
    for y in range(0, image.knitImage().size[1]): #height
        msg = ''
        for x in range(0, image.knitImage().size[0]): #width
            pxl = image.knitImage().getpixel((x, y))
            if pxl == 255:
                msg += "#"
            else:
                msg += '-'
        print msg
    image.imageToIntern()
    raw_input("press any key")


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
      raw_input("press any key")


def resizeImage(image):
  image.resizeImage(int(raw_input("New Width (pixel): ")))

def setKnitNeedles(image):
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
    print " 9 - knit image with current settings"
    print ""
    print " 0 - Exit"
    print ""
    print "INFORMATION"
    print "Filename      : ", image.filename()
    # print "Original Image: ", orig_img.size, orig_img.mode
    # print "Knitting Image: ", knit_img.size, "black/white" #knit_img.mode
    print ""
    print "Start Needle  : ", image.knitStartNeedle()
    print "Stop Needle   : ", image.knitStopNeedle()
    print "Start Line    : ", image.startLine()+image.startBlock()*256, \
      "- Line ", image.startLine(), " Block ", image.startBlock()
    print "Image position: ", image.imgPosition()
  

def no_such_action():
    print "Please make a valid selection"


def mainFunction(image):
    """main"""

    actions = {"1": "showImage(image)", 
                "2": "image.invertImage()",
                "3": "resizeImage(image)", 
                "4": "image.rotateImage()", 
                "5": "setKnitNeedles(image)", 
                "6": "setImagePosition(image)",
                "7": "setStartLine(image)", 
                "8": "showImagePosition(image)"
                #"9": a_knitImage
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
        dest = "portname", \
        metavar= "PORT", \
        default = "/dev/ttyACM0", \
        help = "Serial Port used for communication" \
        " with the machine [default: %default]")
    parser.add_option("-l", "--list", \
        dest = "list", \
        action="store_true", \
        default = False, \
        help = "List all available serial ports and exit [default: %default]")

    (options, args) = parser.parse_args()

    if options.list:
      print str(list(getSerialPorts()))
      sys.exit(0)

    if len(args):
      m_image = ayab_image.ayabImage(args[0])
    
      m_ayabControl = ayab_control.ayabControl(options)

      mainFunction(m_image)

    sys.exit(0)
