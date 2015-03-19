#!/bin/bash
. ~/.bash_profile

pushStill=/mnt/Post_Ready/aPhotoPush
pushFashion=/mnt/Post_Ready/eFashionPush

pmPhotoDir=/mnt/Post_Ready/zImages_1
pmPhotoXdir=/mnt/Post_Ready/zImages_1/xFer

#dirStill=/mnt/Post_Ready/Retouch_Still
#dirFashion=/mnt/Post_Ready/Retouch_Fashion

##Copy all to Retouch Folders to Backup
#find $pushStill -type d -mindepth 1 -maxdepth 1 -exec cp -pR {} $dirStill \;
#find $pushFashion -type d -mindepth 1 -maxdepth 1 -exec cp -pR {} $dirFashion \;

fileList=`find $pushStill $pushFashion -type f -iname \*_1.jpg` 

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

#curl -d sample_image=Y -d photographed_date=now -X PUT http://dmzimage01.l3.bluefly.com:8080/photo/"$outName"

done;

##cp -p -R $pushStill $dirStill;
##cp -p -R $pushFashion $dirFashion;

exit;

