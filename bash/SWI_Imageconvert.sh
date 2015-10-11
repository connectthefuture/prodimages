#!/bin/bash
. ~/.bash_profile

#foldername=/Users/johnb/Downloads/bella42413/bellaapendix/one/324264801/324264801_1.jpg
foldername="$1"
#foldername="/Users/johnb/Downloads/bella42413/test/magickBase/tmpArch/FilesToBatch_FromPublicDrop/324193001_1.jpg"
tests=`find "$foldername" -type f -iname \*.\*g`
countFiles=`echo $tests | xargs -n1 | wc -l`

## RGB Profile Files
adobe98="/usr/local/color_profiles/standard/AdobeRGB1998.icc"
srgb_webrdy="/usr/local/color_profiles/standard/sRGB.icm"

echo "File Count " $countFiles
#echo "Converted From " $foldername " File Count " $countFiles " Started At " `date | sed 's/ /_/g'` >> "$LOGDIR"/magick_logs/conversion-log_"$TODAY".txt 
for f in $tests
do

fname=`basename $f | sed 's/.jpg//g'`
dname=`dirname $f`
dmenwidth=`identify -verbose $f | grep "Geometry" | grep -e "[0-9,{1,4}]x[0-9,{1,4}]" | sed -E 's/\+0\+0//g' | sed -E 's/Geometry\://g' | sed -E 's/\ //g' | awk -Fx '{ print $1 }'`

dmenheight=`identify -verbose $f | grep "Geometry" | grep -e "[0-9,{1,4}]x[0-9,{1,4}]" | sed -E 's/\+0\+0//g' | sed -E 's/Geometry\://g' | sed -E 's/\ //g' | awk -Fx '{ print $2 }'`

domclr=`convert $f -posterize 3 -define histogram:unique-colors=true -format "%c" histogram:info:- | sort -k 1 -r | sed 's/(  /(/g' | sed 's/(  /(/g' | sed 's/,  /,/g' | sed 's/, /,/g' | head -n 1 | awk '{ print "srgb"$2 }'`

aspct=`echo $dmenwidth/$dmenheight | bc`

clrsp=`identify $f | awk '{ print $6 }'`

echo $dmenwidth $dmenheight $domclr $aspct $clrsp

if [ "$dmenwidth" -lt "$dmenheight" ];

then
    verhoriz="vertical"

if [ "$dmenheight" -lt "888" ] ;
then
    convert $f -format jpg -crop \
    `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
    -format '%wx%h%O' \
    info:` -background white +repage -gravity center -resize '1100x1320' -background white +repage -extent '1700x2040' -colorspace sRGB -adaptive-sharpen 50 -quality 100 "$f"_new.jpg ;

else
    convert $f -format jpg -crop \
    `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
    -format '%wx%h%O' \
    info:` -background white +repage -gravity center -resize '1300x1560' -background white +repage -extent '1700x2040' -colorspace sRGB -adaptive-sharpen 50 -quality 100 "$f"_new.jpg ;
fi;
   
else
   verhoriz="horizontal"
   #if [ "$dmenheight" -lt "888" ] ;
   
if [ "$domclr" = "srgb(255,255,255)" ] ;
then
   convert $f -format jpg -crop \
   `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
   -format '%wx%h%O' \
   info:` -background white +repage -gravity center -resize '1300x1560' -background white +repage -extent '1700x2040' -colorspace sRGB -adaptive-sharpen 50 -quality 100 "$f"_new.jpg ;
else
      
      convert $f -format jpg +repage -background white +repage -gravity center -resize '1300x1560' -background white +repage -extent '1700x2040' -colorspace sRGB -adaptive-sharpen 50 -quality 100 "$f"_new.jpg ;
  fi;
fi ;
done;
