# windows-build

To build a binary from the Python script files, use PyInstaller (pip install pyinstaller) inside the virtualenv:

    cd ayab-desktop
    venv\Scripts\activate
    PyInstaller -y ayab.spec

This will generate a standalone build inside ./dist/ayab

We use `pyinstaller <https://pyinstaller.readthedocs.io/>`__ to create the
binaries.
`Inno Setup 5 <http://www.jrsoftware.org/isinfo.php>`__ is used to build the
installer. Note that Inno Setup 5 has its own license attached.
