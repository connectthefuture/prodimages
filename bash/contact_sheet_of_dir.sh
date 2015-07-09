#!/bin/bash

. ~/.bash_profile
#convert -format jpg $1 -depth 8 -density 72 -units pixelsperinch -fill grey50 -colorize 40 miff:- | 

#composite -dissolve 15 - -colorspace sRGB -quality 95 ~/virtualenvs/GitHub-prodimages/python/jbmodules/image_processing/magick_tweaks/img/Bluefly_Logo_WatermarkSmall.png "$2"$(basename "$1")


#echo ${JOHJ/J/JPEG}

montage -verbose -label '%f' -font Ubuntu -pointsize 10 -background '#000000' -frame 1 -fill 'white' -define jpeg:size=150x180 -geometry 150x180+2+4 -auto-orient "$1"/\*.jpg "$1"/shotlist.jpg
