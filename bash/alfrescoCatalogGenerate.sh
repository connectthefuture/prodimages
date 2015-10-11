#!/bin/bash

find /mnt/Post_Ready/zAlfresco_Primary/Alfresco_Batch_Import/Images/ -type f -iname \*.jpg | sed s/\ /\\\\\ /g | sed s/\"/\\\"/g | sort | uniq | xargs exiftool -d %m-%d-%Y -m -P -f -fast2 -'FileName' -'ModifyDate' -csv | grep [2-4] | grep -v '_MACOSX' | sort | awk -FS',' '{ print $0 }' | awk '{ gsub(/\ /, "" , $1); print $1 }' | awk '{ gsub(/\ /, "" , $1); print $1 }' | awk -F',' '{ print $2, $1, $NF }' | awk '{ split($0, a, " "); print a[3], $1, a[2] }' | awk '{ gsub(/.jpg/, "" , $2); print $2, $1, $3 }' | awk -v OFS="," '{ gsub(/_[a-zA-Z0-9]{1,5}/, "" , $1); print $1, $2, $3 }' > $DATASRV/csv/AlfrescoImportCatalog.csv

exit;
