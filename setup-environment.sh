#!/bin/sh

# run this script from root directory of repo
# after setting up the Python virtual environment
# to generate additional necessary resources

# convert PyQt5 `.ui` files to Python code
cd src/main/python/ayab
pyuic5 about_gui.ui -o about_gui.py
pyuic5 firmware_flash_gui.ui -o firmware_flash_gui.py
pyuic5 main_gui.ui -o main_gui.py
pyuic5 menu_gui.ui -o menu_gui.py
pyuic5 mirrors_gui.ui -o mirrors_gui.py
pyuic5 prefs_gui.ui -o prefs_gui.py
pyuic5 engine/dock_gui.ui -o engine/dock_gui.py
pyuic5 engine/options_gui.ui -o engine/options_gui.py
pyuic5 engine/status_gui.ui -o engine/status_gui.py

# generate PyQt5 resource file
pyrcc5 ayab_logo_rc.qrc -o ayab_logo_rc.py

# generate translation files
cd -
cd src/main/resources/base/ayab/translations/
./ayab_trans.pl
