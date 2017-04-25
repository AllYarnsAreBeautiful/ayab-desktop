cd ~
mkdir dev_tools
cd dev_tools


## download SIP source code
wget http://sourceforge.net/projects/pyqt/files/sip/sip-4.19.2/sip-4.19.2.tar.gz
tar zxf sip-4.19.2.tar.gz
cd sip-4.19.2
python configure.py
make
make install

## Install Qt5
brew install qt5

## environ for pyQT
export PATH="/System/Library/Frameworks/Python.framework/Versions/2.7/bin:$PATH"
export PATH="/Users/fu/Qt/5.4/clang_64/bin:$PATH"

## check for python's package path
python -c "import site; print site.getsitepackages()"

## compile pyQT ...
python configure.py \
        #-q /Users/fu/Qt/5.4/clang_64/bin/qmake \
        -d /Library/Python/2.7/site-packages/ \
        --sip /System/Library/Frameworks/Python.framework/Versions/2.7/bin/sip

make
sudo make install
