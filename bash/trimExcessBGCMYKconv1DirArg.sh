#!/bin/bash
. ~/.bash_profile



#foldername=/Users/johnb/Downloads/bella42413/bellaapendix/one/324264801/324264801_1.jpg
foldername="$1"
#foldername="/Users/johnb/Downloads/bella42413/test/magickBase/tmpArch/FilesToBatch_FromPublicDrop/324193001_1.jpg"
tests=`find "$foldername" -type f -iname \*.\*g`
countFiles=`echo $tests | xargs -n1 | wc -l`
## CMYK Profile Files
cmyk_uswebcoat="/usr/local/color_profiles/standard/USWebCoatedSWOP.icc"
cmyk_ussheetfedcoat="/usr/local/color_profiles/standard/USSheetfedCoated.icc"
cmyk_jpn01coat="/usr/local/color_profiles/standard/JapanColor2001Coated.icc"
cmyk_FOGRA39coat="/usr/local/color_profiles/standard/CoatedFOGRA39.icc"
cmyk_FOGRA27coat="/usr/local/color_profiles/standard/CoatedFOGRA27.icc"

## RGB Profile Files
adobe98="/usr/local/color_profiles/standard/AdobeRGB1998.icc"
srgb_webrdy="/usr/local/color_profiles/standard/sRGB.icm"

echo "File Count " $countFiles
echo "Converted From " $foldername " File Count " $countFiles " Started At " `date | sed 's/ /_/g'` >> "$LOGDIR"/magick_logs/conversion-log_"$TODAY".txt 
for f in $tests
do

fname=`basename $f | sed 's/.jpg//g'`
dname=`dirname $f`
dmenwidth=`identify -verbose $f | grep "Geometry" | grep -e "[0-9,{1,4}]x[0-9,{1,4}]" | sed -E 's/\+0\+0//g' | sed -E 's/Geometry\://g' | sed -E 's/\ //g' | awk -Fx '{ print $1 }'`

dmenheight=`identify -verbose $f | grep "Geometry" | grep -e "[0-9,{1,4}]x[0-9,{1,4}]" | sed -E 's/\+0\+0//g' | sed -E 's/Geometry\://g' | sed -E 's/\ //g' | awk -Fx '{ print $2 }'`

domclr=`convert $f -posterize 3 -define histogram:unique-colors=true -format "%c" histogram:info:- | sort -k 1 -r | sed 's/(  /(/g' | sed 's/(  /(/g' | sed 's/,  /,/g' | sed 's/, /,/g' | head -n 1 | awk '{ print "srgb"$2 }'`

aspct=`echo $dmenwidth/$dmenheight | bc`

clrsp=`identify $f | awk '{ print $6 }'`


#echo $infomag | awk -F\+ '{ print $1 }' | awk -Fx '{ print $1 }'
#infomag=`convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
#                 -format '%wx%h%O' \
#                 info:`

if [ "$clrsp" = "CMYK" ];
then
    
    clrprofilename=`identify -verbose "$f" | grep "Profile-icc" -A2 | grep "Description" | sed 's/Description\:\ //g' | sed 's/^ *//g'`
    if [ "$clrprofilename" = "Japan Color 2001 Coated" ];
    then
        cmykprofile="$cmyk_jpn01coat" ;
    elif [ "$clrprofilename" = "U.S.\ Web\ Coated\ \(SWOP\)\ v2" ];
    then
        cmykprofile="$cmyk_uswebcoat" ;
    elif [ "$clrprofilename" = "U.S.\ Sheetfed\ Coated\ \(SWOP\)\ v2" ];
    then
        cmykprofile="$cmyk_ussheetfedcoat" ;
    elif [ "$clrprofilename" = "FOGRA39coat" ];
    then
        cmykprofile="$cmyk_FOGRA39coat" ;
    elif [ "$clrprofilename" = "FOGRA27coat" ];
    then
        cmykprofile="$cmyk_FOGRA27coat" ;
    else
        cmykprofile="$cmyk_jpn01coat" ;
    fi;
    
    
    if [ "$dmenwidth" -gt "$dmenheight" ];
    then
        verhoriz="horizontal"
        #hrzdir=`mkdir "$foldername"/"HORIZONTAL"`
        if [ "$dmenheight" -eq "2400" ] ;
        then
            convert $f -format jpg -profile $cmykprofile -crop \
                `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
                -format '%wx%h%O' \
                info:` -background white +repage -gravity center -profile $srgb_webrdy -background white +repage -extent '2000x2400' -colorspace sRGB -unsharp 50 -quality 100 "$f"_new.jpg ;
        else
            convert $f -format jpg -profile $cmykprofile -crop \
                `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
                -format '%wx%h%O' \
                info:` -background white +repage -gravity center -resize '1400x1680' -profile $srgb_webrdy -background white +repage -extent '1500x1800' -colorspace sRGB -unsharp 50 -quality 100 "$f"_new.jpg ;
        fi;
        
    elif [ "$dmenwidth" -eq "$dmenheight" ];
    then
        verhoriz="square"
       
        convert $f -format jpg -profile $cmykprofile -crop \
            `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
            -format '%wx%h%O' \
            info:` -background white +repage -gravity center -resize '1400x1680' -profile $srgb_webrdy -background white +repage -extent '1500x1800' -colorspace sRGB -unsharp 50 -quality 100 "$f"_new.jpg ;
    else
        verhoriz="vertical"

        if [ "$domclr" = "srgb(255,255,255)" ] ;
        then
            convert $f -format jpg -profile $cmykprofile -crop \
                `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
                -format '%wx%h%O' \
                info:` -background white +repage -gravity center -resize '1400x1680' -profile $srgb_webrdy -background white +repage -extent '1500x1800' -colorspace sRGB -unsharp 50 -quality 100 "$f"_new.jpg ;
        else
            if [ "$dmenheight" != "2400" ] && [ "$dmenwidth" != "2000" ] || [ "$dmenheight" != "1680" ] && [ "$dmenwidth" != "1400" ] || [ "$dmenheight" != "1800" ] && [ "$dmenwidth" != "1500" ];
            then
                
                if [ "$dmenheight" -eq "2400" ] ; 
                then
                    convert $f -format jpg -profile $cmykprofile -crop \
                        `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
                        -format '%wx%h%O' \
                        info:` -background white +repage -gravity center -profile $srgb_webrdy -background white +repage -extent '2000x2400' -colorspace sRGB -unsharp 50 -quality 100 "$f"_new.jpg ;
                else
                
                    convert $f -format jpg -profile $cmykprofile -crop \
                        `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
                        -format '%wx%h%O' \
                        info:` -background white +repage -gravity center -resize '1400x1680' -profile $srgb_webrdy -background white +repage -extent '1500x1800' -colorspace sRGB -unsharp 50 -quality 100 "$f"_new.jpg
                fi ;
            else
                    convert $f -format jpg -profile $cmykprofile +repage -profile $srgb_webrdy -background white +repage -colorspace sRGB -quality 100 "$f"_new.jpg ;
            fi;
            
        fi ;

    fi ;
