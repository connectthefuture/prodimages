#!/bin/bash
. ~/.bash_profile
pmPush="$1"

pmPhotoDir=/mnt/Post_Ready/zImages_1
pmPhotoXdir=/mnt/Post_Ready/zImages_1/xFer

fileList=`find $pmPush -type f -iname \*_1.jpg` 

rm -R $pmPhotoXdir
mkdir $pmPhotoXdir

cp -p $fileList $pmPhotoXdir

##Rez Down Images for Faster loading Then send attributes to PM

cd $pmPhotoXdir
mogrify '*.jpg[400x480]'

for f in `ls $pmPhotoXdir`
do

outName=`basename "$f" | sed s/_1.jpg//g`

cd $pmPhotoXdir
exiftool -f -m -P -'directory'=$pmPhotoDir/%4f $pmPhotoXdir/"$outName"_1.jpg

curl -d sample_image=Y -d photographed_date=now -X PUT http://ccapp101.l3.bluefly.com:8080/photo/"$outName"

done;

exit;

