# AYAB - All Yarns Are Beautiful

This is the GUI interface for AYAB.

For information on how to install the release version of the software, see
[http://manual.ayab-knitting.com](http://manual.ayab-knitting.com)

## Running from Source & Development

### Linux

You need Python 3.7 and from your package manager's repository.
The other main dependencies can be found in requirements.txt

*For Debian/Ubuntu*

    sudo apt-get install python3-pip python3-dev python3-virtualenv python3-gi

*For openSUSE*

    sudo zypper install python3-pip python3-virtualenv python3-gi

*All Distributions*

To be able to communicate with your Arduino, it might be necessary to add the rights for USB communication by adding your user to some groups.

    sudo usermod -a -G tty [userName]
    sudo usermod -a -G dialout [userName]

To install the development version you can checkout the git repository

    git clone https://github.com/AllYarnsAreBeautiful/ayab-desktop

Create a virtual enviroment in the cloned repository

    cd ayab-desktop
    virtualenv --python=/usr/bin/python3.7 --system-site-packages venv/
    source venv/bin/activate
    pip3 install -r requirements.txt

Now start ayab with

    python3 -m fbs run

To be able to work on GUI elements and translation files, the Qt Dev tools are needed also:

    sudo apt-get install qttools5-dev-tools

### Windows

You need Python Version 3.5.3 (Important: the 64 bit version!) and PyQt5 (we used 5.11.3).

Download and install Python 3.5.3 (64 bit) (pip is already contained in this installer) from
    https://www.python.org/downloads/windows/ (https://www.python.org/ftp/python/3.5.3/python-3.5.3-amd64.exe)

You may also need PyWin32 (https://sourceforge.net/projects/pywin32/files/pywin32/).

You can checkout the git repository with

    git clone https://github.com/AllYarnsAreBeautiful/ayab-desktop

Create a virtual enviroment in the cloned repository

    cd ayab-desktop
    virtualenv venv/
    venv\Scripts\activate

Then install the remaining prerequisites with

    pip3 install -r requirements.txt

Now start ayab with

    python -m fbs run

### macOS

You need Python 3.5.3 and PyQt5.
For Python I would recommend `pyenv`
You can install it using Homebrew

    brew install pyenv
    brew install pyenv-virtualenv

You also need the Xcode command line tools installed (xcode-select --install).
Once these have been installed, you need to get the Python version installed

    env PYTHON_CONFIGURE_OPTS="--enable-framework" CFLAGS="-I$(xcrun --show-sdk-path)/usr/include" pyenv install 3.5.3

To install the development version you can checkout the git repository

    git clone https://github.com/AllYarnsAreBeautiful/ayab-desktop

Create a virtual enviroment in the cloned repository

    cd ayab-desktop
    pyenv virtualenv 3.5.3 venv
    pyenv activate venv

(If the pyenv commands don't work out, you probably have to add

    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"

to your ~/.bash_profile)

Then install the remaining prerequisites with

    pip3 install -r requirements.txt

To solve pip3 SSL:TLSV1_ALERT_PROTOCOL_VERSION problem:

    curl https://bootstrap.pypa.io/get-pip.py | python3

Now start ayab with

    python3 -m fbs run

To be able to work on GUI elements and translation files, the Qt Dev tools are needed also:

    http://download.qt.io/official_releases/online_installers/qt-unified-mac-x64-online.dmg
