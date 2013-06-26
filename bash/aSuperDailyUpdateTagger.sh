#!/bin/bash

. ~/.bash_profile
. ~/.bashrc

DATE=`date "+%Y-%m-%d"`
DAY=`date "+%Y-%m-%d-RetouchToDo"`

#####______GET FILE String LIST from Arg $1
inDir="$1"
outFileStringPairs=$LIMBO/csvIOutUpdateStrings.csv
$SCRIPTS/outputStringsIOargs.sh $inDir $outFileStringPairs

## RUN SQL Query spooling Meta Tags to CSV
newUpdateMetaTagSQL=$SQLSCRIPTS/update_daily_zImagesTags.sql

dbOutRaw=$LIMBO/spoolDWDailyUpdateTags.csv
dbOutClean=$LIMBO/UpdateExifPreQuery.csv

###<----Make dbOutRaw
$DSSPRDLOGIN @$newUpdateMetaTagSQL;


###<----
cat $dbOutRaw | sed s/'  '//g | sed s/'--'//g | sed s/' ,'/','/g | sed s/'Spec'/'SpecialInstructions'/1 | sed s/'Samp'/'SampleStatusDate'/1 | sort -k1 -t"," -du > $dbOutClean

###<----exiftoolReadyCsv=~/Dropbox/exiftoolReadyCsv1.csv
exiftoolPathsCsv=$LIMBO/compiledUpdateMTagsFrAwk.csv

#####------>AWK to read strings and Match with PM metaData
styleNumPaths=`cat $outFileStringPairs | awk -v OFS="," '{ print $1, $2 }'`
exifHeaders=$PRODSRV/lib/exifUpdateHeaders.csv
exifReadHeaded=$LIMBO/exifUpdateReadWithHead.csv

rm $exiftoolPathsCsv
for styleNum in `echo $styleNumPaths | xargs -n1`
do
style=`echo $styleNum | awk -F"," '{ print $1 }'`
styPath=`echo $styleNum | awk -F"," '{ print $2 }'`
cat $dbOutClean | awk -v OFS="," -F"," -v awKPath="$styPath" -v awKStyle="$style" '$1 ~ awKStyle { print awKPath, $2, $3, $4, $5, $6, $7, $8, $9 }' >> $exiftoolPathsCsv
done;

### NOW THE STRINGS have REPLACED the Style Nums --- Ready to batch concat to get Single ExifTool Executable lines

cat $exifHeaders $exiftoolPathsCsv > $exifReadHeaded;
##----->Exec exiftool ##----> '-xmp:artist<${IPTC:Keywords}'
cat $outFileStringPairs | awk '{ print $2 }' | sort -t, -bdri -k 3.2b,3.2br -k 3.5b,3.5br | uniq | awk -F, '{ print "exiftool -m -f -P -d %Y-%m-%d -overwrite_original_in_place -fast2 -csv='"$exifReadHeaded"' "$1 }' | /bin/bash
exit;
