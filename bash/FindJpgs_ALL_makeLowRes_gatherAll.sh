#!/bin/bash
. ~/.bash_profile


pmPhotoDir=/mnt/Post_Ready/zImages_1
pmPhotoXdir=/mnt/Post_Ready/zImages_1/xxFer
zoomPng=$pmPhotoXdir/zoomPng
dirStill=/mnt/Post_Ready/Retouch_Still
dirFashion=/mnt/Post_Ready/Retouch_Fashion

###-------Time Logging
dateLog=`date`
echo "Start _All_ $dateLog" >> $LOGDIR/FindMakeLowres_log.txt

##Copy all to Retouch Folders to Backup
#find $pushStill -type d -mindepth 1 -maxdepth 1 -exec cp -pR {} $dirStill \;
#find $pushFashion -type d -mindepth 1 -maxdepth 1 -exec cp -pR {} $dirFashion \;

## Double For loop to find and convert recent pushes for Zimages
fileListD=`find "$dirStill" "$dirFashion" -maxdepth 1 -mindepth 1 -mtime -22h -type d | xargs -L1 -n1`
#fileListD=`find $dirStill -maxdepth 1 -mindepth 1 -mmin 2000 -type d & find $dirFashion -maxdepth 1 -mindepth 1 -mmin 2000 -type d | xargs -L1 -n1`
for d in $fileListD; 
do
fileList=`find $d -type f -iname \*.jpg`


for f in $filelist; do name=`basename $f | sed 's/.jpg//1'`;

#exiftool -d %Y-%m-%d -overwrite_original_in_place '-IPTC:OriginalTransmissionReference<${Directory}/${FileName}' $f;
##make Png hi rez for Zimages
convert "$f[100%]" -define png:format=png24 -define png:compression-level=1 -define png:compression-strategy=0 -unsharp 55 -quality 90 $ZIMAGES/xxfer/$name.png;
#-format png
##make jpegs for Zimages
convert "$f[40%]" -adaptive-sharpen 50 -unsharp 75 -quality 75 $ZIMAGES/xxfer/$name.jpg;
done;


done;

## rm -R $pmPhotoXdir


##------->   Rez All files left in tmp Folder Down/Convert Images for Faster loading As Jpeg for display as thumbnail/list view
#>>cd $pmPhotoXdir
#>>mogrify '*.jpg[400x480]' -compress none -format jpg -unsharp 75 -quality 80

#### Tag all Files with Merchant Info
##/mnt/Post_Ready/zProd_Server/imageServer7/scripts/bash/aGreatMerchantTagger.sh /mnt/Post_Ready/zImages_1/xxFer

## Sort all files to 4 digit hash Dir for Web/PM access
#exiftool -r -m -f '-Directory='"$ZIMAGES"'/%4f' '-Filename=%f.%e' $pmPhotoXdir
cd $pmPhotoXdir
exiftool -r -m -f '-Directory=../%4f/' '-Filename=%f.%e' $pmPhotoXdir;

#>>>>>for f in `ls $pmPhotoXdir`
#>>>>>do
#outName=`basename "$f"`
#>>>>>cd $pmPhotoXdir
#>>>>>exiftool -r -o "'"$ZIMAGES"'" '-Directory='"$ZIMAGES"'/%4f' '-Filename=%f.%e' $f

#/mnt/Post_Ready/eFashionPush -ext jpg
##exiftool -f -m -P -'Directory=$pmPhotodir/%4f' $f
#exiftool -f -m -P -'Directory=$pmPhotodir/%4f' -'FileName=%f%+lc.%e' "'"$f"'"
#exiftool -f -m -P -'Directory=$pmPhotodir/%4f' -'FileName=%f%+lc.%e' $pmPhotoXdir/"$f"
##curl -d sample_image=Y -d photographed_date=now -X PUT http://dmzimage01.l3.bluefly.com:8080/photo/"$outName"
#>>done;

####<-----------Clean out Duplicates left over from exif Sort. Moves to tmpDeletePhoto on $PRODSRV
cd $pmPhotoXdir
deleteMove="delete_$TODAY";
mkdir $deleteMove;
find . -type f -maxdepth 1 -exec mv {} $deleteMove/ \;
mv $deleteMove/ $tmpDeletePhoto;
cd $tmpDeletePhoto;
exiftool -r -m -f '-Directory=%4f/' '-Filename=%f.%e' $tmpDeletePhoto;

##cp -p -R $pushStill $dirStill;
##cp -p -R $pushFashion $dirFashion;
sleep 1;

styleStringZimagesPro.sh;

###-------Time Logging
dateLog=`date`
echo "End _All_ $dateLog" >> $LOGDIR/FindMakeLowres_log.txt

exit;
