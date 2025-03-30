# shell/powershell script

# run this script from root directory of repo
# after setting up the Python virtual environment
# to generate additional necessary resources

git submodule update --init --recursive

# generate PySide6 types
pyside6-genpyi all

# convert Qt `.ui` files to Python code
pyside6-uic src/main/python/main/ayab/about_gui.ui -o src/main/python/main/ayab/about_gui.py
perl -pi -e "s/^(.*def setupUi.*):$/\1->None:/s" src/main/python/main/ayab/about_gui.py
pyside6-uic src/main/python/main/ayab/firmware_flash_gui.ui -o src/main/python/main/ayab/firmware_flash_gui.py
perl -pi -e "s/^(.*def setupUi.*):$/\1->None:/s" src/main/python/main/ayab/firmware_flash_gui.py
pyside6-uic src/main/python/main/ayab/main_gui.ui -o src/main/python/main/ayab/main_gui.py
perl -pi -e "s/^(.*def setupUi.*):$/\1->None:/s" src/main/python/main/ayab/main_gui.py
pyside6-uic src/main/python/main/ayab/menu_gui.ui -o src/main/python/main/ayab/menu_gui.py
perl -pi -e "s/^(.*def setupUi.*):$/\1->None:/s" src/main/python/main/ayab/menu_gui.py
pyside6-uic src/main/python/main/ayab/mirrors_gui.ui -o src/main/python/main/ayab/mirrors_gui.py
perl -pi -e "s/^(.*def setupUi.*):$/\1->None:/s" src/main/python/main/ayab/mirrors_gui.py
pyside6-uic src/main/python/main/ayab/prefs_gui.ui -o src/main/python/main/ayab/prefs_gui.py
perl -pi -e "s/^(.*def setupUi.*):$/\1->None:/s" src/main/python/main/ayab/prefs_gui.py
pyside6-uic src/main/python/main/ayab/engine/dock_gui.ui -o src/main/python/main/ayab/engine/dock_gui.py
perl -pi -e "s/^(.*def setupUi.*):$/\1->None:/s" src/main/python/main/ayab/engine/dock_gui.py
pyside6-uic src/main/python/main/ayab/engine/options_gui.ui -o src/main/python/main/ayab/engine/options_gui.py
perl -pi -e "s/^(.*def setupUi.*):$/\1->None:/s" src/main/python/main/ayab/engine/options_gui.py
pyside6-uic src/main/python/main/ayab/engine/status_gui.ui -o src/main/python/main/ayab/engine/status_gui.py
perl -pi -e "s/^(.*def setupUi.*):$/\1->None:/s" src/main/python/main/ayab/engine/status_gui.py


# generate PySide6 resource filea
pyside6-rcc src/main/python/main/ayab/ayab_logo_rc.qrc -o src/main/python/main/ayab/ayab_logo_rc.py
pyside6-rcc src/main/python/main/ayab/engine/lowercase_e_rc.qrc -o src/main/python/main/ayab/engine/lowercase_e_rc.py
pyside6-rcc src/main/python/main/ayab/engine/lowercase_e_reversed_rc.qrc -o src/main/python/main/ayab/engine/lowercase_e_reversed_rc.py

pyside6-rcc src/main/python/main/ayab/engine/eKnitter_rc.qrc -o src/main/python/main/ayab/engine/eKnitter_rc.py
pyside6-rcc src/main/python/main/ayab/engine/eKnitter_reversed_rc.qrc -o src/main/python/main/ayab/engine/eKnitter_reversed_rc.py

# generate translation files
cd src/main/resources/base/ayab/translations/
perl ayab_trans.pl
cd ../../../../../../
