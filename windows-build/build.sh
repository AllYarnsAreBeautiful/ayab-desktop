#!/bin/bash
set -e

HERE="`dirname \"$0\"`"
VERSION="$1"
PACKAGE_VERSION="`cat ../package_version`"
cd "$HERE"

mkdir -p ../dist/release

echo "# build the app"
cd ..
cp package_version LICENSE.txt ayab/
cp LICENSE.txt windows-build/
/cygdrive/c/python35/python.exe -m fbs freeze

echo "# create the installer"
/cygdrive/c/python35/python.exe -m fbs installer

AYAB_EXE="`pwd`/dist/release/"
cp target/AYABSetup.exe dist/release/AYAB-Windows$VERSION-$PACKAGE_VERSION-Setup.exe
7z a -tzip ../dist/release/AYAB-$PACKAGE_VERSION-windows$VERSION.zip "target/AYAB/*"
ls -l ../dist/

echo "The installer can be found in \"$AYAB_EXE\"."

