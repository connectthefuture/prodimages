#!/bin/bash
. ~/.bash_profile


swidir = "$1"

for f in `find $swidir -type f -iname *_H*`; do
mv $f $(echo $f|sed 's/_HH//g'|sed $f 's/_H//g');
done
