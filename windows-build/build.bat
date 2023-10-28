set VERSION=%1

rem echo "# build the app"
python -m fbs freeze

rem echo "# create the installer"
python -m fbs installer

xcopy /Y  .\target\AYABSetup.exe .\target\AYAB-eKnitter-v%VERSION%-Setup.exe