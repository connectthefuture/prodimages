#!/bin/bash
. ~/.bash_profile
Today=`date +%Y-%m-%d`

#####    Remove Bad Files
## Use grep & xargs like using -exec mv
#find $1 -type f -iname \*.* | grep ' ' | xargs -I '{}' mv -f '{}' $2


#if [ "$#" -eq 1 ]; then
#    ## If the sysargv1 listing has more jpgs than directories, dont decend dirs and do the root dir only
#    echo "1Arg"
#    rootdir="$1"
#    dirs=`find "$rootdir" -type d -wholename \*/[3-9][0-9][0-9][0-9]/\* -mindepth 1 -maxdepth 1`
#elif [ "$#" -lt 1 ]; then
#    echo "Zero"
#    rootdir=/mnt/Production_Raw/.zImages_1
#    dirs=`find "$rootdir" -type d -wholename \*/[3-9][0-9][0-9][0-9]/\* -mindepth 1 -maxdepth 2 -atime -7`
#    #identify -precision 5 -define identify:locate=maximum -define identify:limit=3
#elif [ "$#" -gt 1 ]; then
#    echo "2Plus"
#    dirs="$@"  
#    ##=`find "$@" -type d -maxdepth 1 -wholename \*/[3-9][0-9][0-9][0-9]/\*`
#fi;



#for d in "$dirs"; do
#    #echo "33Find"
#    echo $d
for f in `find "$1" -type f -wholename \*\/[^.]\*\[0-9].jp[g$] -mindepth 1 -maxdepth 1`; do 
## First Test if a thumb has already been made and skip if exists since it is a long process and waste to redo
#if [[ `test -f "$f"_thumb` -gt 0 ]]; then
    if [ -s "$f"_thumb ]; then
            echo ThumbExists_"$f"
    
    elif [ ! -s "$f"_thumb ]; then
        echo Created"$f"_thumb     
        convert "$f" -auto-orient \
            -background "rgb(255,255,255)" \
            -filter Mitchell \
            -resize 600x \
            -unsharp 10% \
            -quality 65% "$f"_thumb; 
    
    fi;

done;
#done;
    
    #echo "MAKINGTHUMb77"
# -filter sinc \
# -set filter:window=jinc \
# -set filter:lobes=8 \
# -resize 150%

#-draw 'bezier 20,50 45,100 45,0 70,50'
#else
#    echo "$f"_thumb"AlreadyExists"
#fi;

