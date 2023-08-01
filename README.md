# AYAB - All Yarns Are Beautiful

This is the GUI interface for AYAB.

For information on how to install the release version of the software, see
[http://manual.ayab-knitting.com](http://manual.ayab-knitting.com)

## Running from Source & Development

The AYAB desktop software runs using Python 3.8. This is not the current
version of Python, so it is recommended to install the software to a
virtual environment. Miniconda provides a virtual environment that is
platform-independent and easy to use: download the lastest version from
https://docs.conda.io/en/latest/miniconda.html and follow the installation
instructions for your operating system.

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
    cd ayab-desktop

Create a virtual environment for AYAB:

    conda create --name ayab -c conda-forge python=3.8 pip

Now activate the virtual environment. The command prompt should now display
`(ayab)` at the beginning of each line.

    conda activate ayab

Install the remaining prerequisites.

    python -m pip install --upgrade pip
    pip install --upgrade setuptools
    pip install --ignore-installed -r requirements.txt
    bash setup-environment.ps1

Now start AYAB with

    fbs run

### Windows

Run Anaconda Powershell as administrator and install git.

    conda install git

Now you can download the git repository with:

    git clone https://github.com/AllYarnsAreBeautiful/ayab-desktop
    cd ayab-desktop

Next, create a virtual environment for AYAB:

    conda create --name ayab -c conda-forge python=3.8 pip

Activate the virtual environment. The command prompt should now display
`(ayab)` at the beginning of each line.

    conda activate ayab

Install the prerequisite Python modules.

    python -m pip install --upgrade pip
    pip install --upgrade setuptools
    pip install --ignore-installed -r requirements.txt

To be able to work on GUI elements and translation files, the Qt Dev tools are needed.
Navigate to https://www.qt.io/download in a web browser and follow the installation
instructions. From the available options, select "Custom install" and then "Qt 5.15.2".
Then convert the PyQt5 `.ui` files and generate the translation files:

    .\setup-environment.ps1

Now start AYAB with:

    fbs run

### macOS

*If on Apple Silicon (M1 & M2 chips)*

* You will need to install the virtual environment using the x86_64 versions of packages due to the requirement of Python 3.8 (which has no build in Conda due to it predating Apple silicon). In order to do this, you need to set the terminal to fetch packages built for x86_64 architectures rather than the native arm64. In Applications, go to the Utilities folder and right click on the Terminal app, and choosing `Get Info`. Select the `Open using Rosetta` checkbox and close the window. Check that the change has taken place by opening the terminal and entering the command `arch`. This should return `i386` if everything went correctly.
* Installing both native and rosetta versions of packages can cause conflicts. You can remove conflicting packages from homebrew by specifying architecture and using the remove command: `arch=arm64 brew remove xyz`.

You can install Git using Homebrew:

    brew install git

You will also need the Xcode command line tools:

    xcode-select --install

Next download the git repository:

    git clone https://github.com/AllYarnsAreBeautiful/ayab-desktop
    cd ayab-desktop

Create a virtual environment for AYAB:

    conda create --name ayab -c conda-forge python=3.8 pip

Now activate the virtual environment. The command prompt should now display
`(ayab)` at the beginning of each line.

    conda activate ayab

Then install the remaining prerequisites with:

    python -m pip install --upgrade pip
    pip install --upgrade setuptools
    pip install -r requirements.txt

To solve pip SSL:TLSV1_ALERT_PROTOCOL_VERSION problem:

    curl https://bootstrap.pypa.io/get-pip.py | python

To be able to work on GUI elements and translation files, the Qt Dev tools are needed also:

    https://download.qt.io/archive/qt/5.12/5.12.12/qt-opensource-mac-x64-5.12.12.dmg

Finally, convert the PyQt5 `.ui` files and generate the translation files:

    ./setup-environment.ps1

If you get errors about missing `lrelease`, you can skip this if you do not need the translation files. To do so, comment out lines [23:26] of `setup-environment.ps1`.

Now start AYAB with

    fbs run

## CI/CD on GitHub

### Triggering a new build

A new build is triggered when a new tag is created, either starting with

* v (i.e. v1.0.0), or
* test (i.e. test230517)

Convention for the test-tag is to suffix the current date in the YYMMdd format. If there is already an existing test build for a single day, attach a letter.
The test tags and releases will be manually removed from time for a better overview.

The tag can be pushed from your local environment, or via the ["Draft a new Release"](https://github.com/AllYarnsAreBeautiful/ayab-desktop/releases/new) button on the GitHub website.

### Choosing the firmware release to be bundled with the build

The CI automatically downloads a given firmware release from the [ayab-firmware repo](https://github.com/AllYarnsAreBeautiful/ayab-firmware) and packs it into the Desktop release. The name of the firmware release is chosen in [this manifest file](https://github.com/AllYarnsAreBeautiful/ayab-desktop/blob/1.0.0-dev/src/main/resources/base/ayab/firmware/manifest.txt) in the ayab-desktop repo.

Whenever building from source, you should ensure that the firmware is available as a compiled hex file is available at `main/resources/base/ayab/firmware/firmware.hex`. You can either compile the firmware and upload it through other means (e.g. VSCode with PlatformIO), or compile and then drop it into the right path in the desktop directory, making it available for the flash through AYAB desktop.
