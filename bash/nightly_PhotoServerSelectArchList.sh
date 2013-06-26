#!/bin/bash
. ~/.bash_profile

## catalogDirIntr="$1"

## CATALOG EVERYFILE ON $catalogDir(akaPost_Ready)
styleStringImport=$DATASRV/csv/post_ready_original.csv
retouchDirs=/mnt/Post_Ready/Retouch_\*



find $retouchDirs -type f -iname \*_\?.jpg | sed s/\ /\\\\\ /g | sed s/\"/\\\"/g | sort -k1 -dur | xargs exiftool -i /mnt/Post_Ready/Retouch_Still/EXTRA -d %Y-%m-%d -m -P -f -fast2 -'FileName' -'CreateDate' -csv | grep [2-7] | xargs -n1 | awk -v RS=' ' -v ORS='\n' -FS',' '{ print $0 }' | awk -FS',' '{ print $2, $1 }' | awk -v RS='\n' -FS',' '{ gsub(/.jpg/, "", $2); print $1,$3,$2 }' | sed 's/^ *//g' | awk -v RS='\n' -F, '{ split($2, a, "_"); print a[1], $3, $1, a[2] }' | awk '{print $1,$2,$3,$4}' | awk '{ gsub(/.jpg/, "", $4); print $1, $2, $3, $4 }' | grep "_" | sed 's:/mnt/Post_Ready::g' > $styleStringImport ;


### Old Unreliable version
#find $retouchDirs -type f -iname \*_\?.jpg | sed s/\ /\\\\\ /g | sed s/\"/\\\"/g | sort -k1 -dur | xargs exiftool -i /mnt/Post_Ready/Retouch_Still/EXTRA -d %Y-%m-%d -m -P -f -fast2 -'FileName' -'CreateDate' -csv | grep [2-7] | grep jpg | awk -FS',' '{ print $0 }' | awk '{ gsub(/\ /, "" , $1); print $1 }' | awk -F',' '{ print $2, $1, $NF }' | awk '{ split($0, a, " "); print a[3], $1, a[2] }' | awk '{ gsub(/.jpg/, "" , $2); print $2, $1, $3 }' | awk '{ gsub(/_[a-zA-Z0-9]{1,5}/, "" , $1); print $1, $2, $3 }' | sort -k1.1,1.9 -k2.1,2.10 -n | grep -e ^[2-7,{1}] | awk '{ split($NF, a, "[0-9]{9}"); print $0, a[NF] }' | sed 's/\/Volumes\/Post_Ready//1' | awk -F' ' '{ gsub(/.jpg/, "" , $NF); print $0 }' | awk -F' ' '{ gsub(/.png/, "" , $NF); print $0 }' | awk -F' ' '{ gsub(/_/, "" , $NF); print $0 }' | sort -k1.1,1.9 -d | grep _ | sed 's:/mnt/Post_Ready::g' > $styleStringImport;

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
