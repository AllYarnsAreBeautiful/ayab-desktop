# windows-build

To build a binary from the Python script files, use PyInstaller (pip install pyinstaller) inside the virtualenv:

    cd ayab-desktop
    venv\Scripts\activate
    PyInstaller -y ayab.spec

This will generate a standalone build inside ./dist/ayab
