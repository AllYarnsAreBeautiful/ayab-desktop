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
/cygdrive/c/python35/python.exe -m PyInstaller -y ayab.spec
cd windows-build

echo "# create the installer"
AYAB_EXE="`pwd`/../dist/release//AYAB-Windows$VERSION-$PACKAGE_VERSION-Setup.exe"
chmod -R 770 Inno\ Setup\ 5/
sed -i "s/PACKAGE_VERSION/$PACKAGE_VERSION/g" ayab.iss
Inno\ Setup\ 5/ISCC.exe -FAYAB-$PACKAGE_VERSION-windows$VERSION-setup /O../dist/release/ ayab.iss
7z a -tzip ../dist/release/AYAB-$PACKAGE_VERSION-windows$VERSION.zip "../dist/ayab/*"
ls -l ../dist/

echo "The installer can be found in \"$AYAB_EXE\"."

