# AYAB

All Yarns Are Beautiful

This is the GUI interface for AYAB.

## Installation

### Linux

#### Prerequisites

You need Python 3.5 and PyQt5 from your package manager's repository.
The other main dependencies can be found in requirements.txt

*For Debian/Ubuntu*

    sudo apt-get install python3-pip python3-qt5 python3-dev python3-virtualenv

*For openSUSE*

    sudo zypper install python3-pip python3-qt5 python3-virtualenv

*All Distributions*

To be able to communicate with your Arduino, it might be necessary to add the rights for USB communication by adding your user to some groups.

    sudo usermod -a -G tty [userName]
    sudo usermod -a -G dialout [userName]

#### Release Version

This will install the latest release version from PyPi

    virtualenv -p python3 --system-site-packages venv/
    source venv/bin/activate
    pip3 install ayab

Now, you can start the software with

    ayab

Instead of installing from the PyPi repository, you can also download the .whl file from the release section and install it like this

    pip3 install <file>.whl

#### Running from Source & Development

To install the development version you can checkout the git repository

    git clone https://github.com/AllYarnsAreBeautiful/ayab-desktop

Create a virtual enviroment in the cloned repository

    cd ayab-desktop
    virtualenv -p python3 --system-site-packages venv/
    source venv/bin/activate
    pip3 install -r requirements.txt

Now start ayab with

    python3 ayab_devel_launch.py

To be able to work on GUI elements and translation files, the Qt Dev tools are needed also:

    qttools5-dev-tools

You can also install directly the git development version using git

    pip3 install -e git+https://github.com/AllYarnsAreBeautiful/ayab-desktop.git#egg=ayab

### Windows

#### Release Version

The Windows version which is available at http://ayab-knitting.com has been packed with
PyInstaller and should not require any additional dependencies.
Just unzip the archive or use the Installer and run

    ayab.exe

#### Running from source & Development (Tested on Win10)

You need Python Version 3.5.3 (Important: the 64 bit version!) and PyQt5 (we used 5.3.2).

Download and install Python 3.5.3 (64 bit) (pip is already contained in this installer) from
    https://www.python.org/downloads/windows/ (https://www.python.org/ftp/python/3.5.3/python-3.5.3-amd64.exe)

You may also need PyWin32 (https://sourceforge.net/projects/pywin32/files/pywin32/).

Now, use pip to install further dependencies

    pip3 install virtualenv pyqt5

You can checkout the git repository with

    git clone https://github.com/AllYarnsAreBeautiful/ayab-desktop

Create a virtual enviroment in the cloned repository

    cd ayab-desktop
    virtualenv --system-site-packages venv/
    venv\Scripts\activate

Then install the remaining prerequisites with

    pip3 install -r requirements.txt

Now start ayab with

    python ayab_devel_launch.py

### macOS

#### Release Version

The macOS version is using a wrapper script to ensure all dependencies are installed.
As a result, the first start might take a while depending on your CPU and internet download speed.
Open the DMG image and copy the app to your Application folder.
Then just run

    AYAB-Launcher.app

and wait for the dependencies to be downloaded and installed.

#### Running from source & Development

You need Python 3.5 and PyQt5.
For Python I would recommend `pyenv`
You can install it using Homebrew

    brew install pyenv

You also need the Xcode command line tools installed.
Once these have been installed, you need to get the Python version installed

    env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.5.0

To install the development version you can checkout the git repository

    git clone https://github.com/AllYarnsAreBeautiful/ayab-desktop

Create a virtual enviroment in the cloned repository

    cd ayab-desktop
    pyvenv venv
    cd venv

Then install the remaining prerequisites with

    bin/pip3 install pyqt5
    bin/pip3 install -r requirements.txt

Now start ayab with

    bin/python3 ayab_devel_launch.py

To be able to work on GUI elements and translation files, the Qt Dev tools are needed also:

    http://download.qt.io/official_releases/online_installers/qt-unified-mac-x64-online.dmg
