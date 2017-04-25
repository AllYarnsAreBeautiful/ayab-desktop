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

./install_pyqt5.sh

echo -n "Python version: "
which python
python --version
sudo easy_install pip
python -m pip install --upgrade pip

echo "# install requirements"
python -m pip install $USER -r ../requirements.txt
python -m pip install $USER PyInstaller

./build.sh $USER

