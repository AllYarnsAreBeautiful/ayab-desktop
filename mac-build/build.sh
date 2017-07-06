#!/bin/bash
#
# execute with --user to make pip install in the user home
#
set -e

HERE="`dirname \"$0\"`"
USER="$1"
PACKAGE_VERSION="`cat ./package_version`"
cd "$HERE"

mkdir -p ../dist/release

echo "# build the app"
/usr/local/bin/platypus -x -P AYAB.platypus -V $PACKAGE_VERSION -Y AYAB-Launcher -y ../dist/AYAB-Launcher

echo "# create the .dmg file"
AYAB_DMG="`pwd`/../dist/release/AYAB.dmg"
rm -f "$AYAB_DMG"
ls -l ../dist/
dmgbuild -s dmg_settings.py AYAB "$AYAB_DMG"

echo "The installer can be found in \"$AYAB_DMG\"."

