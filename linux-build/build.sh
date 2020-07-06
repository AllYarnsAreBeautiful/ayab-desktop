#!/bin/bash
#
#
set -e

PACKAGE_VERSION="`cat src/main/resources/base/ayab/package_version`"

apt install libasound2-dev avrdude

python3 -m pip install -r requirements.txt

# generate translation files
cd src/main/resources/base/ayab/translation
./ayab_trans.pl
lrelease *.ts
cd ../../../../../..

echo "# build the app"
python3 -m fbs freeze

mkdir -p dist/release
tar cfz dist/release/AYAB-Linux-$PACKAGE_VERSION.tar.gz -C target AYAB
