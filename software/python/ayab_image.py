# -*- coding: utf-8 -*-

import Image

class ayabImage(object):
  def __init__(self, pFilename):
    self.__origImage = Image.open(pFilename)
    self.__filename  = pFilename

    # knitImage: Internal Dataformat
    self.__knitImage = self.__origImage
    self.__knitImage = self.__knitImage.convert('1') # convert to 1 bit depth


  def showImage(self):
    """
    show the image in ASCII
    """
    for y in range(0, self.__knitImage.size[1]): #height
        msg = ''
        for x in range(0, self.__knitImage.size[0]): #width
            pxl = self.__knitImage.getpixel((x, y))
            if pxl == 255:
                msg += "#"
            else:
                msg += '-'
        print msg


  # def invertImage():
  #     """invert the pixels of the image"""
  #     global knit_img

  #     for y in range(0, knit_img_height):
  #       for x in range(0, knit_img_width):
  #         pxl = knit_img.getpixel((x, y))
  #         if pxl == 255:
  #           knit_img.putpixel((x,y),0)
  #         else:
  #           knit_img.putpixel((x,y),255)


  # def rotateImage():
  #     """rotate the image 90 degrees clockwise"""
  #     global knit_img
  #     global knit_img_width
  #     global knit_img_height

  #     print "rotating image 90 degrees..."
  #     knit_img = knit_img.rotate(-90)
  #     knit_img_width  = knit_img.size[0]
  #     knit_img_height = knit_img.size[1]

  #     calc_imgStartStopNeedles()


  # def resizeImage():
  #     """resize the image to a given width, keeping the aspect ratio"""
  #     global knit_img
  #     global knit_img_width
  #     global knit_img_height

  #     newWidth = int(raw_input("New Width (pixel): "))
  #     wpercent = (newWidth/float(knit_img_width))
  #     hsize = int((float(knit_img_height)*float(wpercent)))
  #     knit_img = orig_img.resize((newWidth,hsize), Image.ANTIALIAS)
      
  #     knit_img_width  = knit_img.size[0]
  #     knit_img_height = knit_img.size[1]

  #     a_showImagePosition()


  # def setNeedles():
  #     """set the start and stop needle"""
  #     global StartNeedle
  #     global StopNeedle
      
  #     StartNeedle = int(raw_input("Start Needle (0 <= x <= 198): "))
  #     StopNeedle  = int(raw_input("Stop Needle  (1 <= x <= 199): "))


  # def setImagePosition():
  #     global ImgPosition

  #     print "Allowed options:"
  #     print ""
  #     print "center"
  #     print "alignLeft"
  #     print "alignRight"
  #     print "<position from left>"
  #     print ""
  #     ImgPosition = raw_input("Image Position: ")
  #     return

  # def setStartLine():
  #     global StartLine
  #     global LineBlock

  #     StartLine = int(raw_input("Start Line: "))
  #     #Check if StartLine is in valid range (picture height)
  #     if StartLine >= knit_img_height:
  #         StartLine = 0
  #         return
          
  #     #Modify Block Counter and fix StartLine if >255
  #     LineBlock = int(StartLine/256)
  #     StartLine %= 256
  #     return

  # def showImagePosition():
  #     """show the current positioning of the image"""

  #     calc_imgStartStopNeedles()
      
  #     print "Image Start: ", ImgStartNeedle
  #     print "Image Stop : ", ImgStopNeedle  
  #     print ""

  #     # print markers for active area and knitted image
  #     msg = '|'
  #     for i in range(0,200):
  #         if i >= StartNeedle and i <= StopNeedle:
  #             if i >= ImgStartNeedle and i <= ImgStopNeedle:
  #                 msg += 'x'
  #             else:          
  #                 msg += '-'
  #         else:
  #             msg += '_'
  #     msg += '|'
  #     print msg

  #     # print markers at multiples of 10
  #     msg = '|'
  #     for i in range(0,200):
  #         if i == 100:
  #             msg += '|'
  #         else:
  #             if (i % 10) == 0:
  #                 msg += '^'
  #             else:
  #                 msg += ' '
  #     msg += '|'
  #     print msg

  #     raw_input("press Enter")
  #         