#!/bin/bash
. ~/.bash_profile
. ~/.bashrc

DATE=`date "+%Y-%m-%d"`
DAY=`date "+%Y-%m-%d-Reshoots"`
dataDir=$PRODSRV/data/csv
filesDir="${pushFashion} ${pushStill}"
##styleStringNew=$dataDir/StyleStringTest.csv
styleStringNew=$dataDir/post_ready_reshoots.csv
## $DSSPRDLOGIN

find $filesDir -type f -ctime 0 -iname \*_\?.jpg | sed s/\ /\\\\\ /g | sed s/\"/\\\"/g | xargs exiftool -d %Y-%m-%d -m -P -f -fast2 -'FileName' -'CreateDate' -csv | grep [2-7] | grep jpg | awk -FS',' '{ print $0 }' | awk '{ gsub(/\ /, "" , $1); print $1 }' | awk -F',' '{ print $2, $1, $NF }' | awk '{ split($0, a, " "); print a[3], $1, a[2] }' | awk '{ gsub(/.jpg/, "" , $2); print $2, $1, $3 }' | awk '{ gsub(/_[a-zA-Z0-9]{1,5}/, "" , $1); print $1, $2, $3 }' | sort -k1.1,1.9 -k2.1,2.10 -n | grep -e ^[2-7,{1}] | | sort -t, -k1.1,1.9 -du > $styleStringNew;

## GET STYLES AND LOCATIONS ON SERVER FOR DAILY INC DOWNLOAD DELIVERY
sqlDailyReshootDownload=$SQLSCRIPTS/sqlPrdRecentReshootsToPull.sql
##/usr/local/sqlScripts/sqlPrdRecentToPull.sql
inHouseInc=`$DSSPRDLOGIN @$sqlDailyReshootDownload | sed s/'--'//g | sed s/'  '//g | sed s/' ,'/','/g | sort | uniq`

dailyDownloadFile=$dataDir/Reshoot_DAILY_DOWNLOADFILE7.csv

#rm $dailyDownloadFile;
for styleNum in $inHouseInc
do
cat $styleStringNew | grep -v zImages | grep -v zAlf | awk -v searchStyle="$styleNum" '$1 ~ searchStyle' >> $dailyDownloadFile
done;

cat $dailyDownloadFile | awk -F' ' '{ print $NF }' | sed s/\'//g | awk -F'/' '{ print $0, $NF }' | awk '{ print("mkdir -p /mnt/Post_Ready/Daily/$DAY && cp -f "$1" /mnt/Post_Ready/Daily/$DAY/"$2)}' | sed s/\$DAY/$DAY/g | awk '{ gsub(/\r/, "" , $0); print $0 }' | /bin/bash
exit;
