#!/bin/bash

for i in {0..1}; 
do 
fpath=`date +"/mnt/Production_Raw/PHOTO_STUDIO_OUTPUT/ON_FIGURE/%m_%Y/%m%d%y_*" --date="$i days ago"`; 
find $fpath -wholename \*RAW\* -type f -iname \*.CR2 -exec /usr/local/batchRunScripts/python/mtags_singlefile_RAW.py {} \; &
done;
