#!/bin/bash
#
# execute with --user to make pip install in the user home
#
set -e

HERE="`dirname \"$0\"`"
USER="$1"
cd "$HERE"

(
  cd ..

  echo "# build the distribution"
  python setup.py sdist
)

pwd
ls

echo "# build the app"
cp ayab.spec ../
cd ..
# see https://pythonhosted.org/PyInstaller/usage.html
python -m PyInstaller -d -y ayab.spec

echo "# create the .dmg file"
# see http://stackoverflow.com/a/367826/1320237
AYAB_DMG="`pwd`/dist/AYAB.dmg"
rm -f "$AYAB_DMG"
hdiutil create -srcfolder dist/ayab.app "$AYAB_DMG"

echo "The installer can be found in \"$AYAB_DMG\"."

