#!/bin/bash
. ~/.bash_profile

#filesDir="$1"
#outDir="$2"
filesDir=/mnt/Post_Ready/zImages_1
outDir=$PRODSRV/data/csv
filename=`basename $filesDir`

## CATALOG EVERYFILE ON $catalogDir(akaPost_Ready)
styleStringTest="$outDir"/"$filename".csv

find $filesDir -type f -iname \*_\?.jpg | sed s/\ /\\\\\ /g | sed s/\"/\\\"/g | sort -k1 -du | xargs exiftool -d %Y-%m-%d -m -P -f -fast2 -'FileName' -'CreateDate' -csv | grep [2-7] | grep jpg | awk -FS',' '{ print $0 }' | awk '{ gsub(/\ /, "" , $1); print $1 }' | awk -F',' '{ print $2, $1, $NF }' | awk '{ split($0, a, " "); print a[3], $1, a[2] }' | awk '{ gsub(/.jpg/, "" , $2); print $2, $1, $3 }' | awk '{ gsub(/_[a-zA-Z0-9]{1,5}/, "" , $1); print $1, $2, $3 }' | sort -k1.1,1.9 -k2.1,2.10 -n | grep -e ^[2-7,{1}] | awk '{ split($NF, a, "/[0-9]{9}"); print $1, $2, $3, a[NF] }' | awk '{ split($NF, a, ".jpg"); print $1, $2, $3, a[1] }' | awk '{ gsub(/_/, "", $NF); print }' | sed 's/\/Volumes\/Post_Ready\/zImages_1/zImages/1' sort -k1.1,1.9 -t, -d > $styleStringTest;
## awk '{ split($2, a, "-"); print $1, a[3]"-"a[1]"-"a[2], $3, $4}'
cp $styleStringTest "$styleStringTest"_open

###<------------Send Outputted CSV to data_imagepaths MySQL db-------------------->
mysqlimport --host=127.0.0.1 --port=3301 --user=root --password=mysql --fields-terminated-by="," --delete --replace --ignore-lines=0 --columns=colorstyle,photo_date,file_path,alt --local data_imagepaths "$styleStringTest"_open

exit;
