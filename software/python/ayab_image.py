# -*- coding: utf-8 -*-

import Image

class ayabImage(object):
  def __init__(self, pFilename, pNumColors):
    self.__numColors      = pNumColors

    self.__imgPosition    = 'center'
    self.__imgStartNeedle = '0'
    self.__imgStopNeedle  = '0'

    self.__knitStartNeedle = 80
    self.__knitStopNeedle  = 119

    self.__startLine  = 0
    self.__startBlock = 0

    self.__image = Image.open(pFilename)
    self.__filename  = pFilename

    self.__image = self.__image.convert('L') # convert to 1 byte depth
    self.__updateImageData()


  def filename(self):
    return self.__filename

  def imageIntern(self):
    return self.__imageIntern

  def imgWidth(self):
    return self.__imgWidth

  def imgHeight(self):
    return self.__imgHeight

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


  def __updateImageData(self):
    self.__imgWidth   = self.__image.size[0]
    self.__imgHeight  = self.__image.size[1]      

    self.__convertImgToIntern()
    self.__calcImgStartStopNeedles()


  def __convertImgToIntern(self): 
    num_colors = self.__numColors
    clr_range  = float(256)/num_colors

    imgWidth   = self.__imgWidth
    imgHeight  = self.__imgHeight
    
    self.__imageIntern = \
      [[0 for i in range(imgWidth)] \
      for j in range(imgHeight)]
    self.__imageColors = \
      [[0 for i in range(num_colors)] \
      for j in range(imgHeight)]
    self.__imageExpanded = \
      [[0 for i in range(imgWidth)] \
      for j in range(4*imgHeight)]

    # Distill image to x colors
    for row in range(0, imgHeight):
      for col in range(0, imgWidth):
        pxl = self.__image.getpixel((col, row))

        for color in range(0, num_colors):
          lowerBound = int(color*clr_range)
          upperBound = int((color+1)*clr_range) 
          if pxl>=lowerBound and pxl<upperBound:
            # color map
            self.__imageIntern[row][col]    = color
            # amount of bits per color per line
            self.__imageColors[row][color]  += 1
            # colors separated per line
            self.__imageExpanded[(4*row)+color][col] = 1
    
    # print(self.__imageIntern)
    # print(self.__imageColors)
    # print(self.__imageExpanded)


  def __calcImgStartStopNeedles(self):
    # TODO improve error handling in case of invalid values
    if self.__imgPosition == 'center':
        needleWidth = (self.__knitStopNeedle - self.__knitStartNeedle) +1
        self.__imgStartNeedle = (self.__knitStartNeedle + needleWidth/2) - self.__image.size[0]/2
        self.__imgStopNeedle  = self.__imgStartNeedle + self.__image.size[0] -1      

    elif self.__imgPosition == 'left':
        self.__imgStartNeedle = self.__knitStartNeedle
        self.__imgStopNeedle  = self.__imgStartNeedle + self.__image.size[0]

    elif self.__imgPosition == 'right':
        self.__imgStopNeedle  = self.__knitStopNeedle
        self.__imgStartNeedle = self.__imgStopNeedle - self.__image.size[0]

    elif int(self.__imgPosition) > 0 and int(self.__imgPosition) < 200:
        self.__imgStartNeedle = int(self.__imgPosition)
        self.__imgStopNeedle  = self.__imgStartNeedle + self.__image.size[0]

    else:
        return False
    return True


  def invertImage(self):
      """
      invert the pixels of the image
      """
      for y in range(0, self.__image.size[1]):
        for x in range(0, self.__image.size[0]):
          pxl = self.__image.getpixel((x, y))
          if pxl == 255:
            self.__image.putpixel((x,y),0)
          else:
            self.__image.putpixel((x,y),255)
      self.__updateImageData()
      

  def rotateImage(self):
      """
      rotate the image 90 degrees clockwise
      """
      print "rotating image 90 degrees..."
      self.__image = self.__image.rotate(-90)

      self.__updateImageData()


  def resizeImage(self, pNewWidth):
      """
      resize the image to a given width, keeping the aspect ratio
      """
      wpercent = (pNewWidth/float(self.__image.size[0]))
      hsize = int((float(self.__image.size[1])*float(wpercent)))
      self.__image = self.__image.resize((pNewWidth,hsize), Image.ANTIALIAS)

      self.__updateImageData()


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
      if pStartLine >= self.__image.size[1]:
          return

      self.__startLine = pStartLine    

      #Modify Block Counter and fix StartLine if >255
      self.__startBlock = int(self.__startLine/256)
      self.__startLine %= 256
      return