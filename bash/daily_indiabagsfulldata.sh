#!/bin/bash

. ~/.bash_profile
. ~/.bashrc

DATE=`date "+%Y-%m-%d"`
DAY=`date "+%Y-%m-%d-RetouchToDo"`

#####______GET FILE String LIST from Arg $1
inDir="$1"
outFileStringPairs=$LIMBO/csvIOutStrings_IndiaBags.csv
outputStringsIOargs.sh $inDir $outFileStringPairs

## RUN SQL Query spooling New Styles For Sending to India Daily
indiaBagSQL=$SCRIPTS/sql/sql_silhouette_bags_india.sql

dbOutRaw=$LIMBO/spool_IndiaBags.csv
dbOutClean=$LIMBO/PushedIndiaBagsPre.csv

###<----Make dbOutRaw
$DSSPRDLOGIN @$indiaBagSQL;


###<----Format SQL output for Processing with AWK --csv format
cat $dbOutRaw | sed s/'  '//g | sed s/'--'//g > $dbOutClean
#| sed s/' |'/'|'/g | sort -k1 -t"|" -du
compiled_IndiaPathsForBatch=$DATASRV/csv/compiled_IndiaBags_FrAwk.csv

#####------>AWK to read strings and Match with PM metaData
filePaths_IndiaPaths=`cat $outFileStringPairs | awk -v OFS="," '{ print $1, $2 }'`


rm $compiled_IndiaPathsForBatch
for styleNum in `echo $filePaths_IndiaPaths | xargs -n1`
do
style=`echo $styleNum | awk -F"|" '{ print $1 }'`
styPath=`echo $styleNum | awk -F"|" '{ print $2 }'`
cat $dbOutClean | awk -v OFS="," -F"|" -v awKPath="$styPath" -v awKStyle="$style" '$1 ~ awKStyle { print awKPath, $2, $3, $4, $5, $6, $7, $8, $9 }' >> $compiled_IndiaPathsForBatch
done;

### NOW THE STRINGS have REPLACED the Style Nums --- Ready to batch concat to get Single ExifTool Executable lines
##----->Exec exiftool ##----> '-xmp:artist<${IPTC:Keywords}'
#cat $outFileStringPairs | awk '{ print $2 }' | grep -v _MAC | sort -t, -bdri -k 3.2b,3.2br -k 3.5b,3.5br | uniq | awk -F, '{ print "exiftool -m -f -P -overwrite_original -fast2 -csv='"$exifReadHeaded"' "$1 }' | /bin/bash
exit;
