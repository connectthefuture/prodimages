#!/bin/bash
. ~/.bash_profile

## catalogDirIntr="$1"

## CATALOG EVERYFILE ON $catalogDir(akaPost_Ready)
styleStringImport=$DATASRV/csv/post_ready_original.csv
retouchDirs=/Volumes/Post_Ready/Retouch_\*



find $retouchDirs -type f -iname \*_\?.jpg | sed s/\ /\\\\\ /g | sed s/\"/\\\"/g | sort -k1 -dur | xargs exiftool -i SYMLINKS -i /mnt/Post_Ready/Retouch_Still/EXTRA -d %Y-%m-%d -m -P -f -fast2 -'FileName' -'CreateDate' -csv | grep [2-7] | xargs -n1 | awk -v RS=' ' -v ORS='\n' -FS',' '{ print $0 }' | awk -FS',' '{ print $2, $1 }' | awk -v RS='\n' -FS',' '{ gsub(/.jpg/, "", $2); print $1,$3,$2 }' | sed 's/^ *//g' | awk -v RS='\n' -F, '{ split($2, a, "_"); print a[1], $3, $1, a[2] }' | awk '{print $1,$2,$3,$4}' | awk '{ gsub(/.jpg/, "", $4); print $1, $2, $3, $4 }' | grep "_" | sed 's:/mnt/Post_Ready::g' 
#> $styleStringImport ;
#
#
#cp $styleStringImport $styleStringImport_open
#cp $styleStringImport $DATASRV/csv
#
#
####<------------Send Outputted CSV to data_imagepaths MySQL db-------------------->
#mysqlimport --host=127.0.0.1 --port=3301 --user=root --password=mysql --fields-terminated-by=" " --fields-escaped-by="\"" --delete --replace --ignore-lines=0 --columns=colorstyle,photo_date,file_path,alt --local data_imagepaths $styleStringImport
#
#exit;
