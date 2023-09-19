# AYAB - All Yarns Are Beautiful

This is the GUI interface for AYAB.

For information on how to install the release version of the software, see
[http://manual.ayab-knitting.com](http://manual.ayab-knitting.com)

## Running from Source & Development

### Linux

You need Python 3.5 and from your package manager's repository.
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
    virtualenv -p python3 --system-site-packages venv/
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

You will need brew as package manager, git to acccess github, anaconda for Python 3.5 in an virtual environment

install brew (not needed if git already installed):

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

install git via brew (not needed if git already installed) :

    brew install git

install Xcode command line tools:

    xcode-select --install

get ayab-desktop for eKnitter from github:

    git clone -b ComViaIp https://github.com/yekomS/ayab-desktop ayab-desktop-eknitter

change to ayab-desktop-eknitter directory:

    cd ayab-desktop-eknitter

make directory for anaconda (python virtual environment):

    mkdir -p ~/miniconda3

you can check your mac processor architecture (neede for next command):

    arch

if you use mac with arm processor: get anaconda for arm64 processor:

    curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh

if you use mac with intel processor: get anaconda for x86_64 processor:

    curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o ~/miniconda3/miniconda.sh

install anaconda (python virtual environment): 
    
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3

remove anaconda install script:

    rm -rf ~/miniconda3/miniconda.sh


init anaconda:

    ~/miniconda3/bin/conda init bash
    ~/miniconda3/bin/conda init zsh

restart you terminal window

create python 3.5 virtual environment:

    conda create --name venv -c conda-forge python=3.5 pip

activate python environment:

    conda activate venv

update your python environment with required tools:

    python -m pip install --upgrade pip
    pip install --upgrade setuptools
    pip install -r requirements.txt

To solve pip3 SSL:TLSV1_ALERT_PROTOCOL_VERSION problem (dont know if neccessary):
    
    curl https://bootstrap.pypa.io/get-pip.py | python

start ayab-desktop for eKnitter:

    python3 -m fbs run


once all tools are installed, you can start ayab-desktop for eKnitter:
    
    cd ayab-desktop-eknitter
    conda activate ayab
    python3 -m fbs run

