#!/bin/bash
. ~/.bash_profile




#foldername="$1"
foldername="/Users/johnb/Pictures/new/117546copy"
tests=`find "$foldername" -type f -iname \*.\*g`

## CMYK Profile Files
cmyk_uswebcoat="/usr/local/color_profiles/standard/USWebCoatedSWOP.icc"
cmyk_ussheetfedcoat="/usr/local/color_profiles/standard/USSheetfedCoated.icc"
cmyk_jpn01coat="/usr/local/color_profiles/standard/JapanColor2001Coated.icc"
cmyk_FOGRA39coat="/usr/local/color_profiles/standard/CoatedFOGRA39.icc"

## RGB Profile Files
adobe98="/usr/local/color_profiles/standard/AdobeRGB1998.icc"
srgb_webrdy="/usr/local/color_profiles/standard/sRGB.icm"


for f in $tests
do

fname=`basename $f | sed 's/.jpg//g'`
dname=`dirname $f`
dmenwidth=`identify -verbose $f | grep "Geometry" | grep -e "[0-9,{1,4}]x[0-9,{1,4}]" | sed -E 's/\+0\+0//g' | sed -E 's/Geometry\://g' | sed -E 's/\ //g' | awk -Fx '{ print $1 }'`

dmenheight=`identify -verbose $f | grep "Geometry" | grep -e "[0-9,{1,4}]x[0-9,{1,4}]" | sed -E 's/\+0\+0//g' | sed -E 's/Geometry\://g' | sed -E 's/\ //g' | awk -Fx '{ print $2 }'`

domclr=`convert $f -posterize 3 -define histogram:unique-colors=true -format "%c" histogram:info:- | sort -k 1 -r | sed 's/(  /(/g' | sed 's/(  /(/g' | sed 's/,  /,/g' | sed 's/, /,/g' | head -n 1 | awk '{ print "srgb"$2 }'`

aspct=`echo $dmenwidth/$dmenheight | bc`

clrsp=`identify $f | awk '{ print $6 }'`
if [ "$clrsp" = "CMYK" ];
then
    


    if [ "$dmenwidth" -gt "$dmenheight" ];
    then
        verhoriz="horizontal"
        #hrzdir=`mkdir "$foldername"/"HORIZONTAL"`
        
        mogrify -format jpg -profile $cmyk_jpn01coat -resize '1200x' -profile $srgb_webrdy -background white -gravity center -extent 1400x1680 -colorspace sRGB $f ;
        #mv $f "$dname"/"$hrzdir"
    elif [ "$dmenwidth" -eq "$dmenheight" ];
    then
        verhoriz="square"
        #sqdir=`mkdir "$foldername"/SQUARE`
        #mv $f $sqdir
        mogrify -format jpg -profile $cmyk_jpn01coat -resize '1200x' -profile $srgb_webrdy -background white -gravity center -extent 1400x1680 -colorspace sRGB $f ;
    else
        verhoriz="vertical"
        #vrtdir=`mkdir "$foldername"/"VERTICAL"`
        if [ "$domclr" = "srgb(255,255,255)" ] ;
        then
            mogrify -format jpg -profile $cmyk_jpn01coat -resize '1400x' -profile $srgb_webrdy -background white -gravity center -extent 1400x1680 -colorspace sRGB $f ;
        else
            mogrify -format jpg -profile $cmyk_jpn01coat -resize '1400x' -profile $srgb_webrdy -background white -gravity north -extent 1400x1680 -colorspace sRGB $f ;
        fi ;
        #mv $f "$dname"/"$vrtdir"
    fi ;

else

    if [ "$dmenwidth" -gt "$dmenheight" ];
    then
        verhoriz="horizontal"
        #hrzdir=`mkdir "$foldername"/"HORIZONTAL"`
        
        mogrify -format jpg -colorspace RGB -resize '1200x' -background white -gravity center -extent 1400x1680 -colorspace sRGB $f ;
        #mv $f "$dname"/"$hrzdir"
    elif [ "$dmenwidth" -eq "$dmenheight" ];
    then
        verhoriz="square"
        sqdir=`mkdir "$foldername"/SQUARE`
        mogrify -format jpg -colorspace RGB -resize '1200x' -background white -gravity center -extent 1400x1680 -colorspace sRGB $f ;
        #mv $f $sqdir
    else
        verhoriz="vertical"
        #vrtdir=`mkdir "$foldername"/"VERTICAL"`
        if [ "$domclr" = "srgb(255,255,255)" ] ;
        then
            mogrify -format jpg -colorspace RGB -resize '1400x' -background white -gravity center -extent 1400x1680 -colorspace sRGB $f ;
        else
            mogrify -format jpg -profile $cmyk_jpn01coat -resize '1400x' -profile $srgb_webrdy -background white -gravity north -extent 1400x1680 -colorspace sRGB $f ;
        fi ;
        #mv $f "$dname"/"$vrtdir"
    fi ;

fi;

echo $fname $dmenwidth $dmenheight $domclr $verhoriz $clrsp 


done