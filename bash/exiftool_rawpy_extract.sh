#!/bin/bash

for i in {0..1}; 
do 
fpath=`date +"/mnt/Production_Raw/PHOTO_STUDIO_OUTPUT/ON_FIGURE/%m_%Y/%m%d%y_*" --date="$i days ago"`; 
find $fpath -wholename \*RAW\* -type d -exec /usr/local/batchRunScripts/python/raw_jpg_extractor.py {} \; &
done;
