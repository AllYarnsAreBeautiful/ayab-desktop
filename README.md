# AYAB - All Yarns Are Beautiful

This is the GUI interface for AYAB.

For information on how to install the release version of the software, see
[http://manual.ayab-knitting.com](http://manual.ayab-knitting.com)

## Running from Source & Development

The AYAB desktop software runs using Python 3.6. This is not the current
version of Python, so it is recommended to install the software to a
virtual environment. Miniconda provides a virtual environment that is
platform-independent and easy to use: download the lastest version from
https://docs.conda.io/en/latest/miniconda.html and follow the instructions
for installation.

The Python module dependencies can be found in *requirements.txt*.

This repository uses [pre-commit](https://pre-commit.com/) hooks.
After cloning the repo and installing the requirements, you should run
`pre-commit install` to set up the git hook scripts.

### Linux

For flashing the firmware, avrdude has to be available on your system.
To be able to work on GUI elements and translation files, the Qt Dev tools are
needed also.

#### Debian/Ubuntu

    sudo apt-get install python3-pip python3-dev python3-virtualenv python3-gi
    sudo apt-get install libasound2-dev avrdude qttools5-dev-tools
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get install python3.6 python3.6-dev

It may be necessary 

#### For openSUSE

    sudo zypper install python3-pip python3-virtualenv python3-gi
    sudo zypper install libasound avrdude qttools5-dev-tools

#### All Distributions

To be able to communicate with your Arduino, it might be necessary to add the
rights for USB communication by adding your user to some groups.

    sudo usermod -aG tty [userName]
    sudo usermod -aG dialout [userName]

To install the development version you can checkout the git repository.

    git clone https://github.com/AllYarnsAreBeautiful/ayab-desktop

Create a virtual enviroment in the cloned repository:

    cd ayab-desktop
<<<<<<< HEAD
    conda create --name venv -c conda-forge python=3.6.* pip
    source activate venv
=======
    virtualenv --python=/usr/bin/python3.6 --system-site-packages venv/
    source venv/bin/activate
    python3 -m pip install --upgrade pip
<<<<<<< HEAD
>>>>>>> b9abee6... Updated instructions for Ubuntu in README.md
=======
>>>>>>> b9abee6... Updated instructions for Ubuntu in README.md
    pip3 install -r requirements.txt
    ./setup-environment.sh

Now start ayab with

    python3 -m fbs run

### Windows

Download and run the Git for Windows installer from https://git-scm.com/download/win
 
Now you can download the git repository from the Anaconda prompt with:

    git clone https://github.com/AllYarnsAreBeautiful/ayab-desktop

Create a virtual enviroment in the cloned repository:

    cd ayab-desktop
    conda create --name venv -c conda-forge python=3.6.* pip
    conda activate venv

Then install the remaining prerequisites with:

    pip install -r requirements.txt
    ./setup-environment.sh

Now start ayab with

    python -m fbs run

### macOS

You can install Git using Homebrew:

    brew install git

You will also need the Xcode command line tools:

    xcode-select --install

Next download the git repository:

    git clone https://github.com/AllYarnsAreBeautiful/ayab-desktop

Create a virtual enviroment in the cloned repository.

    cd ayab-desktop
    conda create --name venv -c conda-forge python=3.6.* pip
    source activate venv

Then install the remaining prerequisites with:

    pip3 install -r requirements.txt

To solve pip3 SSL:TLSV1_ALERT_PROTOCOL_VERSION problem:

    curl https://bootstrap.pypa.io/get-pip.py | python3

To be able to work on GUI elements and translation files, the Qt Dev tools are needed also:

    http://download.qt.io/official_releases/online_installers/qt-unified-mac-x64-online.dmg

Finally, convert the PyQt5 `.ui` files and generate the translation files:

    ./setup-environment.sh

Now start ayab with

    python3 -m fbs run
