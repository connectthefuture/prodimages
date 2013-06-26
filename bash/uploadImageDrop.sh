#!/bin/bash
. ~/.bash_profile

Today=`date +%Y-%m-%d`
batchDoneDate=`date +%Y%b%d`

ftpLoginFull="ftp://file3.bluefly.corp/ImageDrop/ --user imagedrop:imagedrop0"


################----------Test if 1 arg supplied, If no args run of CurrentDir
testArgs1=`ls "$1" | wc -l`
if [ "$testArgs1" -lt 1 ];
then
search="$1";
else
search=".";
fi;

########
for f in `find $search -type f -iname \*.*g`
do
uploadResult=`curl -k -T $f $ftpLoginFull`

########--------Test if Arg #2 supplied
testArgs2=`ls "$2" | wc -l`

if [ "$testArgs2" -lt 1 ]; 
then
uploadComplete="$2"
mv -f "$f" "$uploadComplete";
echo '"$Today" "$f" "$uploadResult"  >> ./"$batchDoneDate"_uploadLog.txt
fi;

done;
