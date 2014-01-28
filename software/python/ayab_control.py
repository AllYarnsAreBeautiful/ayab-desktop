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


import os,sys,time                # std lib
import serial                     # serial communication
import Image                      # for image operations
from optparse import OptionParser # argument parsing


def calc_imgStartStopNeedles():
    global ImgStartNeedle
    global ImgStopNeedle
    global ImgPosition    

    if ImgPosition == 'center':
        _needleWidth = (StopNeedle - StartNeedle) +1
        ImgStartNeedle = (StartNeedle + _needleWidth/2) - knit_img_width/2
        ImgStopNeedle  = ImgStartNeedle + knit_img_width -1      

    elif ImgPosition == 'alignLeft':
        ImgStartNeedle = StartNeedle
        ImgStopNeedle  = ImgStartNeedle + knit_img_width

    elif ImgPosition == 'alignRight':
        ImgStopNeedle = StopNeedle
        ImgStartNeedle = ImgStopNeedle - knit_img_width

    elif int(ImgPosition) > 0 and int(ImgPosition) < 200:
        ImgStartNeedle = int(ImgPosition)
        ImgStopNeedle  = ImgStartNeedle + knit_img_width

    else:
        print "unknown alignment"
        return False
    return True


def checkSerial( curState ):
    time.sleep(0.5) #TODO if problems in communication, tweak here
    line = ''
    while ser.inWaiting() > 0:
        line += ser.read(1)
        #line = ser.readline()    

    if line != '':
        msgId = ord(line[0])            
        if msgId == 0xC1:    # cnfStart
            msg = "> cnfStart: "
            if ord(line[1]) == 1:
                msg += "success"
            else:
                msg += "failed"
            print msg

            # reqStart was successful, proceed to next state
            if curState == 's_start' and ord(line[1]) == 1:
                curState = 's_operate'
                print "-----Ready to operate-----"
            else:
                curState = 's_abort'

        elif msgId == 0xC3: # cnfInfo
            print "> cnfInfo: Version=" + str(ord(line[1]))
            # reqInfo showed the right version, proceed to next state            
            if curState == 's_init' and ord(line[1]) == 0x01:
                curState = 's_start'
            else:
                curState = 's_abort'

        elif msgId == 0x82: #reqLine            
            msg = "> reqLine: "
            msg += str(ord(line[1]))
            print msg
            
            if curState == 's_operate':
                _imgFinished = cnfLine(ord(line[1]))
                if _imgFinished:
                    curState = 's_finished'
        else:
            print "unknown message: "
            print line[:] #drop crlf
            curState = 's_abort'

    return curState


def serial_reqInfo():
    print "< reqInfo"
    ser.write(chr(0x03) + '\n\r')

def serial_reqStart():
    msg = chr(0x01)                     #msg id
    msg += chr(int(StartNeedle))
    msg += chr(int(StopNeedle))
    msg += chr(int(StartLine))
    print "< reqStart"
    ser.write(msg + '\n\r')

def serial_cnfLine(lineNumber, lineData, flags, crc8):
    msg  = chr(0x42)                    # msg id
    msg += chr(lineNumber)              # line number
    msg += lineData                     # line data
    msg += chr(flags)                   # flags
    msg += chr(crc8)                    # crc8
    print "< cnfLine"
    ser.write(msg + '\n\r')


def setBit(int_type, offset):
    mask = 1 << offset
    return(int_type | mask)

def setPixel(bytearray,pixel):
    _numByte = int(pixel/8)
    bytearray[_numByte] = setBit(int(bytearray[_numByte]),pixel-(8*_numByte))
    return

def cnfLine(lineNumber):  
    #TODO optimize performance
    global LastRequest  
    global LineBlock
    #initialize bytearray to 0x00
    bytes = bytearray(25)
    for x in range(0,25):
        bytes[x] = 0x00

    if lineNumber < 256:
        #TODO some better algorithm for block wrapping
        # if the last requested line number was 255, wrap to next block of lines 
        if LastRequest == 255 and lineNumber == 0:
            LineBlock += 1
        # store requested line number for next request
        LastRequest = lineNumber
        # adjust actual line number according to current block
        imgLineNumber  += LineBlock*255

        # build output message and screen output
        msg = ''
        for x in range(0, knit_img_width):
            pxl = knit_img.getpixel((x, imgLineNumber))            
            if pxl == 255: # contrast color
                # take the image offset into account
                setPixel(bytes,x+ImgStartNeedle)
                msg += "#"
            else:
                msg += '-'
        msg += str(imgLineNumber)
        msg += ' '
        print msg + str(lineNumber)

        if imgLineNumber == knit_img_height-1:
            lastLine = 0x01
        else:
            lastLine = 0x00

        # TODO implement CRC8
        crc8 = 0x00

        serial_cnfLine(lineNumber, bytes, lastLine, crc8)
    else:
        print "requested lineNumber out of range"

    if lineNumber == knit_img_height-1:
        return 1 # image finished 
    else:
        return 0


#
# MENU FUNCTIONS
#

def a_showImage():
    """show the image in ASCII"""
    for y in range(0, knit_img_height):
        msg = ''
        for x in range(0, knit_img_width):
            pxl = knit_img.getpixel((x, y))
            if pxl == 255:
                msg += "#"
            else:
                msg += '-'
        print msg
    raw_input("press Enter")


