#!/bin/bash
#. ~/.bash_profile

start=`date`
echo "Started At: "$start
foldername="$1"
filenames=`find "$foldername" -type f -iname \*.\*g`;
countFiles=`echo $filenames | xargs -n1 | wc -l`;

## RGB Profile Files
#adobe98="/usr/local/color_profiles/standard/AdobeRGB1998.icc"
#srgb_webrdy="/usr/local/color_profiles/standard/sRGB.icm"
cd $foldername
curdir=`pwd`
##upload_complete=/mnt/Post_Complete/.Vendor_to_Load/upload_complete  ### For Final
upload_complete="$curdur"/../"$foldername"_arch
mkdir $upload_complete

echo "File Count " $countFiles
for f in $filenames
do

##1A## Prep Zoom sized PNG by Enlarging image by 50%. Finish by padding white to reach 1800x2160 Zoom size. Save as Jpeg to convert to PNG
convert $f -format jpg -crop \
                `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
                -format '%wx%h%O' \
                info:` -background white +repage -gravity center -resize '1100x1320' -background white +repage -extent '1800x2160' -colorspace sRGB -unsharp 25 -quality 100 "$f"_new.jpg


##1B## Make PNG for Zoom cropped to bounds of subject in image and enlarge by 50%. Finish by padding white to reach 1800x2160 Zoom size
mogrify -format png "$f"_new.jpg -define png:preserve-colormap \
                -define png:format=png24 -define png:compression-level=N -define png:compression-strategy=N \
                -define png:compression-filter=N -quality 100 -adaptive-sharpen 50 -unsharp 75
                
##
##1C## Delete Temp Jpeg now that Zoom PNG created plus Remove extraaneous chars
mv "$f"_new.png "${f//.jpg}.png"

rm "$f"_new.jpg


##
##2## Make Large Jpg BC List page cropped to bounds of subject in image Uses original File not enlarged Zoom
convert $f -format jpg -crop \
                `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
                -format '%wx%h%O' \
                info:` -background white +repage -gravity center -resize 'x480' -background white +repage -extent '400x' -colorspace sRGB -adaptive-sharpen 25 -unsharp 25 -quality 100 "${f//.jpg}_l.jpg"

##
##3## Make Medium Bfly List page Jpg cropped to bounds of subject in image Uses original File not enlarged Zoom              
convert $f -format jpg -crop \
                `convert "$f" -virtual-pixel edge -blur 0x15 -fuzz 1% -trim \
                -format '%wx%h%O' \
                info:` -background white +repage -gravity center -resize 'x240'  -background white +repage -extent '200x' -colorspace sRGB -adaptive-sharpen 25 -unsharp 10 -quality 100 "${f//.jpg}_m.jpg"
                        

##
##
###Move Original to Archive
mv $f "$archdir"/

echo "Processed: $f"
let "countFiles -= 1" ;
echo "File Count " $countFiles
done;

end=`date` 
echo "Finished At: "$end