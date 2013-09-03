#!/bin/bash

. ~/.bash_profile





renameDir="$1"
renameFile="$2"


cd "$renameDir"

xls2csv "$renameFile" | awk -F";" '{ print $1".jpg",$2".jpg"}' | sed 's/\"//g' | grep -v Vendor > "$renameFile"_new

renamXls=`xls2csv "$renameFile" | awk -F";" '{ print $1".jpg",$2".jpg"}' | sed 's/\"//g' | grep -v Vendor | sort | xargs -n2 > "$renameFile"_newer`

##echo $renamXls | xargs -n2


while read line; 
do 
oldname=`echo "$line" | awk '{ print $1 }'`; 
newname=`echo "$line" | awk '{ print $2 }'`; 
mv $oldname $newname; 
done <"$renameFile"_new


exit;
