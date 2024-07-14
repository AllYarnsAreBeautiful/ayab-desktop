# AYAB - All Yarns Are Beautiful

This is the GUI interface for AYAB.

For information on how to install the release version of the software, see
[http://manual.ayab-knitting.com](http://manual.ayab-knitting.com)

## Running from Source & Development

The AYAB desktop software runs using Python 3.11.  
The Python module dependencies are split across **runtime dependencies**, which are in *requirements.build.txt* and **development dependencies**, found in *requirements.txt*.

This repository uses [pre-commit](https://pre-commit.com/) hooks.
After cloning the repo and installing the development dependencies, you should run
`pre-commit install` to set up the git hook scripts.
### Platform-Specific Setup
<details>
    <summary>
        Linux
    </summary>

For flashing the firmware, avrdude has to be available on your system.
To build or run the application, you will also need the system libraries required by Qt 6; installing the Qt 6 development tools is a concise (if heavy-handed) way of bringing in these dependencies.

#### Debian/Ubuntu
```bash
    sudo apt install python3.11 python3.11-dev python3.11-venv
    sudo apt install libasound2-dev avrdude qt6-tools-dev-tools build-essential
```
#### openSUSE
```bash
    sudo zypper install python311 python311-pip python311-virtualenv python311-devel
    sudo zypper install libasound2 alsa-devel avrdude qt6-tools-dev-tools build-essential
```
#### All Distributions

To be able to communicate with your Arduino, it might be necessary to add the
rights for USB communication by adding your user to some groups.
```bash
    sudo usermod -aG tty [userName]
    sudo usermod -aG dialout [userName]
```
</details>

<details>
    <summary>
        Windows
    </summary>

AYAB requires Windows version 10 or later.

Run Anaconda Powershell as administrator and install git.
```ps
    conda install git
```
Now you can download the git repository with:
```ps
    git clone https://github.com/AllYarnsAreBeautiful/ayab-desktop
    cd ayab-desktop
```
Next, create a virtual environment for AYAB:
```ps
    conda create --name ayab -c conda-forge python=3.11 pip
```
Activate the virtual environment. The command prompt should now display
`(ayab)` at the beginning of each line.
```ps
    conda activate ayab
```
(You may skip the virtual environment setup below.)

You will also need to download and install Perl from [https://www.perl.org/get.html](https://www.perl.org/get.html).
</details>

<details>
<summary>
macOS
</summary>

You can install Git using Homebrew:
```bash
    brew install git
```
You will also need the Xcode command line tools:
```bash
    xcode-select --install
```
Install python from [the official universal2 installer](https://www.python.org/ftp/python/3.11.8/python-3.11.8-macos11.pkg). (Conda does not produce universal binaries)  

If you encounter the pip `SSL:TLSV1_ALERT_PROTOCOL_VERSION` problem:
```bash
    curl https://bootstrap.pypa.io/get-pip.py | python
```
</details>

### Universal Setup Steps
Once platform-specific setup is complete, download the git repository:
```bash
    git clone https://github.com/AllYarnsAreBeautiful/ayab-desktop
    cd ayab-desktop
```
Create a virtual environment for AYAB:
```bash
    python3.11 -m venv .venv 
```
Now activate the virtual environment. The command prompt should now display
`(.venv)` at the beginning of each line.
```bash
    source .venv/bin/activate
```
Install the remaining prerequisites with:
```bash
    python -m pip install --upgrade pip
    pip install --upgrade setuptools
    pip install -r requirements.txt
```

Next, convert the PySide6 `.ui` files and generate the translation files:
```bash
    bash ./setup-environment.ps1
```

Finally, you can start AYAB with
```bash
    fbs run
```

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
