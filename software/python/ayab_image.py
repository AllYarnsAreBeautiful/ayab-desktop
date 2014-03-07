# -*- coding: utf-8 -*-

import Image

class ayabImage(object):
  def __init__(self, pFilename):
    self.__imgPosition    = 'center'
    self.__imgStartNeedle = '0'
    self.__imgStopNeedle  = '0'

    self.__knitStartNeedle = 80
    self.__knitStopNeedle  = 119

    self.__startLine  = 0
    self.__startBlock = 0

    self.__origImage = Image.open(pFilename)
    self.__filename  = pFilename

    # TODO knitImage: convert to internal Dataformat
    self.__knitImage = self.__origImage
    self.__knitImage = self.__knitImage.convert('1') # convert to 1 bit depth
    self.__calcImgStartStopNeedles()

  def filename(self):
    return self.__filename

  def knitImage(self):
    return self.__knitImage

  def knitStartNeedle(self):
    return self.__knitStartNeedle

  def knitStopNeedle(self):
    return self.__knitStopNeedle

  def imgStartNeedle(self):
    return self.__imgStartNeedle

  def imgStopNeedle(self):
    return self.__imgStopNeedle

  def imgPosition(self):
    return self.__imgPosition

  def startLine(self):
    return self.__startLine

  def startBlock(self):
    return self.__startBlock

  def __calcImgStartStopNeedles(self):
    if self.__imgPosition == 'center':
        needleWidth = (self.__knitStopNeedle - self.__knitStartNeedle) +1
        self.__imgStartNeedle = (self.__knitStartNeedle + needleWidth/2) - self.__knitImage.size[0]/2
        self.__imgStopNeedle  = self.__imgStartNeedle + self.__knitImage.size[0] -1      

    elif self.__imgPosition == 'left':
        self.__imgStartNeedle = self.__knitStartNeedle
        self.__imgStopNeedle  = self.__imgStartNeedle + self.__knitImage.size[0]

    elif self.__imgPosition == 'right':
        self.__imgStopNeedle = self.__knitStopNeedle
        self.__imgStartNeedle = self.__imgStopNeedle - self.__knitImage.size[0]

    elif int(self.__imgPosition) > 0 and int(self.__imgPosition) < 200:
        self.__imgStartNeedle = int(self.__imgPosition)
        self.__imgStopNeedle  = self.__imgStartNeedle + self.__knitImage.size[0]

    else:
        print "unknown alignment"
        return False
    return True


  def invertImage(self):
      """
      invert the pixels of the image
      """
      for y in range(0, self.__knitImage.size[1]):
        for x in range(0, self.__knitImage.size[0]):
          pxl = self.__knitImage.getpixel((x, y))
          if pxl == 255:
            self.__knitImage.putpixel((x,y),0)
          else:
            self.__knitImage.putpixel((x,y),255)
      

  def rotateImage(self):
      """
      rotate the image 90 degrees clockwise
      """
      print "rotating image 90 degrees..."
      self.__knitImage = self.__knitImage.rotate(-90)

      self.__calcImgStartStopNeedles()


  def resizeImage(self, pNewWidth):
      """
      resize the image to a given width, keeping the aspect ratio
      """
      wpercent = (pNewWidth/float(self.__knitImage.size[0]))
      hsize = int((float(self.__knitImage.size[1])*float(wpercent)))
      self.__knitImage = self.__knitImage.resize((pNewWidth,hsize), Image.ANTIALIAS)

      self.__calcImgStartStopNeedles()


  def setKnitNeedles(self, pKnitStart, pKnitStop):
      """
      set the start and stop needle
      """      
      self.__knitStartNeedle = pKnitStart
      self.__knitStopNeedle  = pKnitStop


  def setImagePosition(self, pImgPosition):
      """
      set the position of the pattern
      """
      self.__imgPosition = pImgPosition
      self.__calcImgStartStopNeedles()
      return

  def setStartLine(self, pStartLine):
      """
      set the line where to start knitting
      """
      #Check if StartLine is in valid range (picture height)
      if pStartLine >= self.__knitImage.size[1]:
          return

      self.__startLine = pStartLine    

      #Modify Block Counter and fix StartLine if >255
      self.__startBlock = int(self.__startLine/256)
      self.__startLine %= 256
      return
       