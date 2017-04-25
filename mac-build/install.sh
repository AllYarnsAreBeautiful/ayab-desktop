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
echo "# install pyenv"
brew unlink pyenv
brew install pyenv
echo "# pyenv 3.5.0"
env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.5.0
pyenv global 3.5.0
echo "# install PyQt5"
brew install PyQt5

echo -n "Python version: "
~/.pyenv/shims/python3 --version
~/.pyenv/shims/python3 -m pip install --upgrade pip

echo "# install requirements"
~/.pyenv/shims/python3 -m pip install $USER -r ../requirements.txt
~/.pyenv/shims/python3 -m pip install $USER PyInstaller

./build.sh $USER

