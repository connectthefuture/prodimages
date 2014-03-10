#!/bin/bash
. ~/.bash_profile
Today=`date +%Y-%m-%d`

#####    Remove Bad Files
## Use grep & xargs like using -exec mv
#find $1 -type f -iname \*.* | grep ' ' | xargs -I '{}' mv -f '{}' $2


if [ "$#" -lt 1 ]; then
    
    echo "1"
    rootdir=/mnt/Production_Raw/.zImages_1
    dirs=`find "$rootdir" -type d -wholename \*/[3-9][0-9][0-9][0-9]/\* -maxdepth 1 -atime -3`
    #identify -precision 5 -define identify:locate=maximum -define identify:limit=3

elif [ "$#" -gt 1 ]; then
    
    echo "2"
    dirs="$@"  
    ##=`find "$@" -type d -maxdepth 1 -wholename \*/[3-9][0-9][0-9][0-9]/\*`

elif [ "$#" -eq 1 ]; then
    ## If the sysargv1 listing has more jpgs than directories, dont decend dirs and do the root dir only
    echo "3"
    #dirs=`find "'"$1"'" -type d -wholename \*/[3-9][0-9][0-9][0-9]/\* -maxdepth 1 -atime -3`
    
    #if [ `echo "$dirs" | wc -l` -lt `find "$dirs" -name \*\.jp[g$] -maxdepth 1 -atime -3 | wc -l` ];
    #then
    dirs="$1"
    #fi;

fi;


for d in "$dirs"; do
    #echo "33Find"

for f in `find "$d" -type f -wholename \*\/[^.]\*\.jp[g$] -maxdepth 2`; do 
## First Test if a thumb has already been made and skip if exists since it is a long process and waste to redo
#if [[ `test -f "$f"_thumb` -gt 0 ]]; then
    echo $f
    convert "$f" -auto-orient \
        -background "rgb(255,255,255)" \
        -filter Mitchell \
        -resize 600x \
        -unsharp 10% \
        -quality 65% "$f"_thumb.jpg; 
    
    echo "MAKINGTHUMb77"
# -filter sinc \
# -set filter:window=jinc \
# -set filter:lobes=8 \
# -resize 150%

#-draw 'bezier 20,50 45,100 45,0 70,50'
#else
#    echo "$f"_thumb"AlreadyExists"
#fi;

done; 
done;
