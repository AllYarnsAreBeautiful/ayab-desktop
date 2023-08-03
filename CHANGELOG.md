# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
(at least since version 1.0.0).

## [Unreleased]

## [1.0.0]

Change in versioning scheme: From now on, the AYAB desktop software and firmware are using the Semantic Versioning 2.0.0 (https://semver.org/) versioning scheme.
Pre-releases are marked with a suffix, e.g. `1.0.0-rc1`, which stands for "release candidate 1"

### Added

- Devops: TEST_GUIDE.md (#546).
- Devops: Mac M1 build documentation (#543).
- Engine: Check for out-of-sequence line number requests (#540).
- Devops: Doxygen documentation of Python code (#519,#522).
- GUI: New menu items and keyboard shortcuts (#517).
- Engine: Run-time test methods and change required API version to 6 (#413).
- GUI: Check for new release on startup (#395).
- Devops: Forthcoming features to CHANGELOG (#393).
- Devops: Script to make PyQt5 files from XML during build (#375).
- Engine: Classes for configuration options (#356).
- Devops: Script to make translation files from master during build (#354).
- GUI: Translations for languages other than German (#353).
- GUI: Link to documentation in Help-About form (#342).
- Engine: CRC8 check for serial communication (#311).
- Devops: Tests of Python code to CI workflow (#301).
- GUI: Simulation mode (#300).
- GUI: Ability to load and convert DAK .PAT and .STP files (#298).
- Devops: Windows, OSX, and AppImage builds to Github workflow (#278,#310).
- GUI: Preference settings menu item and dialog (#238).
- GUI: Checkbox to options dock for image mirroring (#236).
- GUI: Knit progress area reporting line-by-line graphics (#226).
- GUI: Sound effects at start, end, and new line (#208).
- GUI: 10 second timeout for firmware flash (#206).
- GUI: Feedback while flashing firmware (#145).
- GUI: Stretch and reflect to image actions submenu (#131,#261).

### Fixed

- GUI: avrdude command where there is whitespace in the file path (#458,#535,#539).
- Devops: Test workflow (#531,#533).
- GUI: Knitting progress window for knitting modes using ribber (#527,#530).
- GUI: Width of image files by removing needle at 0 (#526,#529,#530).
- GUI: Black line showing knitting progress (#516).
- GUI: Hardware test operation (#515).
- Devops: System calls under Windows (#513).
- GUI: Audio error after knitting finishes (#506,#514).
- Engine: Communication errors logged as debug messages (#498,#499)
- Engine: ReqTest message sending redundant machine type information (#496,#497).
- GUI: Error in audio playback (#492,#495).
- Engine: Typos in FSM (#482).
- GUI: Persistence of test thread after test dialog is closed (#477).
- Devops: Typo in README.md (#475).
- Devops: Missing firmware hex file in AppImage (#472).
- GUI: Firmware flashing utility (#471,#472).
- Devops: Conda command for to set up Python 3.6 environment (#470).
- Engine: Mock communication for knitting operation (#469,#479).
- Engine: Flanking needle color for singlebed mode (#443).
- GUI: Image alignment and placement of limit lines in graphical scene (#404).
- Engine: Color of needles flanking image to background (#348).
- GUI: Crash on knitting restart (#338).
- GUI: Scrolling of pattern when scrolling the sidebar (#155).

### Changed

- Devops: Transition from Python 3.6 to 3.8, update dependencies (#555,#557,#559).
- Devops: Use most recent version of fbs (#554).
- Engine: Log engine state only on change (#537,#538).
- Devops: Establish semantic versioning (#476,#534,#551).
- GUI: Rename modules (#518,#523).
- GUI: Make DockWidget shorter (#511,#512).
- Devops: Rename setup-environment.sh as setup-environment.ps1 (#509,#510).
- GUI: Rename object names (#501,#502).
- Engine: Use API version sent by device (#493).
- Engine: Change indState message (#490).
- Engine: Change tokens to be consistent with APIv6 (#487).
- Devops: Change source file line endings from CRLF to LF (#481).
- Devops: Update CHANGELOG.md (#480,#553).
- Devops: Bundle firmware for desktop application based on a manifest file (#466,#468).
- Devops: Patch python module fbs to fix Windows installer bug (#464).
- Engine: Pass machine type to firmware before attempting to knit (#447).
- Engine: Migrate to API v6 (#411,#420).
- Devops: Change README with instructions to use Miniconda on all platforms (#419).
- GUI: Rollback to Python 3.6, PyQt5==5.9.2 (#389).
- GUI: Change appearance of menu bar (#379).
- Devops: Add need to install avrdude for Linux to README (#371).
- Engine: Force engine to communicate with GUI via signals to ensure thread safety (#364).
- Engine, GUI: Change implementation of finite state machines (#363).
- Engine: Change parsing of serial communication (#326).
- Engine: Change representation of pattern from grayscale to color (#308).
- GUI: Update Python dependencies (#303).
- GUI: Copy pattern files to user directory on startup (#289).
- GUI: Improve visibility of icon (#286).
- GUI: Limit excessive pattern width when transforming image (#270).
- Devops: Migrate from Ubuntu 16.04 to Ubuntu 20.04 for github workflows.

### Removed

- Devops: .gitlab-ci.yml (#558,#560).
- Engine: Blocking while loops in FSM (#541,#542).
- Devops: Out-of-date documentation in docs folder (#520,#521).
- Devops: Support for Arduino Mega (#467).
- Devops: Build of .deb package (#452,#474).
- GUI: Configure button (#345).
- GUI: Shield test from firmware flash menu (#290).

## [0.95] - 2019-01-28

### Added

- Engine: Heart-of-Pluto Ribber mode (see AYAB manual) (#271).
- Engine: Middle-Color-Twice Ribber mode (see AYAB manual) (#239).

### Fixed

- GUI: Crash when pattern is outside left edge (#280).
- Devops: Mac installation: need OSX 10 (#253).12 (Sierra) or newer.
- GUI: Lace patterns 8-29, 8-30, 8-31, 9-32, 10-33 thru 10-36 (#249).

### Changed

- GUI: Write date and time to the log (#259).
- GUI: Show number of completed repeats (#248).
- Engine: Reduce carriage turn around time (#246).
- GUI: Center patterns with an odd number of stitches on green 1 (#245).
- Engine: Allow some backwards carriage movement without advancing to the next row (#244).
- GUI: Show current color in progess bar (#226).
- GUI: Enlarge row number in progress bar (#225).

## [0.91] - 2018-04-01 [UNRELEASED]

### Added

- GUI: Add Repeat image action and shortcuts (#251).
- Engine: Add experimental support for Garter Carriage.

### Changed

- Engine: Improve I2C communication (#11).
- Engine: Change END_OF_LINE_OFFSET_L to 12 (#9).

## [0.90] - 2017-08-31

### Added

- GUI: Automatic window maximization on startup (#166).
- Devops: OSX App bundle.
- Devops: Windows 7 and Windows 10 builds.
- Engine: KH910 capability.
- GUI: Custom patterns.

### Fixed

- Engine: Multicolor ribber knitting (#197).
- GUI: Image rotation with Pillow 3.0 (#191).
- Engine: Start row in ribber infinite knitting (#167).
- GUI: Automatic setting of start/stop needle for odd image widths (#153).
- Engine: ABBA pattern in 2 color ribber infinite mode (#148).
- Engine: Circular knitting (#148).
- Engine: Exception during serial port closing (#143).
- GUI: Start line spinbox range (#137,#151).
- GUI: Handling of spaces in file paths (#126).
- Engine: Accidental double selection of last row in every knitting mode.

### Changed

- GUI: Check image width before setting pixels (#220).
- GUI: Improve image file dialogue (#211,#212).
- Engine: Validate number of colors in single and circular mode (#205,#207).
- GUI: Change name of logfile to ayab_log.txt (#162).
- GUI: Show filename in status bar (#156).
- GUI: More verbose user notification when using incompatible firmware (#127).
- Engine: New end beep.
- GUI: Migrate from Python2 to Python3.
- GUI: Migrate from PyQt4 to PyQt5.

### Removed

- GUI: Remove Smart Resize menu option for now (#189).
- GUI: Remove progress bar (#141).

## [0.80] - 2015-11-01

### Added

- Engine: Test mode.
- Engine: Auto-Init functionality.
- Engine: Firmware version definition.
- Engine: Support for I2C port expander on shield v1.3TH (MCP23008).
- GUI: Basic visualization of pattern position.
- GUI: Mouse wheel zooming of pattern.
- GUI: Visualization of test mode data.

### Fixed

- Engine: Reset of needles out of active needle area.
- GUI: Pattern rotation direction.
- GUI: Pattern inversion.
- GUI: Growth of image when rotating.
- GUI: Unlocking of knit controls after image manipulation.

### Changed

- Engine: Migrate to API v4.
- GUI: Move firmware database to external JSON file.

## [0.75] - 2015-02-28

### Fixed

- Engine: Lace carriage support.

## [0.7] - 2015-02-01

### Added

- Engine: Lace carriage support.
- GUI: Infinite repeat functionality.
- GUI: Cancel button.
* GUI: Show info about current line number.

### Fixed

- GUI: Some layout issues (e.g. disable UI elements).
- GUI: Progress bar in 2 color doublebed mode.

### Changed

- GUI: Start to knit with the bottom of the image.
- GUI: Make Start and Stop needle selection as on the machine (orange/green).
