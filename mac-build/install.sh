#!/bin/bash
#
# execute with --user to pip install in the user home
#
set -e

HERE="`dirname \"$0\"`"
USER="$1"
cd "$HERE"

echo "# brew --cache"
brew --cache
echo "# brew update"
brew update
echo "# install Python3"
brew install python3
echo "# install PyQt5"
brew install PyQt5

echo -n "Python version: "
python3 --version
python3 -m pip install --upgrade pip

echo "# install requirements"
python3 -m pip install $USER -r ../requirements.txt
python3 -m pip install $USER PyInstaller

./build.sh $USER

