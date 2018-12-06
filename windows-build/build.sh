#!/bin/bash
set -e

HERE="`dirname \"$0\"`"
VERSION="$1"
PACKAGE_VERSION="`cat src/main/resources/base/ayab/package_version`"

python -m pip install -r requirements.txt

echo "# build the app"
python -m fbs freeze

echo "# create the installer"
python -m fbs installer

mkdir -p dist/release
AYAB_EXE="`pwd`/dist/release/"
cp target/AYABSetup.exe dist/release/AYAB-Win$VERSION-$PACKAGE_VERSION-Setup.exe
7z a -tzip dist/release/AYAB-Win$VERSION-$PACKAGE_VERSION.zip "target/AYAB/*"
ls -l dist/release

echo "The installer can be found in \"$AYAB_EXE\"."

