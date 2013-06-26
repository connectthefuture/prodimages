#!/bin/bash

. ~/.bash_profile

cd "$1"
for file in `find "$1" -maxdepth 1 -type f -iname \*.\*g`; 
do 
name=`basename $file | sed 's/.jpg//g' | sed 's/.png//g'` ;
mogrify -format jpg -resize 350x432 -background white -gravity center -extent 400x480 $file ; 
mv "$name".jpg "$name"_l.jpg ;
done ;
