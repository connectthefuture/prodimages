#!/bin/bash
. ~/.bash_profile

pmPhotoDir=/mnt/Post_Ready/zImages_1
pmPhotoXdir=/mnt/Post_Ready/zImages_1/xxFer


fileList=`find ${pushStill} ${pushFashion} -type f -ctime -17h -iname \*_1.jpg` 

for f in $fileList
do
outName=`basename "$f" | sed s/_1.jpg//g`
photoDate=`exiftool -'$CreateDate' "$f"`

##datetime.datetime(2012, 9, 29, 2, 24, 52)
curl -d sample_image=Y -d photographed_date=now -X PUT http://ccapp101.l3.bluefly.com:8080/photo/"$outName"
echo $outName,$photoDate >> $PRODSRV/logs/pmPhotoLoad.csv

done;
exit;

