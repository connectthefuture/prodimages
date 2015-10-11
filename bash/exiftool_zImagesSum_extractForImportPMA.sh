#!/bin/bash

. ~/.bash_profile

for f in `find $ZIMAGES/[2-9][0-9][0-9][0-9]/ -type f -iname \*.\*g | grep -v xxFer`; 
do 
exiftool -d %Y-%m-%d -fast2 -csv -f -q -r -m -p $LIBSRV/exifFormatFileImsrv7.txt $f | sed 's/\/Volumes\/Post_Ready\/zImages_1/\/zImages/g' | sed 's/\#\[TAIL\]//g' | sed 's/SourceFile//g' | sed 's/\?//g' | sed 's/--//g' | grep ',' >> $LIMBO/zimages_exif99_raw.csv; 
done;

cat $LIMBO/zimages_exif99_raw.csv | sort -k1 -t"," -dur | sed 's/\/Volumes\/Post_Ready\/zImages_1/\/zImages/g' | sed 's/\#\[TAIL\]//g' | sed 's/SourceFile//g' | sed 's/\?//g' | sed s/'PRODUCTIO,'/'Production_Complete_Dt,'/1 | sed 's/05-/2005-/g' | sed 's/06-/2006-/g' | sed 's/07-/2007-/g' | sed 's/08-/2008-/g' | sed 's/09-/2009-/g' | sed 's/10-/2010-/g' | sed 's/11-/2011-/g' | sed 's/12-/2012-/g' | sed 's/13-/2013-/g' | sed 's/14-/2014-/g' | sed 's/15-/2015-/g' | sed 's/16-/2016-/g' | sed 's/17-/2017-/g' | sed 's/18-/2018-/g' | sed 's/19-/2019-/g' | sed 's/20-/2020-/g' | sed 's/21-/2021-/g' | sed 's/22-/2022-/g' | sed 's/23-/2023-/g' | sed 's/24-/2024-/g' | sed 's/25-/2025-/g' | sed 's/-JAN-/-01-/g' | sed 's/-FEB-/-02-/g' | sed 's/-MAR-/-03-/g' | sed 's/-APR-/-04-/g' | sed 's/-MAY-/-05-/g' | sed 's/-JUN-/-06-/g' | sed 's/-JUL-/-07-/g' | sed 's/-AUG-/-08-/g' | sed 's/-SEP-/-09-/g' | sed 's/-OCT-/-10-/g' | sed 's/-NOV-/-11-/g' | sed 's/-DEC-/-12-/g' | sed 's/--//g' | sed -e 's/\([1-2][0-9][0-9][0-9]\):\([0-1][1-9]\):\([0-3][1-9]\)/\1-\2-\3/g' | sed 's/'\"'//g' | grep zImages > $pmaImport/zimages_exif99.csv;


#colNames=`head -1 $pmaImport/zimages_exif99.csv | xargs -L1 | sed 's/\///g'`
colNames=`head -1 /mnt/Post_Ready/zProd_Server/imageServer7/lib/headers_exif99.csv`

mysqlimport --host=127.0.0.1 --port=3301 --user=root --password=mysql --fields-enclosed-by="\'" --fields-terminated-by="," --fields-escaped-by="\"" --delete --replace --ignore-lines=0 --columns=""`$colNames`"" --local data_imagepaths "$pmaImport"/zimages_exif99.csv;

sleep 5

##/mnt/Post_Ready/zProd_Server/imageServer7/scripts/default/styleStringZimagesPro.sh;

exit;
