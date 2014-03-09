#!/bin/bash
. ~/.bash_profile
Today=`date +%Y-%m-%d`

#####       Remove Bad Files
## Use grep & xargs
#find $1-type f -iname \*.* | grep ' ' | xargs -I '{}' mv -f '{}' $errorFolder
# if [ `find $REMRUN -mmin -1 -type f | wc -l` -gt 0 ];

if [ "$#" -lt 1 ];
then
    rootdir=/mnt/Production_Raw/.zImages_1
    dirs=`find "$rootdir" -type d -wholename \*/[3-9][0-9][0-9][0-9]/\* -maxdepth 1 -atime -3`
    #identify -precision 5 -define identify:locate=maximum -define identify:limit=3

else if [ "$#" -gt 1 ];
then
    dirs="$@"  ##=`find "$@" -type d -maxdepth 1 -wholename \*/[3-9][0-9][0-9][0-9]/\*`

else
    ## If the sysargv1 listing has more jpgs than directories, dont decend dirs and do the root dir only
    dirs=`find "$1" -type d -wholename \*/[3-9][0-9][0-9][0-9]/\* -maxdepth 1 -atime -3`
    
    if [ `echo "$dirs" | wc -l` -lt `find "$dirs" -name \*\.jp[g$] -maxdepth 1 -atime -3 | wc -l` ];
    then
        dirs="$1"
    fi;

fi;


for d in "$dirs"; 
do 
for f in `find "$d" -type f -maxdepth 1 -atime -3`; 
do 
    convert -auto-orient "$f" -resize 600x \
        -filter Mitchell -compress none -colorspace srgb \
        -format jpeg -adaptive-sharpen 40 -unsharp 40 \
        -quality 60 "$f"_thumb ; 
done; 
done;
