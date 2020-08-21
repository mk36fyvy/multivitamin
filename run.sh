#! /usr/bin/env bash

SHDIR=`dirname $0`

echo $SHDIR

PYTHONPATH=$SHDIR

python3 $SHDIR/multivitamin/multiVitamin.py $@
