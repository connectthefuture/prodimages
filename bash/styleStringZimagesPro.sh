#!/bin/bash
. ~/.bash_profile

#filesDir="$1"
#outDir="$2"
filesDir=/mnt/Post_Ready/zImages_1
outDir=$PRODSRV/data/csv
filename=`basename $filesDir | sed 's/zImages_1/zimages1/'`

## CATALOG EVERYFILE ON $catalogDir(akaPost_Ready)
styleStringTest="$outDir"/"$filename"


find $filesDir -type f -maxdepth 2 -iname \*_\?.jpg | grep -v xxFer | sed s/\ /\\\\\ /g | sed s/\"/\\\"/g | sort -k1 -du | xargs exiftool -i SYMLINKS -d %Y-%m-%d -m -P -f -fast2 -'FileName' -'CreateDate' -csv | awk -FS',' '{ print $0 }' | awk '{ gsub(/\ /, "" , $1); print $1 }' | awk -F',' '{ print $2, $1, $NF }' | awk '{ split($0, a, " "); print a[3], $1, a[2] }' | awk '{ gsub(/.jpg/, "" , $2); print $2, $1, $3 }' | awk '{ gsub(/_[a-zA-Z0-9]{1,5}/, "" , $1); print $1, $2, $3 }' | sort -k1.1,1.9 -k2.1,2.10 -n | awk '{ split($NF, a, "[0-9]{9}"); print $1, $2, $3, a[NF] }' | awk '{ split($3, a, "([0-9]|.)[1-9]_"); print $0, a[2] }' | awk '{ gsub(/.jpg/, "" , $4); print $0 }' | awk '{ split($4, a, "[A-Za-z1-9]_"); print $0,a[NF] }' | awk '{ gsub(/_/, "" , $4); print $1,$2,$3,$4 }' | awk '{ split($1, a, "_[1-9]"); print a[1], $2, $3, $4 }' | sed 's/\/mnt\/Post_Ready\/zImages_1/\/zImages/g' | sort -k1.1,1.9 -t, -du > $styleStringTest.csv;

cp $styleStringTest.csv "$styleStringTest"_photoselects.csv

###<------------Send Outputted CSV to data_imagepaths MySQL db-------------------->
mysqlimport --host=127.0.0.1 --port=3301 --user=root --password=mysql --fields-terminated-by=" " --delete --replace --ignore-lines=0 --columns=colorstyle,photo_date,file_path,alt --local data_imagepaths "$styleStringTest"_photoselects.csv

exit;
