#!/bin/bash
#
# execute with --user to make a pip install in the user home
#
set -e

cd "`dirname \"$0\"`"
USER="$1"

PACKAGE_VERSION="`./package_version`"
TAG_NAME="`./tag_name`"

cd ..

echo "# build the distribution"
cp linux-build/README.rst .
cp package_version LICENSE.txt ayab/
python setup.py sdist bdist_wheel
mkdir -p dist/release
mv dist/ayab*.tar.gz dist/release/
mv dist/ayab*.whl dist/release/
ls dist/release/

echo "# show the versions"
echo -n "setup.py --version: "
python setup.py --version
echo "Package version $PACKAGE_VERSION with possible tag name $TAG_NAME"

