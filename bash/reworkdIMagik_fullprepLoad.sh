#!/bin/bash
. ~/.bash_profile
Today=`date +%Y-%m-%d`
batchDoneDate=`date +%Y%b%d`

##### Replace _1 etc in FileNames
userDropFolders=/home/johnb/mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly
preBatchDtop=/mnt/johnb/Desktop/FilesToBatch_FromPublicDrop
batchDtop=/mnt/johnb/Desktop/batch
postBatchDone=/mnt/johnb/Desktop/batchDone
postBatchArchive=/mnt/johnb/Desktop/Archive

convertedFolder_png=/mnt/johnb/Public/FilesToLoad_DropToServer/a_Drop_to_Load/PNG_Primary/
convertedFolder_l=/mnt/johnb/Public/FilesToLoad_DropToServer/a_Drop_to_Load/L_JPG/
convertedFolder_m=/mnt/johnb/Public/FilesToLoad_DropToServer/a_Drop_to_Load/M_JPG/
convertedFolder_alt=/mnt/johnb/Public/FilesToLoad_DropToServer/a_Drop_to_Load/ALT_JPG_PNG/

uploadInProg=/mnt/johnb/Public/FilesToLoad_DropToServer/b_Drop_Inprog_Loading
uploadComplete=/mnt/johnb/Public/FilesToLoad_DropToServer/c_Drop_Complete


#####		Remove Bad Files
errorFolder=/mnt/johnb/Desktop/Errors
mkdir $errorFolder
find $userDropFolders -type f -iname \*.* | grep ' ' | xargs -I '{}' mv -f '{}' $errorFolder

#### Run Tag Retouched Photos with Retoucher Name
/usr/local/batchRunScripts/TAG_fromDirName.sh

######		Move all files starting with 9 Digits to preBatch Folder
find $userDropFolders -type f -iname [{^2-9}][0-9{8}]\*.jpg | grep -v ' ' | xargs -I '{}' mv -f '{}' $preBatchDtop


### Rename files based on Photo output names (_1,_2)etc.
for f in `find $preBatchDtop -iname \*.jpg`
do
baseName=`basename $f | sed 's/\ /\\\ /g'`
echo $f | sed 's/\ /\\\ /g' | awk -v fname=$baseName '{print("mv -f "$1" /mnt/johnb/Desktop/batch/"fname)}' | sed 's/_1//2' | sed 's/_2/_alt01/2' | sed 's/_3/_alt02/2' | sed 's/_4/_alt03/2' | sed 's/_5/_alt04/2' | sed 's/_6/_alt05/2' | /bin/bash;
done;

### Move/Copy files to folder based on Format ImageMagick will convert to
find $batchDtop -type f -iname \*_alt0[1-5].jpg -exec cp -p {} $convertedFolder_alt \;
find $batchDtop -type f -iname [2-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].jpg -exec cp -p {} $convertedFolder_l \;
find $batchDtop -type f -iname [2-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].jpg -exec cp -p {} $convertedFolder_m \;
find $batchDtop -type f -iname [2-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].jpg -exec cp -p {} $convertedFolder_png \;
##find $batchDtop -type f -iname [2-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].jpg -exec mv -f {} $postBatchDone \;

####### Add _l and _m to files in Respective Folders
## Large Jpegs
for f in `find $convertedFolder_l -iname \*.jpg`
do
baseNamePlus=`echo $f | sed s/\ /\\\\\ /g | sed s/.jpg//g`
echo $f | awk -v folder_l=$convertedFolder_l -v fname=$baseNamePlus '{print("mv -fv "$1 folder_lfname" "fname"_l.jpg")}' | /bin/bash;
#>> /mnt/johnb/AWkdebug.txt 
done;

## Medium Jpegs
for f in `find $convertedFolder_m -iname \*.jpg`
do
baseNamePlus=`echo $f | sed s/\ /\\\\\ /g | sed s/.jpg//g`
echo $f | awk -v folder_m=$convertedFolder_m -v fname=$baseNamePlus '{print("mv -fv "$1 folder_mfname" "fname"_m.jpg")}' | /bin/bash;
done;


##Mogrify - Format as _l jpg
cd $convertedFolder_l
mogrify '*.jpg[400x480]' -compress none -format jpeg -adaptive-sharpen 100 -unsharp 50 -quality 100
find $convertedFolder_l -type f -iname \*.jpg -exec mv {} $uploadInProg \;

##Mogrify - Format as _m jpg and Alt Thumb
cp -pR $convertedFolder_alt $convertedFolder_m
cd $convertedFolder_m
mogrify '*.jpg[200x240]' -compress none -format jpeg -adaptive-sharpen 100 -unsharp 40 -quality 100
find $convertedFolder_m -type f -iname \*.jpg -exec mv {} $uploadInProg \;

##Mogrify - Format as Primary PNG, store originalRetouched
cd $convertedFolder_png
mogrify -format png '*.jpg' -define png:preserve-colormap -define png:format=png24 -define png:compression-level=N -define png:compression-strategy=N -define png:compression-filter=N -quality 100 -adaptive-sharpen 50 -unsharp 75
find $convertedFolder_png -type f -iname \*.png -exec mv {} $uploadInProg \;
find $convertedFolder_png -type f -iname \*.jpg -exec rm {} \;
##Mogrify - Format as Alt PNG
cd $convertedFolder_alt
mogrify -format png '*alt*.jpg' -define png:preserve-colormap -define png:format=png24 -define png:compression-level=N -define png:compression-strategy=N -define png:compression-filter=N -quality 100 -adaptive-sharpen 50 -unsharp 75
find $convertedFolder_alt -type f -iname \*alt*.png -exec mv {} $uploadInProg \;
find $convertedFolder_alt -type f -iname \*.jpg -exec rm {} \;

#### Original stored
batchDoneFolder="/mnt/johnb/Desktop/batchDone/$batchDoneDate"
mkdir $batchDoneFolder
for f in `find $batchDtop -iname \*.jpg`
do
exiftool -m -P -fast2 -overwrite_original -"IPTC:DateOriginalRetouchProcessed"="$Today" $f
mv -f $f $batchDoneFolder
done;

##########			##########	 Upload Files via FTP through cUrl
ftpLoginFull="ftp://file3.bluefly.corp/ImageDrop/ --user imagedrop:imagedrop0"
## weddavLogin="https://imagedrop:imagedrop0@file3.bluefly.corp/ImageDrop/"

### for Find only jp'g' and pn'g' files
for f in `find $uploadInProg -type f -iname \*.*g`
do
uploadResult=`curl -k -T $f $ftpLoginFull`
exiftool -m -P -fast2 -overwrite_original -'IPTC:DateLoaded'='$Today' $f
mv -f $f $uploadComplete;
echo "$Today, $f, $uploadResult" >> $LOGDIR/uploadLog.txt
done;
