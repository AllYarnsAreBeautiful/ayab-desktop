# shell/powershell script

# run this script from root directory of repo
# after setting up the Python virtual environment
# to generate additional necessary resources

git submodule update --init --recursive

# convert QT `.ui` files to Python code
pyside6-uic src/main/python/ayab/about_gui.ui -o src/main/python/ayab/about_gui.py
pyside6-uic src/main/python/ayab/firmware_flash_gui.ui -o src/main/python/ayab/firmware_flash_gui.py
pyside6-uic src/main/python/ayab/main_gui.ui -o src/main/python/ayab/main_gui.py
pyside6-uic src/main/python/ayab/menu_gui.ui -o src/main/python/ayab/menu_gui.py
pyside6-uic src/main/python/ayab/mirrors_gui.ui -o src/main/python/ayab/mirrors_gui.py
pyside6-uic src/main/python/ayab/prefs_gui.ui -o src/main/python/ayab/prefs_gui.py
pyside6-uic src/main/python/ayab/engine/dock_gui.ui -o src/main/python/ayab/engine/dock_gui.py
pyside6-uic src/main/python/ayab/engine/options_gui.ui -o src/main/python/ayab/engine/options_gui.py
pyside6-uic src/main/python/ayab/engine/status_gui.ui -o src/main/python/ayab/engine/status_gui.py

# generate PySide6 resource file
pyside6-rcc src/main/python/ayab/ayab_logo_rc.qrc -o src/main/python/ayab/ayab_logo_rc.py

# generate translation files
cd src/main/resources/base/ayab/translations/
perl ayab_trans.pl
cd ../../../../../../
