# -*- coding: utf-8 -*-

import ayab_communication
import ayab_image
import ayab_control

if __name__ == '__main__':
      m_ayabControl = ayab_control.ayabControl()

      m_image = ayab_image.ayabImage("..\..\patterns\uc3.png")
      m_image.showImage()

      m_ayabControl.knitImage(m_image)
