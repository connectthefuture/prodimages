#!/bin/bash

. ~/.bash_profile

searchDir="$1"
dbOutClean="$2"

renameDir="$searchDir"
renameFile="$dbOutClean"

# testArgs1=`cat "$renameFile" | wc -l`
# if [ "$testArgs1" -lt 2 ];
# then
# cd "$renameDir"
# renameFile="$2";
# fi;



cd "$renameDir"



#### If xls file do xls2csv if CSV cat and format for renaming
testArgs1=`echo "$dbOutClean" | awk -F"." '{ print $NF }'`
if [ "$testArgs1" = "xls" ];
then
xls2csv "$renameFile" | awk -F";" '{ print $1".jpg",$2".jpg"}' | sed 's/\"//g' | grep -v vendor_style_no >> "$renameFile"_new
else
cat "$renameFile" | awk -F, '{ print $1".jpg",$2".jpg"}' | sed 's/\"//g' | grep -v vendor_style_no > "$renameFile"_new

fi;



###Rename files from dboutput
while read line; 
do 
oldname=`echo "$line" | awk '{ print $1 }'`; 
newname=`echo "$line" | awk '{ print $2 }'`; 

mv $oldname $newname;

done <"$renameFile"_new



#####################--------------->
##
### Add back the _1.jpg to the RenameFile Only so the next we can rename the csv and the files for Alts
#rm "$renameFile"_new
#cat "$renameFile" | awk -F, '{ print $1"_1.jpg",$2"_1.jpg"}' | sed 's/\"//g' | grep -v vendor_style_no > "$renameFile"_new
cat "$renameFile" | awk -F, '{ print $1".jpg",$2".jpg"}' | sed 's/\"//g' | grep -v vendor_style_no > "$renameFile"_new

#find "$renameFile"_new -type f -maxdepth 0 -exec sed -i -e 's/.jpg/_1.jpg/g'
####
#### Now Do All the Alts 1 and a time Renaming the RenameFile incrementally as you go. Sure I could serialize with seq 1 5
####
##########
for num in `seq 2 7 | xargs`; 
do 
ext=`echo _"$num".jpg`;

find "$renameFile"_new -type f -maxdepth 0 -exec sed -i -e s/_[1-6].jpg/$ext/g {} \;
#
#
#
while read line; 
do 
oldname=`echo "$line" | awk '{ print $1 }'`; 
newname=`echo "$line" | awk '{ print $2 }'`; 

mv $oldname $newname;

done <"$renameFile"_new


done;
