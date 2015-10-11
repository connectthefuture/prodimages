#!/bin/bash

. ~/.bash_profile


searchStyle_colorstyle.sh $1 $2 | awk -F'~' -v RS="||" -v ORS="\n" 'split($0, a, "--~");{ print a[2] }' | cat | grep -ve --~ | sort -n | grep -e [^A-Za-z1-9]
