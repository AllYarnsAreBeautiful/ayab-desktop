===============
Building AYAB
===============


Build process for Development
-----------------------------

AYAB's GUI is built in Python, based on PyQt4. To develop for it, you must have a set of packages installed.

* Python 2.7+ (Python 3 is not yet supported.)
* PyQt4
* PySerial
* Fysom
* Yapsy
* Pillow (PIL)

You can install most of this packages (except for Python 2.7 and PyQt4) either using your distribution's package manager or using Pip if available. The full list of requirements is available on the ``requirements.txt`` file on the software directory. The ``setup.py`` file also includes the dependencies that can be instaled via pip so you can install using a Virtual Enviroment.

If you are in Windows, you can either install `Python for Windows <https://www.python.org/downloads/windows/>`_, `PyQt4 for Windows <http://winpython.sourceforge.net/>`_ and `pip and easy_install <http://docs.python-guide.org/en/latest/starting/install/win/>`_. An easier alternative is installing a bundle such as `WinPython <http://winpython.sourceforge.net/>`_.

After installing all requirements, you can run AYAB directly using ``python2 ayab_devel_launch.py``.

To build you can use ``python setup.py sdist``. It will generate a .tar.gz file on ``dist/``. This is a tar.gz file that you can install using easy_install or the bundled ``setup.py``.


Build process for Deploy
-----------------------------

Windows packages are built using py2exe ``python setup.py py2exe``.
