#!/bin/bash
. ~/.bash_profile

testsf="/Users/johnb/Pictures/new/ttt"

tests=`find "$testsf" -type f -iname \*.\*g`
for test in $tests
do
#convert $test \
#           \( +clone -fill black -colorize 100% \
#              -fill white -draw 'circle 114,75 110,2' \
#           \) -alpha off -compose CopyOpacity -composite \
#           -trim +repage "$test"_shape.png
mogrify -format jpg -colorspace RGB -resize 1200x1440 -background white -gravity center -extent 1400x1680 -colorspace sRGB $test


#convert $test -modulate 5,255,255  -colorspace HSL \
#          -channel R -separate +channel \
#          \( -clone 0 -background none -fuzz 5% +transparent grey64 \) \
#          \( -clone 1 -background none -fuzz 10% -transparent black \) \
#          -delete 0,1  -alpha extract  -compose multiply -composite -colorspace sRGB "$test"_new
convert $test \( +clone -fx 'p{0,0}' \) \
          -compose Difference -composite  \
          -modulate 100,0  -threshold 10% -alpha off "$test"_difference.png

convert "$test"_difference.png  -threshold 20% -blur 0x0.7 boolean_mask.png
convert $test boolean_mask.png \
          -alpha off -compose CopyOpacity -composite \
          "$test"_boolean.png

convert "$test"_boolean.png \
           \( +clone -fill black -colorize 100% \
              -fill white -draw 'rectangle 0,0 1200,1440' \
           \) -alpha off -compose CopyOpacity -composite \
           -trim +repage "$test"_shape.png
        
convert "$test"_shape.png \
           \( +clone -alpha extract -virtual-pixel black \
              -gamma 2 +level 50,100 -white-threshold 99 \
              -morphology Distance Euclidean:4,10! \
              -sigmoidal-contrast 3,0% \
           \) -compose CopyOpacity -composite \
           -colorspace sRGB "$test"_feathered.png

convert "$test"_shape.png \
           \( +clone -alpha extract -virtual-pixel black \
              -gamma 2 +level 50,100 -white-threshold 99 \
              -morphology Distance Euclidean:4,10! \
              -sigmoidal-contrast 3,0% \
           \) -compose CopyOpacity -composite \
           -colorspace sRGB "$test"_feathered.png

convert "$test"_feathered.png \( +clone -fx 'p{0,0}' \) \
          -compose Difference -composite  \
          -modulate 100,0  -threshold 10% -alpha off "$test"_difference9.png
#convert "$test"_feathered.png \
#           \( +clone -alpha extract -virtual-pixel black \
#              -gamma 2 +level 0,100 -white-threshold 99 \
#              -morphology Distance Euclidean:4,10! \
#              -sigmoidal-contrast 3,0% \
#           \) -compose CopyOpacity -composite \
#           -colorspace sRGB "$test"_feathered2.png

#convert -crop 1200x1400 -gravity center -colorspace sRGB "$test"_feathered2.png



#convert $test \( +clone -fx 'p{0,0}' \) \
#          -compose Difference -composite  \
#          -modulate 100,0  -alpha off  "$test"difference.png
#
#convert "$test"difference.png  -threshold 20% -blur 0x0.07 boolean_mask.png
#convert $test  boolean_mask.png \
#          -alpha off -compose CopyOpacity -composite \
#          "$test"_boolean.png
#        

done        
    