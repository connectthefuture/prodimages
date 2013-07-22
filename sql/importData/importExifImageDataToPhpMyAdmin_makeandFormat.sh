#!/bin/bash
. ~/.bash_profile
#inputDir=$1
exifFormatFile=$LIBSRV/exifFormatFileSQL_INSERT_ex.txt
importRead=$SCRIPTS/sql/import_exifInfoImagePost_Ready.sql
inputDir=$1
tmpFile=$LIMBO/outExiftoolSQL.txt

rm $tmpFile
touch $tmpFile
for f in `find $inputDir -type f -iname \*.jpg`
do
exiftool -m -f -P -p $exifFormatFile $f >> $tmpFile
done ;

sed '/^$/d' $tmpFile | sed 's/\ [0-9]-00-00//g' | sed 's/\ 0000-00-00//g' > $importRead;
#/usr/local/batchRunScripts/mysql5_connectRunEXimport.sh
#run_exifData_mysql5
#source ~/.bash_profile && sudo port load mysql55-server && sudo mysql5 --socket=/Applications/MAMP/tmp/mysql/mysql.sock --password=mysql --database=imageMetaData < $importRead

#rm $tmpFile
exit;
