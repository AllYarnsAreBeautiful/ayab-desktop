# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
(at least since version 1.0.0).

## 1.0.0 / Unreleased

* #413 Engine: Add run-time test methods and change required API version to 6 
* GUI: Fix image alignment and placement of limit lines in graphical scene
* #395 GUI: Check for new release on startup
* #393 Documentation: Add forthcoming features to CHANGELOG
* #389 GUI: Rollback to Python3.6, PyQt5==5.9.2
* #379 GUI: Change appearance of menu bar
* #375 Devops: Add script to make PyQt5 files from XML during build
* #371 Documentation: Add need to install avrdude for Linux to README
* #364 Engine: Force engine to communicate with GUI via signals
  to ensure thread safety
* #363 Engine, GUI: Change implementation of finite state machines
* #356 Engine: Add classes for configuration options
* #354 Devops: Add script to make translation files from master during build
* #353 GUI: Add translations for languages other than German
* #348 Engine: Fix color of needles flanking image to background
* #345 GUI: Remove Configure button
* #342 GUI: Add link to documentation in Help-About form
* #338 GUI: Fix crash on knitting restart
* #326 Engine: Change parsing of serial communication
* #311 Engine: Add CRC8 check for serial communication
* #308 Engine: Change representation of pattern from grayscale to color
* #303 GUI: Update Python dependencies
* #301 Devops: Add tests of Python code to CI workflow
* #300 GUI: Add Simulation mode
* #298 GUI: Add ability to load and convert DAK .PAT and .STP files
* #290 GUI: Remove shield test from firmware flash menu
* #289 GUI: Copy pattern files to user directory on startup
* #286 GUI: Improve visibility of icon
* #278,#310 Devops: Add Windows, OSX, and AppImage builds to Github workflow
* #270 GUI: Limit excessive pattern width when transforming image
* #238 GUI: Add preference settings menu item and dialog
* #236 GUI: Add checkbox to options dock for image mirroring
* #226 GUI: Add knit progress area reporting line-by-line graphics
* #208 GUI: Add sound effects at start, end, and new line
* #206 GUI: Add 10 second timeout for firmware flash
* #145 GUI: Add feedback while flashing firmware
* #131,#261 GUI: Add stretch and reflect to image actions submenu
* #155 GUI: Fix scrolling of pattern when scrolling the sidebar

## 0.95 / 2019-01-28

* #280 GUI: Fix crash when pattern is outside left edge
* #271 Engine: Add Heart-of-Pluto Ribber mode (see AYAB manual)
* #259 GUI: Write date and time to the log
* #253 Devops: Fix Mac installation: need OSX 10.12 (Sierra) or newer
* #249 GUI: Fix lace patterns 8-29, 8-30, 8-31, 9-32, 10-33 thru 10-36
* #248 GUI: Show number of completed repeats
* #246 Engine: Reduce carriage turn around time
* #245 GUI: Center patterns with an odd number of stitches on green 1
* #244 Engine: Allow some backwards carriage movement without advancing
  to the next row
* #239 Engine: Add Middle-Color-Twice Ribber mode (see AYAB manual)
* #226 GUI: Show current color in progess bar
* #225 GUI: Enlarge row number in progress bar

## 0.91 / 2018-04-01 [UNRELEASED]

* #251 GUI: Add Repeat image action and shortcuts
* Engine: Add experimental support for Garter Carriage
* Engine: Improve I2C communication (PR #11)
* Engine: Change END_OF_LINE_OFFSET_L to 12 (#9)

## 0.90 / 2017-08-31

* #220 GUI: Check image width before setting pixels
* #211,#212 GUI: Improve image file dialogue
* #205,#207 Engine: Validate number of colors in single and circular mode
* #197 Engine: Fix multicolor ribber knitting
* #191 GUI: Fix image rotation with Pillow 3.0
* #189 GUI: Remove Smart Resize menu option for now
* #167 Engine: Fix start row in ribber infinite knitting
* #166 GUI: Add automatic window maximization on startup
* #162 GUI: Change name of logfile to ayab_log.txt
* #156 GUI: Show filename in status bar
* #153 GUI: Fix automatic setting of start/stop needle for odd image widths
* #148 Engine: Fix ABBA pattern in 2 color ribber infinite mode
* #148 Engine: Fix circular knitting
* #143 Engine: Fix exception during serial port closing
* #141 GUI: Remove progress bar
* #137,#151 GUI: Fix start line spinbox range
* #127 GUI: More verbose user notification when using incompatible firmware
* #126 GUI: Fix handling of spaces in file paths
* Devops: Add OSX App bundle
* Devops: Add Windows 7 and Windows 10 builds
* Engine: New end beep
* Engine: Fix accidental double selection of last row in every knitting mode
* Engine: Add KH910 capability
* GUI: Migrate from Python2 to Python3
* GUI: Migrate from PyQt4 to PyQt5
* GUI: Add custom patterns

## 0.80 / 2015-11-01

* Engine: Migrate to API v4
* Engine: Add test mode
* Engine: Add Auto-Init functionality
* Engine: Add firmware version definition
* Engine: Fix reset of needles out of active needle area
* Engine: Add support for I2C port expander on shield v1.3TH (MCP23008)
* GUI: Add basic visualization of pattern position
* GUI: Add mouse wheel zooming of pattern
* GUI: Add visualization of test mode data
* GUI: Add Auto-Init functionality (no need to click OK several times when
  starting to knit)
* GUI: Move firmware database to external JSON file
* GUI: Fix pattern rotation direction
* GUI: Fix pattern inversion
* GUI: Fix growth of image when rotating
* GUI: Fix unlocking of knit controls after image manipulation

## 0.75 / 2015-02-28

* Engine: Fix lace carriage support

## 0.7 / 2015-02-01

* Engine: Add lace carriage support
* GUI: Show info about current line number
* GUI: Fix some layout issues (e.g. disable UI elements)
* GUI: Start to knit with the bottom of the image
* GUI: Fix progress bar in 2 color doublebed mode
* GUI: Make Start and Stop needle selection as on the machine (orange/green)
* GUI: Add infinite repeat functionality
* GUI: Add Cancel button
