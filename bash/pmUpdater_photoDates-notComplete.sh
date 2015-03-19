#!/bin/bash
. ~/.bash_profile
TERM=xterm-color

pmPhotoDir=/mnt/Post_Ready/zImages_1
pmPhotoXdir=/mnt/Post_Ready/zImages_1/xxFer


fileList=`find ${pushStill} ${pushFashion} -type f -iname \*_1.jpg` 

for f in $fileList
outName=`basename "$f" | sed s/_1.jpg//g`
photoDate=`exiftool -s3 -'CreateDate' "$f"`;
echo $outName,$photoDate; 

done;


##datetime.datetime(2012, 9, 29, 2, 24, 52)
#curl -d sample_image=Y -d photographed_date=now -X PUT http://dmzimage01.l3.bluefly.com:8080/photo/"$outName"






##rm -R $pmPhotoXdir
##mkdir $pmPhotoXdir

##cp -p $fileList $pmPhotoXdir

##Rez Down Images for Faster loading Then send attributes to PM

##cd $pmPhotoXdir
#mogrify '*.jpg[400x480]'

#for f in `ls $pmPhotoXdir`
#do

#outName=`basename "$f" | sed s/_1.jpg//g`

#cd $pmPhotoXdir
#exiftool -f -m -P -'directory'=$pmPhotoDir/%4f $pmPhotoXdir/"$outName"_1.jpg

##

done;

exit;
