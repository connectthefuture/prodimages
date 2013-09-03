#!/bin/bash
. ~/.bash_profile

## catalogDirIntr="$1"

## CATALOG EVERYFILE ON $catalogDir(akaPost_Ready)
##StyleStringTest=/mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/phpImportTOrelation_PM_SchemasTables_sqlInsert/StyleStringTest.csv
styleStringTest=$DATASRV/csv/StyleStringTest.csv
styleStringImport=$DATASRV/csv/push_photoselects.csv
styleStringImportZ=$DATASRV/csv/zimages1_photoselects.csv
#retouchStill=/mnt/Post_Ready/aPhotoPush
#retouchFashion=/mnt/Post_Ready/eFashionPush

find $pushStill -type f -iname \*_\?.jpg | sed s/\ /\\\\\ /g | sed s/\"/\\\"/g | sort -k1 -d | xargs exiftool -d %Y-%m-%d -m -P -f -fast2 -'FileName' -'CreateDate' -csv | sort | awk -FS',' '{ print $0 }' | awk '{ gsub(/\ /, "" , $1); print $1 }' | awk -F',' '{ print $2, $1, $NF }' | awk '{ split($0, a, " "); print a[3], $1, a[2] }' | awk '{ gsub(/.jpg/, "" , $2); print $2, $1, $3 }' | awk '{ gsub(/_[a-zA-Z0-9]{1,5}/, "" , $1); print $1, $2, $3 }' | sort -k1.1,1.9 -n | awk -F_ '{ print $0, $NF }' | awk '{ split($NF,a,".");print $1,$2,$3,a[1]}'  | grep -e ^[2-7,{1}] | awk '{ split($1, a, "_[1-9]"); print a[1], $2, $3, $4 }' > $styleStringTest;

find $pushFashion -type f -iname \*_\?.jpg | sed s/\ /\\\\\ /g | sed s/\"/\\\"/g | sort -k1 -d | xargs exiftool -d %Y-%m-%d -m -P -f -fast2 -'FileName' -'CreateDate' -csv | sort | awk -FS',' '{ print $0 }' | awk '{ gsub(/\ /, "" , $1); print $1 }' | awk -F',' '{ print $2, $1, $NF }' | awk '{ split($0, a, " "); print a[3], $1, a[2] }' | awk '{ gsub(/.jpg/, "" , $2); print $2, $1, $3 }' | awk '{ gsub(/_[a-zA-Z0-9]{1,5}/, "" , $1); print $1, $2, $3 }' | sort -k1.1,1.9 -n | awk -F_ '{ print $0, $NF }' | awk '{ split($NF,a,".");print $1,$2,$3,a[1]}' | grep -e ^[2-7,{1}] | awk '{ split($1, a, "_[1-9]"); print a[1], $2, $3, $4 }' >> $styleStringTest;


cp $styleStringTest "$styleStringTest"_open
cp $styleStringTest $styleStringImport

## Import updates to Mysql
mysqlimport --host=127.0.0.1 --port=3301 --user=root --password=mysql --fields-terminated-by="\ " --default-character-set=utf8 --fields-enclosed-by="\'" --fields-escaped-by="\"" --delete --replace --ignore-lines=0 --columns="colorstyle,photo_date,file_path,alt" --local data_imagepaths "$styleStringImport" ;


#styleStringImportPma.sh

exit;
