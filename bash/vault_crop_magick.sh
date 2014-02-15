#!/bin/bash
. ~/.bash_profile

#def subproc_magick_large_jpg(imgdir):
#    import subprocess,os,re
#
#    ### Change to Large jpg dir to Mogrify using Glob
#    os.chdir(imgdir)
#    
#    subprocess.call([
#    "convert", 
#    "$f",
#    "-format", 
#    "jpg",
#    "-crop",
#    "`convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
#    -format '%wx%h%O' \
#    info:`",
#     
#    "-background",
#    "white", 
#    "+repage", 
#    "-gravity", 
#    "center", 
#    "-resize", 
#    "'500x'", 
#    "-background", 
#    "white",
#    "+repage", 
#    "-extent", 
#    "'600x720'", 
#    "-colorspace",
#    "sRGB", 
#    "-unsharp", 
#    "15", 
#    "-quality",
#    "85",
#
# 
#"$f"_new.jpg
#

## CMYK Profile Files
cmyk_uswebcoat="/usr/local/color_profiles/standard/USWebCoatedSWOP.icc"
cmyk_ussheetfedcoat="/usr/local/color_profiles/standard/USSheetfedCoated.icc"
cmyk_jpn01coat="/usr/local/color_profiles/standard/JapanColor2001Coated.icc"
cmyk_FOGRA39coat="/usr/local/color_profiles/standard/CoatedFOGRA39.icc"
cmyk_FOGRA27coat="/usr/local/color_profiles/standard/CoatedFOGRA27.icc"

## RGB Profile Files
adobe98="/usr/local/color_profiles/standard/AdobeRGB1998.icc"
srgb_webrdy="/usr/local/color_profiles/standard/sRGB.icm"


foldername="$1"
#foldername="/Users/johnb/Downloads/bella42413/test/magickBase/tmpArch/FilesToBatch_FromPublicDrop/324193001_1.jpg"
fileslist=`find "$foldername" -type f -iname \*.\*pg`

for f in $fileslist; do


fname=`basename $f | sed 's/.jpg//g'`
dname=`dirname $f`
dmenwidth=`identify -verbose $f | grep "Geometry" | grep -e "[0-9,{1,4}]x[0-9,{1,4}]" | sed -E 's/\+0\+0//g' | sed -E 's/Geometry\://g' | sed -E 's/\ //g' | awk -Fx '{ print $1 }'`
dmenheight=`identify -verbose $f | grep "Geometry" | grep -e "[0-9,{1,4}]x[0-9,{1,4}]" | sed -E 's/\+0\+0//g' | sed -E 's/Geometry\://g' | sed -E 's/\ //g' | awk -Fx '{ print $2 }'`
domclr=`convert $f -posterize 1 -define histogram:unique-colors=true -format "%c" histogram:info:- | sort -k 1 -r | sed 's/(  /(/g' | sed 's/(  /(/g' | sed 's/,  /,/g' | sed 's/, /,/g' | head -n 1 | awk '{ print "srgb"$2 }'`
aspct=`echo $dmenwidth/$dmenheight | bc`
clrsp=`identify $f | awk '{ print $6 }'`



echo $domclr

if [ "$domclr" = "srgb(255,255,255)" ]; then
    convert $f -format jpg -profile $srgb_webrdy -crop \
        `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
        -format '%wx%h%O' \
        info:` -background white +repage -gravity center -resize '1400x1680' -profile $srgb_webrdy -background white +repage -extent '1500x1800' -colorspace sRGB -unsharp 50 -quality 100 "$f"_new.jpg ;

        if [ "$dmenheight" -gt "1500" ]; then
            convert $f -format jpg -profile $srgb_webrdy -crop \
                `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
                -format '%wx%h%O' \
                info:` -background white +repage -gravity center  -resize '1400x1680' -profile $srgb_webrdy -background white +repage -extent '1500x1800' -colorspace sRGB -unsharp 50 -quality 100 "$f"_new.jpg ;
        else
            convert $f -format jpg -profile $srgb_webrdy -crop \
                `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
                -format '%wx%h%O' \
                info:` -background white +repage -gravity center -resize '1200x1440' -profile $srgb_webrdy -background white +repage -extent '1250x1500' -colorspace sRGB -unsharp 50 -quality 100 "$f"_new.jpg
        fi ;

fi ;

done;