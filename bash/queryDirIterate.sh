#!/bin/bash
. ~/.bash_profile

searchDir="$1"

##Format the WHERE to use iterated directory Search
find $searchDir -iname \*_1.\* | sort | uniq | xargs -L1 exiftool -r -p $LIBSRV/exifFormatFile_sqlIterate.txt > $LIMBO/sqlIterateFound.csv;

##Complete Composing of SELECT Statement infront of generated WHEREs
echo 'SELECT POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE as "colorstyle", POMGR_SNP.PRODUCT_SNAPSHOT.BRAND as "brand", POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME as "product_type", to_date(POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE, '"'YYYY-MM-DD'"') as "sample_dt", POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS as "sample_status", SUM(POMGR_SNP.PRODUCT_SNAPSHOT.AVAILABLE_ON_HAND) as "qty_avail" FROM POMGR_SNP.PRODUCT_SNAPSHOT WHERE (' > $LIMBO/sqlIteratetmp.csv && cat $LIMBO/sqlIterateFound.csv | sed 's/_1//g' >> $LIMBO/sqlIteratetmp.csv && echo '( POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE = '"'999999999'"' ) ) GROUP BY POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE, POMGR_SNP.PRODUCT_SNAPSHOT.BRAND, POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME, to_date(POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE, '"'YYYY-MM-DD'"'), POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS ORDER by SUM(POMGR_SNP.PRODUCT_SNAPSHOT.AVAILABLE_ON_HAND) DESC, POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE DESC;' >> $LIMBO/sqlIteratetmp.csv;

##Bring in Spool settings to complete SQL file to run through SQLplus
cat $LIBSRV/settingsSqlSpool.csv $LIMBO/sqlIteratetmp.csv > $LIMBO/sqlIterateSelect.csv;
echo 'spool off' >> $LIMBO/sqlIterateSelect.csv;
echo 'exit;' >> $LIMBO/sqlIterateSelect.csv;


dbOutRaw=$LIMBO/iterateSpool.csv
dbOutClean=$pmaImport/sqlIterateComplete.csv

###<----Make dbOutRaw
$DSSPRDLOGIN @$LIMBO/sqlIterateSelect.csv;


###<----Fix the syntax errors migrating from oracle to mysql
cat $dbOutRaw | sed s/'  '//g | sed s/'--'//g | sed s/' ,'/','/g | grep -e "," | sed s/', '/','/g | sed 's/05-/2005-/g' | sed 's/06-/2006-/g' | sed 's/07-/2007-/g' | sed 's/08-/2008-/g' | sed 's/09-/2009-/g' | sed 's/10-/2010-/g' | sed 's/11-/2011-/g' | sed 's/12-/2012-/g' | sed 's/13-/2013-/g' | sed 's/14-/2014-/g' | sed 's/15-/2015-/g' | sed 's/16-/2016-/g' | sed 's/17-/2017-/g' | sed 's/18-/2018-/g' | sed 's/19-/2019-/g' | sed 's/20-/2020-/g' | sed 's/21-/2021-/g' | sed 's/22-/2022-/g' | sed 's/23-/2023-/g' | sed 's/24-/2024-/g' | sed 's/25-/2025-/g' | sed 's/-JAN-/-01-/g' | sed 's/-FEB-/-02-/g' | sed 's/-MAR-/-03-/g' | sed 's/-APR-/-04-/g' | sed 's/-MAY-/-05-/g' | sed 's/-JUN-/-06-/g' | sed 's/-JUL-/-07-/g' | sed 's/-AUG-/-08-/g' | sed 's/-SEP-/-09-/g' | sed 's/-OCT-/-10-/g' | sed 's/-NOV-/-11-/g' | sed 's/-DEC-/-12-/g' | sort -k1.1,1.10 -t"," -dur | sed 's/^ *//g' > $dbOutClean;
exit;


#awkHTMLTableFr1Input.sh $dbOutClean > $dbOutClean_html


# searchDir="$1"
# foundPaths=`find $searchDir -iname \*_1.\* | sort | uniq`
# ##Format the WHERE to use iterated directory Search
# echo $foundPaths | xargs -L1 exiftool -r -p $LIBSRV/exifFormatFile_sqlIterate.txt > $LIMBO/sqlIterateFound.csv;
# 
# headers=`head -1 $dbOutClean`
# ##stylesOnly=`cat $dbOutClean | awk -F, '{ print $1 }' | xargs -n1`
# 
# for stylePath in $foundPaths
# do
# styleOnly=`echo $stylePath | xargs basename | sed -e 's/_1.jpg//g'`
# cat $dbOutClean | awk -v OFS="," -F"," -v awKPath="$stylePath" -v awKStyle="$styleOnly" '$1 ~ awKStyle { print $1, $2, $3, $4, $5, $6 }' >> $dbOutClean_withinv;
# done;
