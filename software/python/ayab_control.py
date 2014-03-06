# -*- coding: utf-8 -*-

import ayab_communication

class ayabControl(object):
    def __init__(self):
        self.__ayabCom = ayab_communication.ayabCommunication()


    # def __checkSerial( curState ):
    #     time.sleep(0.5) #TODO if problems in communication, tweak here
    #     line = ''
    #     while ser.inWaiting() > 0:
    #         line += ser.read(1)
    #         #line = ser.readline()    

    #     if line != '':
    #         msgId = ord(line[0])            
    #         if msgId == 0xC1:    # cnfStart
    #             msg = "> cnfStart: "
    #             if ord(line[1]) == 1:
    #                 msg += "success"
    #             else:
    #                 msg += "failed"
    #             print msg

    #             # reqStart was successful, proceed to next state
    #             if curState == 's_start' and ord(line[1]) == 1:
    #                 curState = 's_operate'
    #                 print "-----Ready to operate-----"
    #             else:
    #                 curState = 's_abort'

    #         elif msgId == 0xC3: # cnfInfo
    #             print "> cnfInfo: Version=" + str(ord(line[1]))
    #             # reqInfo showed the right version, proceed to next state            
    #             if curState == 's_init' and ord(line[1]) == API_VERSION:
    #                 curState = 's_start'
    #             else:
    #                 curState = 's_abort'

    #         elif msgId == 0x82: #reqLine            
    #             msg = "> reqLine: "
    #             msg += str(ord(line[1]))
    #             print msg
                
    #             if curState == 's_operate':
    #                 _imgFinished = cnfLine(ord(line[1]))
    #                 if _imgFinished:
    #                     curState = 's_finished'
    #         else:
    #             print "unknown message: "
    #             print line[:] #drop crlf
    #             curState = 's_abort'

    #     return curState


    # def __cnfLine(lineNumber):  
    #     #TODO optimize performance
    #     global LastRequest  
    #     global LineBlock
    #     #initialize bytearray to 0x00
    #     bytes = bytearray(25)
    #     for x in range(0,25):
    #         bytes[x] = 0x00

    #     if lineNumber < 256:
    #         #TODO some better algorithm for block wrapping
    #         # if the last requested line number was 255, wrap to next block of lines 
    #         if LastRequest == 255 and lineNumber == 0:
    #             LineBlock += 1
    #         # store requested line number for next request
    #         LastRequest = lineNumber
    #         # adjust actual line number according to current block
    #         imgLineNumber = lineNumber
    #         imgLineNumber += LineBlock*256

    #         # build output message and screen output
    #         msg = ''
    #         for x in range(0, knit_img_width):
    #             pxl = knit_img.getpixel((x, imgLineNumber))            
    #             if pxl == 255: # contrast color
    #                 # take the image offset into account
    #                 setPixel(bytes,x+ImgStartNeedle)
    #                 msg += "#"
    #             else:
    #                 msg += '-'
    #         msg += str(imgLineNumber)
    #         msg += ' '
    #         msg += str(lineNumber)
    #         msg += ' '
    #         print msg + str(LineBlock)

    #         if imgLineNumber == knit_img_height-1:
    #             lastLine = 0x01
    #         else:
    #             lastLine = 0x00

    #         # TODO implement CRC8
    #         crc8 = 0x00

    #         serial_cnfLine(lineNumber, bytes, lastLine, crc8)
    #     else:
    #         print "requested lineNumber out of range"

    #     if lineNumber == knit_img_height-1:
    #         return 1 # image finished 
    #     else:
    #         return 0


    def knitImage(self, pImage):
        _curState = 's_init'
        _oldState = _curState
        _reqSent  = 0

        self.__ayabCom.openSerial()

        # while True:
        #     _curState = checkSerial(_curState)

        #     if _oldState != _curState:
        #         _reqSent = 0
        #     elif _curState == 's_abort':
        #         raw_input("press Enter")
        #         return

        #     if _curState == 's_init':
        #         if _reqSent == 0:
        #             serial_reqInfo()
        #             _reqSent = 1

        #     elif _curState == 's_start':
        #         if _reqSent == 0:
        #             serial_reqStart()
        #             _reqSent = 1     

        #     #elif _curState == 's_operate':
        #     #    print "s_operate"
        #     elif _curState == 's_finished':
        #         print "Image finished"
        #         raw_input("press Enter")
        #         return

        #     _oldState = _curState
        
        return  


