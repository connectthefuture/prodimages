#!/bin/bash
. ~/.bash_profile

fileInput=$LIMBO/newTmp.txt
#$1
sourceDir=$1
DAYR=`date "+%Y-%m-%d-RetouchToDo"`
DAYR_DIR=/mnt/Post_Ready/Daily/"$DAYR"
sourceDir="$DAYR_DIR"
TODAY=$(date +"%m-%d-%Y")
formatFile=$LIBSRV/exifFormatFilePrdStatsCsv_ex.txt
#headersExif=`cat $formatFile | grep -v "#"`
rm ~/dailySummary.txt
metaKey=`$SCRIPTS/bash/key_exiftoolPM.sh $formatFile`

find $sourceDir -type f -iname \*_1.jpg | xargs -L1 exiftool -d %d-%b-%Y -m -f -r -p ${FormatFile} | sort | uniq > $fileInput

##### Sums Count "c"(styleNumuniq) of each "a"record($4=Brand), totalSum of records for "b"

for col in `echo $metaKey | awk '{ print NF }' | xargs seq 2`
do
header=`echo $metaKey | xargs -n1 | cat | grep -E $col`

awk -v name="$header" -v field="$col" -F"," '{a[$field]++;b[$3]++;c[$1]++}END{for (i in a) print i,a[i],c[i],b[i]}' $fileInput | sort -d > $LIMBO/totals_$header.txt
#>> ~/dailySummary.txt

#>> ~/fileOuttt.txt
done;
exit;


