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
python2 setup.py sdist

ls dist

echo "# show the versions"
echo -n "setup.py --version: "
python2 setup.py --version
echo -n "requirements: "
python2 setup.py requirements
echo "Package version $PACKAGE_VERSION with possible tag name $TAG_NAME"

