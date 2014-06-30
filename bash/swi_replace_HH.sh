#!/bin/bash
. ~/.bash_profile


swidir=$1
for f in `find "$@" -type f`; do
mv $f $(echo $f|sed 's/_HH//g'|sed $f 's/_H//g');
done
