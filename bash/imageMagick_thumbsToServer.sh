#!/bin/bash
. ~/.bash_profile
Today=`date +%Y-%m-%d`
batchDoneDate=`date +%Y%b%d`


thumbSelects=$PRODSRV/images/images_jpg_Thumbs/selects
MAGICK_LOAD=$thumbSelects/tmp

##### Replace _1 etc in FileNames
#userDropFolders="${eFashionPush} ${aPhotoPush}"
preBatchDtop=$MAGICK_LOAD/batch/preBatch
batchDtop=$MAGICK_LOAD/batch/batch
postBatchDone=$MAGICK_LOAD/batch/batchDone
postBatchArchive=$MAGICK_LOAD/batch/batchArchive

##convertedFolder_png=$MAGICK_LOAD/PNG_Primary/
convertedFolder_l=$MAGICK_LOAD/L_JPG/
convertedFolder_lZ=$MAGICK_LOAD/LZOOM_JPG/
##convertedFolder_m=$MAGICK_LOAD/M_JPG/
convertedFolder_alt=$MAGICK_LOAD/ALT_JPG/
convertedFolder_altZ=$MAGICK_LOAD/ALTZOOM_JPG/

uploadInProg=$MAGICK_LOAD/b_Drop_Inprog_Loading
uploadComplete=$MAGICK_LOAD/c_Load_Complete

mkdir -p $preBatchDtop $preBatchDtop $batchDtop $postBatchDone $postBatchArchive $convertedFolder_l $convertedFolder_lZ $convertedFolder_altZ $convertedFolder_alt $uploadInProg
cd ${PRODSRV}/
#####		Remove Bad Files
errorFolder=$MAGICK_LOAD/errors
mkdir $errorFolder
find ${pushFashion}/ ${pushStill}/ -type f -iname \*.jpg | grep ' ' | xargs -I '{}' mv -f '{}' $errorFolder

#### Run Tag Retouched Photos with Retoucher Name
#$PRODSRV/scripts/bash/TAG_fromDirName.sh

######		Move all files starting with 9 Digits to preBatch Folder
find ${pushFashion}/ ${pushStill}/ -type f -iname [{^2-9}][0-9{8}]\*.jpg | grep -v ' ' | xargs -I '{}' cp -Rp '{}' $preBatchDtop

findPreBatch=`find $preBatchDtop -iname \*.jpg`
### Rename files based on Photo output names (_1,_2)etc.
for f in $findPreBatch
do
baseName=`basename $f | sed 's/\ /\\\ /g'`
echo $f | sed 's/\ /\\\ /g' | awk -v batch=$batchDtop -v fname=$baseName '{print("mv -f "$1" "batch"/"fname)}' | sed 's/_1//2' | sed 's/_2/_alt01/2' | sed 's/_3/_alt02/2' | sed 's/_4/_alt03/2' | sed 's/_5/_alt04/2' | sed 's/_6/_alt05/2' | /bin/bash;
done;

### Move/Copy files to folder based on Format ImageMagick will convert to
find $batchDtop -type f -iname \*_alt0[1-5].jpg -exec mv -p {} $convertedFolder_alt \;
find $batchDtop -type f -iname [2-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].jpg -exec mv -p {} $convertedFolder_l \;
##find $batchDtop -type f -iname [2-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].jpg -exec cp -p {} $convertedFolder_m \;
##find $batchDtop -type f -iname [2-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].jpg -exec cp -p {} $convertedFolder_png \;
##find $batchDtop -type f -iname [2-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].jpg -exec mv -f {} $postBatchDone \;

####### Add _l and _m to files in Respective Folders
## Large Jpegs
for f in `find $convertedFolder_l -iname \*.jpg`
do
baseNamePlus=`echo $f | sed s/\ /\\\\\ /g | sed s/.jpg//g`
echo $f | awk -v folder_l=$convertedFolder_l -v fname=$baseNamePlus '{print("mv -fv "$1 folder_lfname" "fname"_l.jpg")}' | /bin/bash;
done;

## Medium Jpegs
##for f in `find $convertedFolder_m -iname \*.jpg`
##do
##baseNamePlus=`echo $f | sed s/\ /\\\\\ /g | sed s/.jpg//g`
##echo $f | awk -v folder_m=$convertedFolder_m -v fname=$baseNamePlus '{print("mv -fv "$1 folder_mfname" "fname"_m.jpg")}' | /bin/bash;
##done;


##Mogrify - Format as Thumb_l and Zoom
cd $convertedFolder_l
cp -p \*.jpg $convertedFolder_lZ
mogrify '*.jpg[200x240]' -compress none -format jpeg -adaptive-sharpen 100 -unsharp 50 -quality 100
find $convertedFolder_l -type f -iname \*.jpg -exec mv {} $uploadInProg \;
cd $convertedFolder_lZ
mogrify '*.jpg[600x720]' -compress none -format jpeg -adaptive-sharpen 100 -unsharp 50 -quality 100

##Mogrify - Format as Alt Thumb and Zoom
##cp -pR $convertedFolder_alt $convertedFolder_m
cd $convertedFolder_alt
cp -p \*.jpg $convertedFolder_altZ
mogrify '*.jpg[200x240]' -compress none -format jpeg -adaptive-sharpen 100 -unsharp 40 -quality 100
find $convertedFolder_alt -type f -iname \*.jpg -exec mv {} $uploadInProg \;
cd $convertedFolder_altZ
mogrify '*.jpg[600x720]' -compress none -format jpeg -adaptive-sharpen 100 -unsharp 50 -quality 100





exit;
#### Original stored
# batchDoneFolder="$postBatchDone/$batchDoneDate"
# mkdir $batchDoneFolder
# for f in `find $batchDtop -iname \*.jpg`
# do
# exiftool -m -P -fast2 -overwrite_original -'IPTC:DateOriginalRetouchProcessed'='$Today' $f
# mv -f $f $batchDoneFolder
# done;

##########			##########	 Upload Files via FTP through cUrl
# ftpLoginFull="ftp://file3.bluefly.corp/ImageDrop/ --user imagedrop:imagedrop0"
## weddavLogin="https://imagedrop:imagedrop0@file3.bluefly.corp/ImageDrop/"

### for Find only jp'g' and pn'g' files
# for f in `find $uploadInProg -type f -iname \*.*g`
# do
# uploadResult=`curl -k -T $f $ftpLoginFull`
# exiftool -m -P -fast2 -overwrite_original -'IPTC:DateLoaded'='$Today' $f
# mv -f $f $uploadComplete;
# echo "$Today, $f, $uploadResult" >> $PRODSRV/logs/uploadLog.txt
# done;
