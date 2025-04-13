set VERSION=%1

python -m fbs freeze

python -m fbs installer

xcopy /Y  .\target\AYABSetup.exe .\target\AYAB-eKnitter-v%VERSION%-Setup.exe