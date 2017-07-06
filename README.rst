AYAB
====

All Yarns Are Beautiful

This is the GUI interface for AYAB.

Installation
------------

Linux
~~~~~

Prerequisites
^^^^^^^^^^^^^

You need Python 3.5 and PyQt5 from your package manager's repository.

*For Debian/Ubuntu*

::

    sudo apt-get install python3-pip python3-qt5 python3-dev python3-virtualenv

*For openSUSE*

::

    sudo zypper install python3-pip python3-qt5 python3-virtualenv

*All Distributions*

To be able to communicate with your Arduino, it might be necessary to
add the rights for USB communication by adding your user to some groups.

::

    sudo usermod -a -G tty [userName]
    sudo usermod -a -G dialout [userName]

Release Version
^^^^^^^^^^^^^^^

This will install the latest release version from PyPi

::

    virtualenv -p python3 --system-site-packages venv/
    source venv/bin/activate
    pip3 install ayab

Now, you can start the software with

::

    ayab
