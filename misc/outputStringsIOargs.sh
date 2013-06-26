#!/bin/bash
. ~/.bash_profile

## CATALOG EVERYFILE ON $catalogDir(akaPost_Ready)
searchDir=$1
outFile=$2
##AKA stylestringtests
find $searchDir -type f -iname \*_\?.jpg | sed s/\ /\\\\\ /g | sed s/\"/\\\"/g | uniq | xargs exiftool -d %m-%d-%Y -m -P -f -fast2 -'FileName' -'ModifyDate' -csv | grep -v _MACOSX | grep [2-4] | grep jpg | sort | awk -FS',' '{ print $0 }' | awk '{ gsub(/\ /, "" , $1); print $1 }' | awk -F',' '{ print $2, $1, $NF }' | awk '{ split($0, a, " "); print a[3], $1, a[2] }' | awk '{ gsub(/.jpg/, "" , $2); print $2, $1, $3 }' | awk '{ gsub(/_[a-zA-Z0-9]{1,5}/, "" , $1); print $1, $3 }' > $outFile;
exit;
