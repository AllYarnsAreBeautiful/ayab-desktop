#!/bin/bash
#
#
set -e

PACKAGE_VERSION="`cat src/main/resources/base/ayab/package_version`"

python3 -m pip install -r requirements.txt

echo "# build the app"
python3 -m fbs freeze

echo "# create the installer"
python3 -m fbs installer

mkdir -p dist/release
tar cfz dist/release/AYAB-Linux-$PACKAGE_VERSION.tar.gz -C target AYAB
