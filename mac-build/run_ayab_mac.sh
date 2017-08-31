#!/bin/bash
export LC_CTYPE=en_US.UTF-8
export PYTHONIOENCODING=utf-8

rm -f /tmp/ayab_install.log

RUN_PATH=`pwd`
if [[ $RUN_PATH != *"Applications"* ]]
then
  echo "AYAB-Launcher.app needs to be copied to the /Applications folder"
  exit 1
fi

USER=`whoami`
PACKAGE_VERSION="`cat ./package_version`"

if type xcode-select >&- && xpath=$( xcode-select --print-path ) &&
   test -d "${xpath}" && test -x "${xpath}" ; then
     echo "xcode command line tools already installed"
else
     echo "install xcode command line tools"
     echo "******************************************"
     echo "please be patient, this might take a while"
     echo "******************************************"
     touch /tmp/.com.apple.dt.CommandLineTools.installondemand.in-progress;
     PROD=$(softwareupdate -l | grep "\*.*Command Line" | head -n 1 | awk -F"*" '{print $2}' | sed -e 's/^ *//' | tr -d '\n')
     softwareupdate -i "$PROD";
fi

if [ ! -f "/Users/$USER/.pyenv/bin/pyenv" ]
then
  echo "install pyenv"
  curl -s -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer -o /tmp/pyenv-installer >> /tmp/ayab_install.log 2>&1
  bash /tmp/pyenv-installer >> install.log 2>&1
  rm -f /tmp/pyenv-installer
else
  echo "pyenv already installed"
fi

if [ ! -f "/Users/$USER/.pyenv/shims/python3.5" ]
then
  echo "install python"
  env PYTHON_CONFIGURE_OPTS="--enable-framework" /Users/$USER/.pyenv/bin/pyenv install 3.5.0 >> /tmp/ayab_install.log 2>&1
else
  echo "python already installed"
fi

/Users/$USER/.pyenv/bin/pyenv local 3.5.0 >> /tmp/ayab_install.log 2>&1
eval "$(/Users/$USER/.pyenv/bin/pyenv init -)" >> /tmp/ayab_install.log 2>&1
/Users/$USER/.pyenv/shims/pip3 install --upgrade pip >> /tmp/ayab_install.log 2>&1
/Users/$USER/.pyenv/shims/pip3 install PyQt5 >> /tmp/ayab_install.log 2>&1
/Users/$USER/.pyenv/shims/pip3 install pyobjc >> /tmp/ayab_install.log 2>&1
/Users/$USER/.pyenv/shims/pip3 install -r requirements.txt >> /tmp/ayab_install.log 2>&1

if [ ! -f "/Applications/AYAB-Launcher.app/Contents/Resources/AYAB.app/Contents/MacOS/main.sh" ]
then
  echo "creating wrapper"
  /Users/$USER/.pyenv/shims/python3 pyapp.py ayab_devel_launch.py AYAB $PACKAGE_VERSION >> /tmp/ayab_install.log 2>&1
fi

if [ ! -d "/Users/$USER/Documents/AYAB/patterns" ]
then
  echo "installing patterns"
  mkdir -p /Users/$USER/Documents/AYAB/
  cp -R patterns /Users/$USER/Documents/AYAB/
fi

echo "running app"
AYAB.app/Contents/MacOS/main.sh
