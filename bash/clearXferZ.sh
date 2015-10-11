#!/bin/bash
. ~/.bash_profile

dateLog=`date | sed 's/\ /_/g' | sed 's/\//_/g' | sed 's/\://g'`
echo "Start ClearXXfer $dateLog" >> ~/Dropbox/FindMakeLowres_log.txt


pmPhotoXdir=/mnt/Post_Ready/zImages_1/xxFer
pmPhotoDir=/mnt/Post_Ready/zImages_1

cd $pmPhotoXdir
exiftool -f -m -P -fast2 -'Directory='$pmPhotoDir'/%4f' $pmPhotoXdir;

cd $pmPhotoXdir
deleteMove="delete_$dateLog";
mkdir $deleteMove;
find . -type f -maxdepth 1 -exec mv {} $deleteMove/ \;
mv $deleteMove/ $tmpDeletePhoto;
cd $tmpDeletePhoto;
exiftool -r -m -f '-Directory=%4f/' '-Filename=%f.%e' $tmpDeletePhoto;

##cp -p -R $pushStill $dirStill;
##cp -p -R $pushFashion $dirFashion;
sleep 1;
##/mnt/Post_Ready/zProd_Server/imageServer7/scripts/default/styleStringZimagesPro.sh;

###-------Time Logging
dateLog=`date`
echo "End _ClearXXfer_ $dateLog" >> ~/Dropbox/FindMakeLowres_log.txt

exit;