def a_invertImage():
    """invert the pixels of the image"""
    global knit_img

    for y in range(0, knit_img_height):
      for x in range(0, knit_img_width):
        pxl = knit_img.getpixel((x, y))
        if pxl == 255:
          knit_img.putpixel((x,y),0)
        else:
          knit_img.putpixel((x,y),255)


def a_rotateImage():
    """rotate the image 90 degrees clockwise"""
    global knit_img
    global knit_img_width
    global knit_img_height

    print "rotating image 90 degrees..."
    knit_img = knit_img.rotate(-90)
    knit_img_width  = knit_img.size[0]
    knit_img_height = knit_img.size[1]


def a_resizeImage():
    """resize the image to a given width, keeping the aspect ratio"""
    global knit_img
    global knit_img_width
    global knit_img_height

    newWidth = int(raw_input("New Width (pixel): "))
    wpercent = (newWidth/float(knit_img_width))
    hsize = int((float(knit_img_height)*float(wpercent)))
    knit_img = orig_img.resize((newWidth,hsize), Image.ANTIALIAS)
    
    knit_img_width  = knit_img.size[0]
    knit_img_height = knit_img.size[1]

    a_showImagePosition()


def a_setNeedles():
    """set the start and stop needle"""
    global StartNeedle
    global StopNeedle
    
    StartNeedle = int(raw_input("Start Needle (0 <= x <= 198): "))
    StopNeedle  = int(raw_input("Stop Needle  (1 <= x <= 199): "))


def a_setImagePosition():
    global ImgPosition

    print "Allowed options:"
    print ""
    print "center"
    print "alignLeft"
    print "alignRight"
    print "<position from left>"
    print ""
    ImgPosition = raw_input("Image Position: ")
    return

def a_setStartLine():
    global StartLine

    StartLine = int(raw_input("Start Line: "))
    #Check if StartLine is in valid range (picture height)
    if StartLine >= knit_img_height:
        StartLine = 0
        return
        
    #Modify Block Counter and fix StartLine if >255
    LineBlock = int(StartLine/255)
    StartLine %= 255
    #DEBUG OUTPUT
    print LineBlock
    print StartLine
    return

def a_showImagePosition():
    """show the current positioning of the image"""

    calc_imgStartStopNeedles()
    
    print "Image Start: ", ImgStartNeedle
    print "Image Stop : ", ImgStopNeedle  
    print ""

    # print markers for active area and knitted image
    msg = '|'
    for i in range(0,200):
        if i >= StartNeedle and i <= StopNeedle:
            if i >= ImgStartNeedle and i <= ImgStopNeedle:
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
 

def a_knitImage():
    _curState = 's_init'
    _oldState = _curState
    _reqSent  = 0

    while True:
        _curState = checkSerial(_curState)

        if _oldState != _curState:
            _reqSent = 0
        elif _curState == 's_abort':
            raw_input("press Enter")
            return

        if _curState == 's_init':
            if _reqSent == 0:
                serial_reqInfo()
                _reqSent = 1

        elif _curState == 's_start':
            if _reqSent == 0:
                serial_reqStart()
                _reqSent = 1     

        #elif _curState == 's_operate':
        #    print "s_operate"
        elif _curState == 's_finished':
            print "Image finished"
            raw_input("press Enter")
            return

        _oldState = _curState
    
    return     

def print_main_menu():
    """Print the main menu"""
    print "======================"
    print "=   AYAB CONTROL v1  ="
    print "======================"
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
    print "Filename      : ", filename
    print "Original Image: ", orig_img.size, orig_img.mode
    print "Knitting Image: ", knit_img.size, "black/white" #knit_img.mode
    print ""
    print "Start Needle  : ", StartNeedle
    print "Stop Needle   : ", StopNeedle
    print "Start Line    : ", StartLine
    print "Image position: ", ImgPosition


def no_such_action():
    print "Please make a valid selection"


def mainFunction():
    """main"""


    actions = {"1": a_showImage, 
                "2": a_invertImage,
                "3": a_resizeImage, 
                "4": a_rotateImage, 
                "5": a_setNeedles, 
                "6": a_setImagePosition,
                "7": a_setStartLine, 
                "8": a_showImagePosition,
                "9": a_knitImage}    
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        
        print_main_menu()
        print ""    
        selection = raw_input("Your selection: ")
        print ""
        if "0" == selection:
            #ser.close()
            exit()
            return
        toDo = actions.get(selection, no_such_action)
        toDo()

        #checkSerial( False )

    return


if __name__ == "__main__":
    if (len(sys.argv) < 2):
      print "Usage: ayab_control.py <FILE>"
      os.system("exit")
    else:
      filename = sys.argv[1]
      if filename != '':
          orig_img = Image.open(filename)
          orig_img = orig_img.convert('1')
          knit_img = orig_img
          knit_img_width  = knit_img.size[0]
          knit_img_height = knit_img.size[1]

          StartNeedle = 80
          StopNeedle  = 120
          StartLine   = 0
          ImgPosition = 'center'
          ImgStartNeedle = 0
          ImgStopNeedle  = 0
          # Helper variables for images with height > 255
          LineBlock      = 0
          LastRequest    = 0

          ser = serial.Serial('/dev/ttyACM0', 115200)

          mainFunction()
      else:
         print "Please check the filename"
