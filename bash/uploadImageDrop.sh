#!/bin/bash
. ~/.bash_profile

Today=`date +%Y-%m-%d`
batchDoneDate=`date +%Y%b%d`

ftpLoginFull="ftp://file3.bluefly.corp/ImageDrop -u imagedrop:imagedrop0"
uploadComplete="/mnt/Post_Complete/Complete_Archive/Uploaded"
upload_arch="$uploadComplete"/"$batchDoneDate"/
mkdir -p "$upload_arch"

################----------Test if 1 arg supplied, If no args run of CurrentDir
# testArgs1=`ls "$1" | wc -l`
# if [ "$testArgs1" -lt 1 ];
# then
# search="$1";
# else
search="$1"
#fi;

########
for f in `find $search -type f -iname \*.*g`
do

curl -k -T "$f" "$ftpLoginFull"

#echo $uploadResult
sleep .5
########--------Test if Arg #2 supplied
# testArgs2=`ls "$2" | wc -l`
#
# if [ "$testArgs2" -lt 1 ];
# then
# uploadComplete="$2"
mv -f "$f" "$upload_arch";
echo "$Today" "$f" "$upload_arch"  >> ./"$batchDoneDate"_uploadLog.txt
#fi;

done;
