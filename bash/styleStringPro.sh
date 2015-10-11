#!/bin/bash
. ~/.bash_profile

filesDir="$1"
outDir="$2"
filename=`basename $filesDir`

## CATALOG EVERYFILE ON $catalogDir(akaPost_Ready)
styleStringTest="$outDir"/$filename.csv

find $filesDir -type f -iname \*_\?.jpg | sed s/\ /\\\\\ /g | sed s/\"/\\\"/g | sort -k1 -dur | xargs exiftool -d %Y-%m-%d -m -P -f -fast2 -'FileName' -'CreateDate' -csv | grep [2-7] | grep jpg | awk -FS',' '{ print $0 }' | awk '{ gsub(/\ /, "" , $1); print $1 }' | awk -F',' '{ print $2, $1, $NF }' | awk '{ split($0, a, " "); print a[3], $1, a[2] }' | awk '{ gsub(/.jpg/, "" , $2); print $2, $1, $3 }' | awk '{ gsub(/_[a-zA-Z0-9]{1,5}/, "" , $1); print $1, $2, $3 }' | sort -k1.1,1.9 -k2.1,2.10 -n | grep -e ^[2-7,{1}] | sort -k1.1,1.9 -t, -du > $styleStringTest;

cp $styleStringTest "$styleStringTest"_open

exit;
