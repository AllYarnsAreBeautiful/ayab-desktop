#!/bin/bash
export LC_CTYPE=en_US.UTF-8
export PYTHONIOENCODING=utf-8

USER=`whoami`

if [ ! -f "/Users/$USER/.pyenv/bin/pyenv" ]
then
  echo "install pyenv"
  curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer -o /tmp/pyenv-installer
  bash /tmp/pyenv-installer
  rm -f /tmp/pyenv-installer
fi

if [ ! -f "/Users/$USER/.pyenv/shims/python3.5" ]
then
  echo "install python"
  env PYTHON_CONFIGURE_OPTS="--enable-framework" /Users/$USER/.pyenv/bin/pyenv install 3.5.0
fi

/Users/$USER/.pyenv/bin/pyenv local 3.5.0
eval "$(/Users/$USER/.pyenv/bin/pyenv init -)"
/Users/$USER/.pyenv/shims/pip3 install --upgrade pip
/Users/$USER/.pyenv/shims/pip3 install PyQt5
/Users/$USER/.pyenv/shims/pip3 install -r requirements.txt

/Users/$USER/.pyenv/shims/python3 ayab_devel_launch.py
