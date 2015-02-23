# AYAB

All Yarns Are Beautiful

This is the GUI interface for AYAB.

## Installation

### Linux

#### Prerequisites

*For Debian/Ubuntu*

    sudo apt-get install python-pip python-qt4 python-dev

*For openSUSE*

    # openSUSE
    sudo zypper install python-pip python-qt4 python-virtualenv

#### Setup

Create a virtual enviroment (e.g. in $HOME/ayab/) and install ayab with

    virtualenv --system-site-packages venv/
    source venv/bin/activate
    pip install ayab

Start ayab with
    ayab

### Windows

The Windows version which is available at http://ayab-knitting.com has been packed with py2exe and should not require
any additional dependencies. Just unzip the archive to C:\ayab-apparat-0.7 and
start ayab.exe

### Development

To install the development version you can checkout the git repository. You need Python 2.7 and PyQt from your package manager's repository.
The other main dependencies are: Pillow >= 2.4, pyserial >= 2.7, fysom >= 1.1 and Yapsy >= 1.10
Move to the software/python/ folder and install the required dependencies.

#### Development Dependencies for Linux

pyqt4-dev-tools 

#### Development Dependencies for Windows

Download and install Python 2.7.x from
    https://www.python.org/downloads/windows/
Download and install pip from
    https://pip.pypa.io/en/latest/installing.html
Download and install PyQt4 from
    http://www.riverbankcomputing.co.uk/software/pyqt/download

## Release Notes

### 0.75 (February 2015)

#### Firmware

* Fixed Lace carriage support

### 0.7 (February 2015)

#### Firmware

* Lace carriage support

#### GUI

* Showing info about current line number
* Some layout fixes (disabling UI elements, ...)
* Starting to knit with the bottom of the image
* Fixed progressbar in 2 color doublebed mode
* Start and Stop needle selection like on the machine (orange/green)
* Infinite Repeat functionality
* Cancel button added
