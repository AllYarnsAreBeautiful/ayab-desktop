import time
import serial
import sys
import Image

#
# HELPER FUNCTIONS
#
def setBit(int_type, offset):
    mask = 1 << offset
    return(int_type | mask)

def setPixel(bytearray,pixel):
    _numByte = int(pixel/8)
    bytearray[_numByte] = setBit(int(bytearray[_numByte]),pixel-(8*_numByte))
    return

#
# ACTIONS
#
def a_reqInfo():
    print "< reqInfo"
    ser.write(chr(0x03) + '\n\r')

def a_reqStart( ):
    startNeedle = raw_input("Start Needle: ")
    stopNeedle  = raw_input("Stop Needle : ")

    msg = chr(0x01)                     #msg id
    msg += chr(int(startNeedle))
    msg += chr(int(stopNeedle))
    print "< reqStart"
    ser.write(msg + '\n\r')


def a_cnfLine():
    lineNumber = raw_input("Line Number    : ")
    lineNumber = int(lineNumber)

    lineData = ''
    while len(lineData) != 25:
        lineData = raw_input("Line Data      : ")

    lastLine   = raw_input("Last Line (0/1): ")
    flags      = int(lastLine)
    crc8 = 0x00
    print type(lineData)
    cnfLine(lineNumber, lineData, flags, crc8)


def a_printImage():
    msg = chr(0x01)       #msg id
    msg += chr(int(0))
    msg += chr(int(199))
    print "< reqStart"
    ser.write(msg + '\n\r')
    while True:
        checkSerial( True )


def a_showImage():
    for y in range(0, imageH):
        msg = ''
        for x in range(0, imageW):
            pxl = image.getpixel((x, y))
            if pxl == 255:
                msg += "#"
            else:
                msg += '-'
        print msg


def sendLine(lineNumber):
    bytes = bytearray(25)
    if lineNumber < imageH:
        msg = ''
        for x in range(0, imageW):
            pxl = image.getpixel((x, lineNumber))            
            if pxl == 255:
                msg += "#"
                setPixel(bytes,x)
            else:
                msg += '-'
        print msg + str(lineNumber)

        if lineNumber == imageH-1:
            lastLine = 0x01
        else:
            lastLine = 0x00

        cnfLine(lineNumber, bytes, lastLine, 0x00)


def cnfLine(lineNumber, lineData, flags, crc8):
    msg  = chr(0x42)                    # msg id
    msg += chr(lineNumber)              # line number
    msg += lineData                     # line data
    msg += chr(flags)                   # flags
    msg += chr(crc8)                    # crc8
    print "< cnfLine"
    ser.write(msg + '\n\r')


def checkSerial( printMode ):
    time.sleep(1)
    out = ''
    while ser.inWaiting() > 0:
        line = ser.readline()        

        msgId = ord(line[0])            
        if msgId == 0xC1:    # cnfStart
            msg = "> cnfStart: "
            if(ord(line[1])):
                msg += "success"
            else:
                msg += "failed"
            print msg

        elif msgId == 0xC3: # cnfInfo
            msg = "> cnfInfo: Version="
            msg += str(ord(line[1]))
            print msg

        elif msgId == 0x82: #reqLine            
            
            msg = "> reqLine: "
            msg += str(ord(line[1]))
            print msg
            if printMode:
                sendLine(ord(line[1]))
        else:
            print line[:-2] #drop crlf


def no_such_action():
    print "Please make a valid selection"


def print_menu():
    print "==================="
    print "=   AYAB CONTROL  ="
    print "==================="    
    print "= andz & chris007 ="
    print "=       v1        ="
    print "==================="
    print "Image: " + filename  
    print img.format, img.size, img.mode
    print ""
    print "1 - reqInfo"
    print "2 - reqStart"
    print "3 - cnfLine"
    print ""
    print "4 - show image"
    print "5 - print image"
    print ""
    print "0 - Exit"


def mainFunction():   

    actions = {"1": a_reqInfo, "2": a_reqStart, "3": a_cnfLine, "4": a_showImage, "5": a_printImage}
    print_menu()
    while True:
        print ""    
        selection = raw_input("Your selection: ")
        print ""
        if "0" == selection:
            ser.close()
            exit()
            return
        toDo = actions.get(selection, no_such_action)
        toDo()

        checkSerial( False )
        

        
filename = sys.argv[1]
if filename != '':
    img = Image.open(filename)
    image = img.convert('1')
    imageW = image.size[0]
    imageH = image.size[1]
    maxWidth = 200 
    if imageW > maxWidth:
        wpercent = (maxWidth/float(imageW))
        hsize = int((float(imageH)*float(wpercent)))
        image = image.resize((maxWidth,hsize), Image.ANTIALIAS)
        imageW = image.size[0]
        imageH = image.size[1]

ser = serial.Serial('/dev/ttyACM0', 115200)

mainFunction()
