#!/bin/bash
set -e

HERE="`dirname \"$0\"`"
USER="$1"
cd "$HERE"

mkdir -p /usr/local/share/platypus/
cp -R platypus/share/* /usr/local/share/platypus/
cp platypus/platypus /usr/local/bin/
pip install dmgbuild
cp ../package_version ../LICENSE ../ayab/

./build.sh $USER

