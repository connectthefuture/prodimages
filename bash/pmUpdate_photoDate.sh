#!/bin/bash
. ~/.bash_profile

pmPhotoDir=/mnt/Post_Ready/zImages_1
pmPhotoXdir=/mnt/Post_Ready/zImages_1/xxFer



#####  ONLY UPDATES STILL LIFE SETS PHOTO ATTRIB -- USE SEP PYTHON SCRIPT FOR FASHION
## Or uncomment next line
#fileList=`find ${pushStill} ${pushFashion} -type f -cmin -1000 -iname \*_1.jpg`

dailydirname=`date +"%m%d%y"`

fileList=`find ${pushStill}/${dailydirname}_* -type f -cmin -1200 -iname \*_1.jpg`


for f in $fileList
do
outName=`basename "$f" | sed s/_1.jpg//g`
#photoDate=`exiftool -${CreateDate} "$f"`

##datetime.datetime(2012, 9, 29, 2, 24, 52)
curl -d sample_image=Y -d photographed_date=now -X PUT http://dmzimage01.l3.bluefly.com:8080/photo/"$outName"
#echo $outName,$photoDate >> $PRODSRV/logs/pmPhotoLoad.csv

done;
exit;

