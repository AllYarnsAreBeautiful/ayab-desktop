set VERSION=%1

python -m fbs freeze

python -m fbs installer

xcopy /Y  .\target\AYAB-eKnitterSetup.exe .\target\AYAB-eKnitter-v%VERSION%-Setup.exe