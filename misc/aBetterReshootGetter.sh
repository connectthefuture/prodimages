#!/bin/bash
. ~/.bash_profile
. ~/.bashrc

DATE=`date "+%Y-%m-%d"`
DAY=`date "+%Y-%m-%d-Reshoots"`
dataDir=$DATASRV/csv
catalogDirFashion=/mnt/Post_Ready/Retouch_Fashion/
catalogDirStill=/mnt/Post_Ready/Retouch_Still/
##styleStringNew=$dataDir/StyleStringTest.csv
styleStringNew=$dataDir/post_ready_summary.csv
## $DSSPRDLOGIN

## GET STYLES AND LOCATIONS ON SERVER FOR DAILY INC DOWNLOAD DELIVERY
sqlDailyReshootDownload=$SQLSCRIPTS/sqlPrdRecentReshootsToPull.sql
##/usr/local/sqlScripts/sqlPrdRecentToPull.sql
inHouseInc=`$DSSPRDLOGIN @$sqlDailyReshootDownload | sed s/'--'//g | sed s/'  '//g | sed s/' ,'/','/g | sort -k1.1,1.9 -t, -du`

dailyDownloadFile=$dataDir/Reshoot_DAILY_DOWNLOADFILE7.csv

rm $dailyDownloadFile;
for styleNum in $inHouseInc
do
cat $styleStringNew | grep -v zImages | grep -v zAlf | awk -v searchStyle="$styleNum" '$1 ~ searchStyle' >> $dailyDownloadFile
done;

cat $dailyDownloadFile | awk -F' ' '{ print $NF }' | sed s/\'//g | awk -F'/' '{ print $0, $NF }' | awk '{ print("mkdir -p /mnt/Post_Ready/Daily/$DAY && cp -f "$1" /mnt/Post_Ready/Daily/$DAY/"$2)}' | sed s/\$DAY/$DAY/g | awk '{ gsub(/\r/, "" , $0); print $0 }' | /bin/bash

exit;
