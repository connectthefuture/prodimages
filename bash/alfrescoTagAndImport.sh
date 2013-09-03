#!/bin/bash
. ~/.bash_profile
. ~/.bashrc

DATE=`date "+%Y-%m-%d"`
DAY=`date "+%Y-%m-%d-RetouchToDo"`
loggerX=`date >> ~/Dropbox/logger.txt`
echo $loggerX
#####------------>GET FILE String LIST from Arg $1
inDir="$1"
outFileStringPairs=$LIMBO/csvIOutStrings.csv
outputStringsIOargs.sh $inDir $outFileStringPairs

## RUN SQL Query spooling Meta Tags to CSV
newMetaTagSQL=$SCRIPTS/sql/ssShorterNewerExifSQL.sql

dbOutRaw=$LIMBO/spoolexiftoolCsvMetaData.csv
dbOutClean=$LIMBO/PushedexifPreQuery.csv

###<----Make dbOutRaw
$DSSPRDLOGIN @$newMetaTagSQL;


###<----
cat $dbOutRaw | sed s/'  '//g | sed s/'--'//g | sed s/' ,'/','/g | sed s/'Spec'/'SpecialInstructions'/1 | sed s/'Simi'/'SimilarityIndex'/1 | sort -k1.1,1.9 -t"," -du > $dbOutClean

###<----exiftoolReadyCsv=~/Dropbox/exiftoolReadyCsv1.csv
exiftoolPathsCsv=$LIMBO/compiledMTagsFrAwk.csv

#####------>AWK to read strings and Match with PM metaData
styleNumPaths=`cat $outFileStringPairs | awk -v OFS="," '{ print $1, $2 }'`

rm $exiftoolPathsCsv
for styleNum in `echo $styleNumPaths | xargs -n1`
do
style=`echo $styleNum | awk -F"," '{ print $1 }'`
styPath=`echo $styleNum | awk -F"," '{ print $2 }'`
cat $dbOutClean | awk -v OFS="," -F"," -v awKPath="$styPath" -v awKStyle="$style" '$1 ~ awKStyle { print awKPath, $2, $3, $4, $5, $6, $7, $8, $9 }' >> $exiftoolPathsCsv
done;

### NOW THE STRINGS have REPLACED the Style Nums --- Ready to batch concat to get Single ExifTool Executable lines
exifHeaders=$LIBSRV/exifHeaders.csv
exifReadHeaded=$LIMBO/exifReadWithHead.csv
cat $exifHeaders $exiftoolPathsCsv > $exifReadHeaded;
##----->Exec exiftool ##----> '-xmp:artist<${IPTC:Keywords}'
cat $outFileStringPairs | awk '{ print $2 }' | grep -v _MAC | sort -t, -bdri -k 3.2b,3.2br -k 3.5b,3.5br | uniq | awk -F, '{ print "exiftool -m -f -P -d %Y-%m-%d -overwrite_original -fast2 -csv='"$exifReadHeaded"' "$1 }' | /bin/bash


############<-----------------------Move Tagged Files To Alfresco Share
#alfrescoImportDir=/mnt/Post_Ready/zAlfresco_Primary/tmp_Alfresco_Batch_Import_Drop/
#alfrescoImportComplete=$LIMBO/tmp_Alfresco_Batch_Import_Complete/
#execImportStrings=`cat $outFileStringPairs | awk '{ print $2 }' | grep -v _MAC | awk -v alfDir="$alfrescoImportDir" -F"/" '{ print "cp "$0" "alfDir"/"$NF }'`
#importedPath=`echo $execImportStrings | xargs -n3 | awk '{ print $3 }'`

#------>execute Move to Import & Execute BulkImport
#sleepCount=`echo $execImportStrings | xargs -n3 | wc -l`
#echo $execImportStrings | xargs -n3 | /bin/bash
#echo $loggerX
#sleep $sleepCount
#sleep $sleepCount
#echo $loggerX

#echo $sleepCount
#echo $ALFRESCOBULKIMPORT | /bin/bash
#sleep $sleepCount
#sleep $sleepCount

echo $loggerX
###--->Move to Alfresco complete
#echo $importedPath | xargs -n1 | awk -v alfComplete="$alfrescoImportComplete" -F"/" '{ print "mv "$0" "alfComplete$NF }' | /bin/bash
#echo $loggerX

exit;
