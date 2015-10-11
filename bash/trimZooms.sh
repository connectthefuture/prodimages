#!/bin/bash
. ~/.bash_profile

#foldername=/Users/johnb/Downloads/bella42413/bellaapendix/one/324264801/324264801_1.jpg
foldername="$1"
#foldername="/Users/johnb/Downloads/bella42413/test/magickBase/tmpArch/FilesToBatch_FromPublicDrop/324193001_1.jpg"
tests=`find "$foldername" -type f -iname \*.\*g`
countFiles=`echo $tests | xargs -n1 | wc -l`
## CMYK Profile Files
#cmyk_uswebcoat="/usr/local/color_profiles/standard/USWebCoatedSWOP.icc"
#cmyk_ussheetfedcoat="/usr/local/color_profiles/standard/USSheetfedCoated.icc"
#cmyk_jpn01coat="/usr/local/color_profiles/standard/JapanColor2001Coated.icc"
#cmyk_FOGRA39coat="/usr/local/color_profiles/standard/CoatedFOGRA39.icc"
#cmyk_FOGRA27coat="/usr/local/color_profiles/standard/CoatedFOGRA27.icc"

## RGB Profile Files
#adobe98="/usr/local/color_profiles/standard/AdobeRGB1998.icc"
srgb_webrdy="/usr/local/color_profiles/standard/sRGB.icm"

echo "File Count " $countFiles
echo "Converted From " $foldername " File Count " $countFiles " Started At " `date | sed 's/ /_/g'` >> "$LOGDIR"/magick_logs/conversion-log_"$TODAY".txt
for f in $tests
do

fname=`basename $f | sed 's/.jpg//g'`
dname=`dirname $f`

#dmenwidth=`identify -verbose $f | grep "Geometry" | grep -e "[0-9,{1,4}]x[0-9,{1,4}]" | sed -E 's/\+0\+0//g' | sed -E 's/Geometry\://g' | sed -E 's/\ //g' | awk -Fx '{ print $1 }'`
#dmenheight=`identify -verbose $f | grep "Geometry" | grep -e "[0-9,{1,4}]x[0-9,{1,4}]" | sed -E 's/\+0\+0//g' | sed -E 's/Geometry\://g' | sed -E 's/\ //g' | awk -Fx '{ print $2 }'`
#domclr=`convert $f -posterize 3 -define histogram:unique-colors=true -format "%c" histogram:info:- | sort -k 1 -r | sed 's/(  /(/g' | sed 's/(  /(/g' | sed 's/,  /,/g' | sed 's/, /,/g' | head -n 1 | awk '{ print "srgb"$2 }'`
#if [ "$domclr" != "srgb(255,255,255)" ] ;
#    then
#    convert $f -format jpg -profile $rgbprofile -crop \
#        `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
#        -format '%wx%h%O' \
#        info:` +repage -gravity center -resize '1400x1680' -profile $srgb_webrdy +repage -extent '1500x1800' -colorspace sRGB -unsharp 10 -quality 85 "$f"_new.jpg ;
#else

convert $f -format jpg -profile $srgb_webrdy -crop \
  `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
   -format '%wx%h%O' \
   info:` -background white +repage -gravity center -resize '500x' -profile $srgb_webrdy -background white +repage -extent '600x720' -colorspace sRGB -unsharp 15 -quality 85 "$f"_new.jpg
#fi ;



mv "$f"_new.jpg "$f"

echo $fname `date | sed 's/ /_/g'`
echo $fname `date | sed 's/ /_/g'` >> "$LOGDIR"/magick_logs/conversion-log_"$TODAY".txt

done ;
