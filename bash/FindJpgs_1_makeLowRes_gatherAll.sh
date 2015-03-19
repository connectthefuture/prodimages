#!/bin/bash
. ~/.bash_profile

#pushStill=/Volumes/Post_Ready/aPhotoPush
#pushFashion=/Volumes/Post_Ready/eFashionPush
dateLog=`date`
echo "START _1_ $dateLog" >> $LOGDIR/FindMakeLowres_PMphotoAttribImg_log.txt
pmPhotoDir=/Volumes/Post_Ready/zImages_1
pmPhotoXdir=/Volumes/Post_Ready/zImages_1/xxFer
echo "START _1_ $dateLog" >> ~/Dropbox/FindMakeLowres_log.txt
pmPhotoDir=/Volumes/Post_Ready/zImages_1
pmPhotoXdir=/Volumes/Post_Ready/zImages_1/xxFer

## -- Read all Dirs in Push folders
fileListD=`find ${pushStill} ${pushFashion} -maxdepth 1 -mindepth 1 -type d | xargs -L1 -n1`


##<--------------->Convert all to Retouch Folders to Backup
for d in $fileListD; 
do
fileList=`find $d -type f -iname \*_1.jpg`



for f in $fileList;
do
name=`basename $f | sed 's/.jpg//1'`
#exiftool -d %Y-%m-%d -overwrite_original_in_place '-IPTC:OriginalTransmissionReference<${Directory}/${FileName}' $f;
##make Png hi rez for Zimages
#convert $f -format png -define png:format=png24 -define png:compression-level=0 -define png:compression-strategy=0 -resize 2000x2400 -unsharp 75 -quality 100 $ZIMAGES/xxfer/$name.png;

##make jpegs for Zimages
convert $f -format jpg -resize 400x480 -adaptive-sharpen 50 -unsharp 75 -quality 100 $ZIMAGES/xxfer/$name.jpg ;
done;


done;

##Rez Down Images for Faster loading Then send attributes to PM
pmPhotoXdir=/Volumes/Post_Ready/zImages_1/xxFer
pmPhotoDir=/Volumes/Post_Ready/zImages_1
cd $pmPhotoXdir
#mogrify '*.jpg[400x480]'

#for f in `find $pmPhotoXdir -maxdepth 0 -type f -iname \*.jpg`
#do
#outName=`basename "$f"`

cd $pmPhotoXdir
exiftool -f -m -P -fast2 -'Directory='$pmPhotoDir'/%4f' $pmPhotoXdir
#exiftool -fast2 -f -m -P -'Directory='"$pmPhotodir"'/%4f' -'FileName=%f%+lc.%e' $pmPhotoXdir
##curl -d sample_image=Y -d photographed_date=now -X PUT http://dmzimage01.l3.bluefly.com:8080/photo/"$outName"


##cp -p -R $pushStill $dirStill;
##cp -p -R $pushFashion $dirFashion;
dateLog=`date`
echo "End _1_ $dateLog" >> $LOGDIR/FindMakeLowres_PMphotoAttribImg_log.txt

exit;