#####    RGB BELOW CMYK ABOVE
else

        clrprofilename=`identify -verbose "$f" | grep "Profile-icc" -A2 | grep "Description" | sed 's/Description\:\ //g' | sed 's/^ *//g'`
        if [ "$clrprofilename" = "Adobe\ RGB\ \(1998\)" ];
        then
            rgbprofile="$adobe98" ;
        elif [ "$clrprofilename" = "sRGB\ IEC61966\-2.1" ];
        then
            rgbprofile="$srgb_webrdy" ;
        else
            rgbprofile="$srgb_webrdy" ;
        fi;




    if [ "$dmenwidth" -gt "$dmenheight" ];
    then
        verhoriz="horizontal"
        
        if [ "$dmenheight" -eq "2400" ] ; 
        then
            convert $f -format jpg -profile $rgbprofile -crop \
                `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
                -format '%wx%h%O' \
                info:` -background white +repage -gravity center -profile $srgb_webrdy -background white +repage -extent '2000x2400' -colorspace sRGB -unsharp 50 -quality 100 "$f"_new.jpg  ;
        else
            convert $f -format jpg -profile $rgbprofile -crop \
                `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
                -format '%wx%h%O' \
                info:` -background white +repage -gravity center -resize '1400x1680' -profile $srgb_webrdy -background white +repage -extent '1500x1800' -colorspace sRGB -unsharp 50 -quality 100 "$f"_new.jpg ;
        fi;

    elif [ "$dmenwidth" -eq "$dmenheight" ];
    then
        verhoriz="square"
        
        convert $f -format jpg -profile $srgb_webrdy -crop \
            `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
            -format '%wx%h%O' \
            info:` -background white +repage -gravity center -resize '1400x1680' -profile $srgb_webrdy -background white +repage -extent '1500x1800' -colorspace sRGB -unsharp 50 -quality 100 "$f"_new.jpg ;
        
    else
        verhoriz="vertical"
            
        if [ "$domclr" = "srgb(255,255,255)" ] ;
        then
            convert $f -format jpg -profile $rgbprofile -crop \
                `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
                -format '%wx%h%O' \
                info:` -background white +repage -gravity center -resize '1400x1680' -profile $srgb_webrdy -background white +repage -extent '1500x1800' -colorspace sRGB -unsharp 50 -quality 100 "$f"_new.jpg ;
        else
            if [ "$dmenheight" != "2400" ] && [ "$dmenwidth" != "2000" ] || [ "$dmenheight" != "1680" ] && [ "$dmenwidth" != "1400" ] || [ "$dmenheight" != "1800" ] && [ "$dmenwidth" != "1500" ];
            then        
                if [ "$dmenheight" -eq "2400" ] ; 
                then
                    convert $f -format jpg -profile $rgbprofile -crop \
                        `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
                        -format '%wx%h%O' \
                        info:` -background white +repage -gravity center -profile $srgb_webrdy -background white +repage -extent '2000x2400' -colorspace sRGB -unsharp 50 -quality 100 "$f"_new.jpg ;
                else
                
                    convert $f -format jpg -profile $rgbprofile -crop \
                        `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
                        -format '%wx%h%O' \
                        info:` -background white +repage -gravity center -resize '1400x1680' -profile $srgb_webrdy -background white +repage -extent '1500x1800' -colorspace sRGB -unsharp 50 -quality 100 "$f"_new.jpg
                fi ;
            
        
            else
                convert $f -format jpg -profile $rgbprofile +repage -profile $srgb_webrdy -background white +repage -colorspace sRGB -quality 100 "$f"_new.jpg ;
            fi ;
        fi ;
    fi ;

fi;



mv "$f"_new.jpg "$f"

echo $fname $dmenwidth $dmenheight $domclr $verhoriz $clrsp $clrprofilename `date | sed 's/ /_/g'`
echo $fname $dmenwidth $dmenheight $domclr $verhoriz $clrsp $clrprofilename `date | sed 's/ /_/g'` >> "$LOGDIR"/magick_logs/conversion-log_"$TODAY".txt

done ;
