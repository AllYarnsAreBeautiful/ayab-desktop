#!/bin/bash
set -e

HERE="`dirname \"$0\"`"
VERSION="$1"
cd "$HERE"

/cygdrive/c/python35/python.exe -m pip install pefile
/cygdrive/c/python35/python.exe -m pip install -r ../requirements.txt

./build.sh $VERSION

