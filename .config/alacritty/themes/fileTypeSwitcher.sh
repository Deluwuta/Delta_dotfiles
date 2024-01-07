#!/bin/bash

# Kinda silly script that takes 2 parameters and changes the type of all
# files whose type matches in the current directory.
# The first parameter is the type to be modified and the second is the 
# type to be obtained.

if [ $# -ne 2 ]; then
    echo "Usage: `basename $0` IN_fileType OUT_fileType" 1>&2
    exit 1
fi

type_in=$1
type_out=$2

for item in *.$type_in; do
    mv $item $(echo $item | cut -d. -f1).$type_out
done
