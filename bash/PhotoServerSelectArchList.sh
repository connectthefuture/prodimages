#!/bin/bash
. ~/.bash_profile

## catalogDirIntr="$1"

## CATALOG EVERYFILE ON $catalogDir(akaPost_Ready)
styleStringTest=$DATASRV/csv/post_ready_archives.csv
filesDir=/mnt/Post_Ready/Retouch_\*

find $filesDir -type f -iname \*_\?.jpg | sed s/\ /\\\\\ /g | sed s/\"/\\\"/g | sort -k1 -dur | xargs exiftool -d %Y-%m-%d -m -P -f -fast2 -'FileName' -'CreateDate' -csv | grep [2-7] | grep jpg | awk -FS',' '{ print $0 }' | awk '{ gsub(/\ /, "" , $1); print $1 }' | awk -F',' '{ print $2, $1, $NF }' | awk '{ split($0, a, " "); print a[3], $1, a[2] }' | awk '{ gsub(/.jpg/, "" , $2); print $2, $1, $3 }' | awk '{ gsub(/_[a-zA-Z0-9]{1,5}/, "" , $1); print $1, $2, $3 }' | sort -k1.1,1.9 -k2.1,2.10 -n | grep -e ^[2-7,{1}] | awk '{ split($NF, a, "/[0-9]{9}"); print $1, $2, $3, a[NF] }' | | awk '{ split($NF, a, ".jpg"); print $1, $2, $3, a[1] }' | awk 'split($4, a, "_");{ print $1, $2, $3, a[NF] }' | sort -k1.1,1.9 -t, -d > $styleStringTest;

## awk '{ split($NF, a, ".jpg"); print $1, $2, $3, a[1] }' | awk '{ gsub(/_/, "", $NF); print }'


## cp $styleStringImport "$styleStringImport"_open
cp $styleStringImport ${PRODSRV}/data/csv

# awk -FS' ' '{ gsub(/'.jpg'/, "" , $1); print $1 }'
# awk '{ gsub(/"_[a-zA-Z0-9]{1,5} /, "" , $1); print $1 }'
# awk '{ split($0, a, "_[a-z]{1,3}[0-9]{1,5}|[1-9].jpg"); print $0, $1 }'
# awk -F' ' '{ print substr( $0, length($0) - 8, length($0) ), $1, $2 }'
# egrep -o '\b[0-9]{9}' | uniq

exit;
