import os,sys   # std lib
import Image # for image operations
from optparse import OptionParser # argument parsing


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
      msg = ''
      for x in range(0, knit_img_width):
        pxl = knit_img.getpixel((x, y))
        if pxl == 255:
          knit_img.putpixel((x,y),0)
        else:
          knit_img.putpixel((x,y),255)


def a_rotateImage():
    """rotate the image 90 degrees clockwise"""
    global knit_img

    print "rotating image 90 degrees..."
    knit_img = knit_img.rotate(-90)


def a_resizeImage():
    """resize the image to a given width, keeping the aspect ratio"""
    global knit_img
    global knit_img_width
    global knit_img_height

    newWidth = int(raw_input("New Width (pixel): "))
    wpercent = (newWidth/float(knit_img_width))
    hsize = int((float(knit_img_height)*float(wpercent)))
    knit_img = knit_img.resize((newWidth,hsize), Image.ANTIALIAS)
    
    knit_img_width  = knit_img.size[0]
    knit_img_height = knit_img.size[1]


def a_setNeedles():
    """set the start and stop needle"""
    global startNeedle
    global stopNeedle
    
    startNeedle = raw_input("Start Needle (0 <= x <  199): ")
    stopNeedle  = raw_input("Stop Needle  (1 <  x <= 199): ")
      

def print_main_menu():
    """Print the main menu"""
    print "======================"
    print "=   AYAB CONTROL v1  ="
    print "======================"
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
    print ""
    print " 0 - Exit"
    print ""
    print "INFORMATION"
    print "Filename      : ", filename
    print "Original Image: ", orig_img.size, orig_img.mode
    print "Knitting Image: ", knit_img.size, "black/white" #knit_img.mode
    print ""
    print "Start Needle  : ", startNeedle
    print "Stop Needle   : ", stopNeedle

def no_such_action():
    print "Please make a valid selection"


def mainFunction():
    """main"""


    actions = {"1": a_showImage, "2": a_invertImage, "3": a_resizeImage, "4": a_rotateImage, "5": a_setNeedles}    
    while True:
        os.system("@echo OFF")
        os.system("cls")
        
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
          knit_img = orig_img.convert('1')
          knit_img_width  = knit_img.size[0]
          knit_img_height = knit_img.size[1]

          startNeedle = 0
          stopNeedle  = 199

          mainFunction()
      else:
         print "Please check the filename"