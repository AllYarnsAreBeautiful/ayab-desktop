# -*- coding: utf-8 -*-
import os
import sys
import serial

import ayab_image
import ayab_control

# Commandline Parameter Parsing
from optparse import OptionParser


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
   for port in list_ports.comports():
      yield port[0]
  

if __name__ == '__main__':

    # Parse command line options
    parser = OptionParser("%prog [options]", \
        description = "AYAB Control Commandline Version")
    parser.add_option("-p", "--port", dest = "portname", type = "string", \
        default = "/dev/ttyACM0", help = "Serial Port used for communication" \
        " with the machine [default: %default]")

    (options, args) = parser.parse_args()

    # DEBUG: Print all available serial ports
    print str(list(getSerialPorts()))

    
    m_ayabControl = ayab_control.ayabControl(options)
    m_image = ayab_image.ayabImage("..\..\patterns\uc3.png")
    #m_image.showImage()

    m_ayabControl.knitImage(m_image)

    sys.exit(0)
