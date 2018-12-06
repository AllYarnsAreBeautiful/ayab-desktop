#!/bin/bash
#
# execute with --user to make pip install in the user home
#
set -e

HERE="`dirname \"$0\"`"
USER="$1"
PACKAGE_VERSION="`cat src/main/resources/base/ayab/package_version`"

python3 -m pip install -r requirements.txt

echo "# build the app"
python3 -m fbs freeze

echo "# create the .dmg file"
python3 -m fbs installer

mkdir -p dist/release
mv target/AYAB.dmg dist/release/AYAB-$PACKAGE_VERSION.dmg
ls -l dist/

AYAB_DMG="`pwd`/dist/release/"
echo "The installer can be found in \"$AYAB_DMG\"."

