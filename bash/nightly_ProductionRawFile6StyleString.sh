#!/bin/bash
. ~/.bash_profile

## catalogDirIntr="$1"

## CATALOG EVERYFILE ON $catalogDir(akaPost_Ready)
styleStringImport=$DATASRV/csv/production_raw_onfigure.csv
retouchDirs=/mnt/Production_Raw/PHOTO_STUDIO_OUTPUT/ON_FIGURE

find $retouchDirs -type f -iname \*_\?.CR2 | sed s/\ /\\\\\ /g | sed s/\"/\\\"/g | sort -k1 -dur | xargs exiftool -d %Y-%m-%d -m -P -f -fast2 -'FileName' -'CreateDate' -csv | grep [2-7] | awk -FS',' '{ print $0 }' | awk '{ gsub(/\ /, "" , $1); print $1 }' | awk -F',' '{ print $2, $1, $NF }' | awk '{ split($0, a, " "); print a[3], $1, a[2] }' | awk '{ gsub(/.jpg/, "" , $2); print $2, $1, $3 }' | awk '{ gsub(/_[a-zA-Z0-9]{1,5}/, "" , $1); print $1, $2, $3 }' | sort -k1.1,1.9 -k2.1,2.10 -n | grep -e ^[2-7,{1}] | awk '{ split($NF, a, "[0-9]{9}"); print $0, a[NF] }' | sed 's/\/Volumes\/Post_Ready//1' | awk -F' ' '{ gsub(/.jpg/, "" , $NF); print $0 }' | awk -F' ' '{ gsub(/.CR2/, "" , $NF); print $0 }' | awk -F' ' '{ gsub(/_/, "" , $NF); print $0 }' | sort -k1.1,1.9 -d | grep _ > $styleStringImport;

## cp $styleStringImport "$styleStringImport"_open
#cp $styleStringImport $DATASRV/csv

    

###<------------Send Outputted CSV to data_imagepaths MySQL db-------------------->
mysqlimport --host=127.0.0.1 --port=3301 --user=root --password=mysql --fields-terminated-by=" " --fields-escaped-by="\"" --delete --replace --ignore-lines=0 --columns=colorstyle,photo_date,file_path,alt --local data_imagepaths $styleStringImport


# awk -FS' ' '{ gsub(/'.jpg'/, "" , $1); print $1 }'
# awk '{ gsub(/"_[a-zA-Z0-9]{1,5} /, "" , $1); print $1 }'
# awk '{ split($0, a, "_[a-z]{1,3}[0-9]{1,5}|[1-9].jpg"); print $0, $1 }'
# awk -F' ' '{ print substr( $0, length($0) - 8, length($0) ), $1, $2 }'
# egrep -o '\b[0-9]{9}' | uniq

exit;
