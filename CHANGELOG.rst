Release Notes
-------------

0.90 (August 2017)
~~~~~~~~~~~~~~~~

Firmware
^^^^^^^^

-  New end beep
-  Fixing accidential double selection of last row (in every knitting mode)

GUI
^^^

-  Migration from Python2 to Python3
-  Migration from PyQt4 to PyQt5
-  OSX App Bundle
-  Windows7 and Windows10 builds
-  Added KH910 and custom patterns
-  Removing Smart Resize menu option for now (#189)
-  Automatically maximising window on startup (#166)
-  Changing filename of logfile to ayab_log.txt (#162)
-  Showing filename in statusbar (#156)
-  Removed progress bar (#141)
-  Making user notification when using incompatible firmware more verbose (#127)
-  checking image width before setting pixels (#220)

Fixes
^^^^^

-  removing unnecessary exception during serial port closing (#143)
-  check for valid number of colors in single and circular mode (#205,#207)
-  improved image file dialogue (#211,#212)
-  fix ABBA pattern in 2 color ribber infinite mode (#148)
-  fixing circular knitting (#148)
-  handling spaces in file paths (#126)
-  fixing multicolor ribber knitting (#197)
-  fixing start row in ribber infinite knitting (#167)
-  fixing image rotation with Pillow 3.0 (#191)
-  fix automatic setting of start/stop needle for odd image widths (#153)
-  fixing start line spinbox range (#151,#137)

0.80 (November 2015)
~~~~~~~~~~~~~~~~~~~~

Firmware
^^^^^^^^

-  API v4
-  Added Test Mode
-  Added Auto-Init functionality
-  Added FW Version Define
-  Fixed reset of needles out of active needle area
-  Added support for I2C port expander on shield v1.3TH (MCP23008)

GUI
^^^

-  requires APIv4
-  Basic visualisation of pattern position
-  Mouse wheel zooming of pattern
-  Visualisation of Test Mode data
-  Auto-Init functionality (no need to click OK several times when
   starting to knit)
-  Firmware database moved to external JSON file
-  Fix pattern rotation direction
-  Fix pattern inversion
-  Fix growth of image when rotating
-  Fix unlocking of knit controls after image manipulation

0.75 (February 2015)
~~~~~~~~~~~~~~~~~~~~

Firmware
^^^^^^^^

-  Fixed Lace carriage support

0.7 (February 2015)
~~~~~~~~~~~~~~~~~~~

Firmware
^^^^^^^^

-  Lace carriage support

GUI
^^^

-  Showing info about current line number
-  Some layout fixes (disabling UI elements, ...)
-  Starting to knit with the bottom of the image
-  Fixed progressbar in 2 color doublebed mode
-  Start and Stop needle selection like on the machine (orange/green)
-  Infinite Repeat functionality
-  Cancel button added
