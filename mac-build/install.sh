#!/bin/bash
set -e

HERE="`dirname \"$0\"`"
USER="$1"
cd "$HERE"

./build.sh $USER

