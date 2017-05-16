#!/bin/bash
export LC_CTYPE=en_US.UTF-8
export PYTHONIOENCODING=utf-8

if [ ! -f "/usr/local/bin/brew" ]
then
  echo "installing brew"
  mkdir /tmp/homebrew && curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C /tmp/homebrew
  mkdir /usr/local/bin
  cp /tmp/homebrew/bin/brew /usr/local/bin/
fi

/usr/local/bin/brew update
/usr/local/bin/brew install pyenv
if [ -f "~/.pyenv/shims/python3.5" ]
then
  echo "install python" 
  env PYTHON_CONFIGURE_OPTS="--enable-framework" /usr/local/bin/pyenv install 3.5.0
fi

/usr/local/bin/pyenv local 3.5.0
eval "$(/usr/local/bin/pyenv init -)"
~/.pyenv/shims/pip3 install --upgrade pip
~/.pyenv/shims/pip3 install PyQt5
~/.pyenv/shims/pip3 install -r requirements.txt

~/.pyenv/shims/python3 ayab_devel_launch.py
