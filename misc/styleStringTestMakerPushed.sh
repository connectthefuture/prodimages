#!/bin/bash
##. ~/.bash_profile

## catalogDirIntr="$1"

## CATALOG EVERYFILE ON $catalogDir(akaPost_Ready)
##StyleStringTest=/mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/phpImportTOrelation_PM_SchemasTables_sqlInsert/StyleStringTest.csv
styleStringTest=/mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/StyleStringTest.csv
styleStringTestF7=/mnt/Post_Ready/zProd_Server/imageServer7/data/csv/StyleStringTest.csv

retouchStill=/mnt/Post_Ready/aPhotoPush
retouchFashion=/mnt/Post_Ready/eFashionPush

find $pushStill -type f -iname \*_\?.jpg | sed s/\ /\\\\\ /g | sed s/\"/\\\"/g | sort -k1 -du | xargs exiftool -d %Y-%m-%d -m -P -f -fast2 -'FileName' -'CreateDate' -csv | grep [2-7] | grep jpg | sort | awk -FS',' '{ print $0 }' | awk '{ gsub(/\ /, "" , $1); print $1 }' | awk -F',' '{ print $2, $1, $NF }' | awk '{ split($0, a, " "); print a[3], $1, a[2] }' | awk '{ gsub(/.jpg/, "" , $2); print $2, $1, $3 }' | awk '{ gsub(/_[a-zA-Z0-9]{1,5}/, "" , $1); print $1, $2, $3 }' | sort -k1.1,1.9 -n | grep -e ^[2-7,{1}] > $styleStringTest;

find $pushFashion -type f -iname \*_\?.jpg | sed s/\ /\\\\\ /g | sed s/\"/\\\"/g | sort -k1 -du | xargs exiftool -d %Y-%m-%d -m -P -f -fast2 -'FileName' -'CreateDate' -csv | grep [2-7] | grep jpg | sort | awk -FS',' '{ print $0 }' | awk '{ gsub(/\ /, "" , $1); print $1 }' | awk -F',' '{ print $2, $1, $NF }' | awk '{ split($0, a, " "); print a[3], $1, a[2] }' | awk '{ gsub(/.jpg/, "" , $2); print $2, $1, $3 }' | awk '{ gsub(/_[a-zA-Z0-9]{1,5}/, "" , $1); print $1, $2, $3 }' | sort -k1.1,1.9 -n | grep -e ^[2-7,{1}] >> $styleStringTest;


cp $styleStringTest "$styleStringTest"_open
cp $styleStringTest $styleStringTestF7
#awk -FS' ' '{ gsub(/'.jpg'/, "" , $1); print $1 }'
# awk '{ gsub(/"_[a-zA-Z0-9]{1,5} /, "" , $1); print $1 }'
#awk '{ split($0, a, "_[a-z]{1,3}[0-9]{1,5}|[1-9].jpg"); print $0, $1 }'
# awk -F' ' '{ print substr( $0, length($0) - 8, length($0) ), $1, $2 }'
#egrep -o '\b[0-9]{9}' | uniq

exit;
