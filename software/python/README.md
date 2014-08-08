# AYAB

All Yarns Are Beautiful

This is the GUI interface for AYAB.

## Installation

### Development Version

To install the development version you can checkout the git repository. You need Python 2.7 and PyQt from your package manager's repository.
The other main dependencies are: Pillow >= 2.4, pyserial >= 2.7, fysom >= 1.1 and Yapsy >= 1.10
Move to the software/python/ folder and install the required dependencies.

*For Debian/Ubuntu*

    sudo apt-get install python-qt4 python-pip python-dev

*For openSUSE*

    # openSUSE
    sudo zypper install python-pip python-qt4 python-virtualenv

*For Windows*

Download and install Python 2.7.x from
    https://www.python.org/downloads/windows/
Download and install pip from
    https://pip.pypa.io/en/latest/installing.html
Download and install PyQt4 from
    http://www.riverbankcomputing.co.uk/software/pyqt/download

Then create a virtual enviroment on software/python/ with

    virtualenv venv/
    source venv/bin/activate
    pip install -r requirements.txt

