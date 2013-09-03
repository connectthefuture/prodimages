#!/bin/bash

. ~/.bash_profile


file4Images=/mnt/Company/Production/Images/Kayla
i7RsyncTmp=$PRODSRV/var/consignment/rsync_file4_tmp


### Rename all Files in all File4Img Directories replacing capital JPG with lowercase jpg
for f in `find $file4Images -type f -iname \*.\*g`
do
echo "$f"
     FILENAME="${f//.JPG/.jpg}";
     mv -f "$f" "$FILENAME"
done;

### Rename all Directories With BadChars
# for d in `find $file4Images -type d`
# do
# cd $file4Images ;
# echo "$d"
#  	FILENAME="${d//[\?%\+\:\&\-\#\(\)]/_}";
#  	mv -f "$d" "$FILENAME"
# done;


#Recursively replace all spaces in File Names
for d in `find $file4Images -type d`
do
    cd $d
    for subd in `find $d -type d`
    do
        cd $subd
        ls -1 | while read file; do new_file=$(echo $file | sed 's/\ /_/g'); 
        mv "$file" "$new_file"; 
        done;
    done;
done;

## Run Rsync
/usr/bin/rsync --archive --compress --update --exclude '/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/archived' --verbose $file4Images/ $i7RsyncTmp



### Rename the synched folders to the PO number as $NF in directory name
i7RsyncTmp=$PRODSRV/var/consignment/rsync_file4_tmp
imgConvDirTmp=$PRODSRV/var/consignment/images_for_conversion/tmp
imgConvDirFinal=$PRODSRV/var/consignment/images_for_conversion


mkdir $imgConvDirTmp;

cd $i7RsyncTmp && ls -1 | while read directory; 
do 
new_dir=$(echo $directory | awk -v finaldir="$imgConvDirTmp" -F_ '{ print finaldir"/"$NF }');
cp -R "$directory" "$new_dir"; 
done;

### Recursively rename all files to Bluefly numbers in Dirs in tmp---Then move up 1 level to final consignment dir
# for d in `find $imgConvDirTmp -type d -2h -iname \*[0-9,{6}]`
# do 
# ponum=`basename $d`
# queryDirIterateVendor.sh "$imgConvDirTmp"/"$ponum" "$ponum"
# done;
# 
# ## MAGICK LOAD--Then Sync up 1 level
# for podir in `find $imgConvDirTmp -type d -mtime -2h -iname \*[0-9,{6}]`
# do
# magickPortable1DirArg.sh "$podir"
# done;

## Rsync from tmp to images for conversion Final
/usr/bin/rsync --archive --compress --update --verbose $imgConvDirTmp/ $imgConvDirFinal

rm -R $imgConvDirTmp

