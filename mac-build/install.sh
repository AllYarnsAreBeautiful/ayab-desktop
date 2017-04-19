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

echo "# install python2.7"
brew install python
echo -n "Python version: "
python --version
python -m pip install --upgrade pip

echo "# install requirements"
python -m pip install $USER -r ../requirements.txt
python -m pip install $USER PyInstaller

./build.sh $USER

