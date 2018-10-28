# windows-build

To build a binary from the Python script files, use PyInstaller (pip install pyinstaller) inside the virtualenv:

    cd ayab-desktop
    venv\Scripts\activate
    python3 -m fbs freeze

This will generate a standalone build inside target/AYAB
To build the NSIS installer, run 
    
    python3 -m fbs installer

(NSIS must be on the Windows PATH)
