#!/bin/bash
. ~/.bash_profile

searchDir="$1"
#searchDir=/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/rugs
echo "$#"

##Format the WHERE to use iterated directory Search
cd $searchDir;

dirPoName=`pwd | awk -F"/" '{ print $NF }'`
# if [ "$dirPoName" -eq "$dirPoName" >& /dev/null ];
# then
# echo "$dirPoName"
# exit;
# fi;


find $searchDir -iname \*.jpg | sort | uniq | xargs -L1 exiftool -r -p $LIBSRV/exifFormatFile_sqlIterateVend.txt > $LIMBO/sqlIterateFoundVend.csv;

##Complete Composing of SELECT Statement infront of generated WHEREs
### Checks for only 1 Arg, which should mean po number is dirname
## Check Whether Directory is PO number, if so use PO in Query, else just use vendor style numbers from filenames

if [ "$#" -ne "1" ];
then

echo 'SELECT DISTINCT POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_STYLE_NO as "vendor_style_no", POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE as "colorstyle", POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR AS "ponumber" FROM POMGR_SNP.PRODUCT_SNAPSHOT WHERE (' > $LIMBO/sqlIteratetmpVend.csv && cat $LIMBO/sqlIterateFoundVend.csv | sed 's/_1//g' >> $LIMBO/sqlIteratetmpVend.csv && echo '( POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE = '"'999999999'"' ) ) ORDER by POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_STYLE_NO DESC, POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR DESC ;' >> $LIMBO/sqlIteratetmpVend.csv;

#### Include PO number in Query qith more than 1 Arg, ie arg1=dirname" arg2=notset"
else
echo 'SELECT DISTINCT POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_STYLE_NO as "vendor_style_no", POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE as "colorstyle", POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR AS "ponumber" FROM POMGR_SNP.PRODUCT_SNAPSHOT WHERE POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR = '$dirPoName' AND (' > $LIMBO/sqlIteratetmpVend.csv && cat $LIMBO/sqlIterateFoundVend.csv | sed 's/_1//g' >> $LIMBO/sqlIteratetmpVend.csv && echo '( POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE = '"'999999999'"' ) ) ORDER by POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_STYLE_NO DESC, POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR DESC ;' >> $LIMBO/sqlIteratetmpVend.csv;
fi;

##Bring in Spool settings to complete SQL file to run through SQLplus
cat $LIBSRV/settingsSqlSpool.csv $LIMBO/sqlIteratetmpVend.csv > $LIMBO/sqlIterateSelectVend.csv;
echo 'spool off' >> $LIMBO/sqlIterateSelectVend.csv;
echo 'exit;' >> $LIMBO/sqlIterateSelectVend.csv;


dbOutRaw=$LIMBO/iterateSpool.csv
dbOutClean="$searchDir"/../sqlIterateCompleteVend_"$dirPoName".csv

###<----Make dbOutRaw
$DSSPRDLOGIN @$LIMBO/sqlIterateSelectVend.csv;


###<----Fix the syntax errors migrating from oracle to mysql
cat $dbOutRaw | sed s/'  '//g | sed s/'--'//g | sed s/' ,'/','/g | grep -e "," | sed s/', '/','/g | sort -k1.1,1.10 -t"," -dur | sed 's/^ *//g' > $dbOutClean;







########RENAMING
renameDir="$searchDir"
renameFile="$dbOutClean"

# testArgs1=`cat "$renameFile" | wc -l`
# if [ "$testArgs1" -lt 2 ];
# then
# cd "$renameDir"
# renameFile="$2";
# fi;



cd "$renameDir"



#### If xls file do xls2csv if CSV cat and format for renaming
testArgs1=`echo "$dbOutClean" | awk -F"." '{ print $NF }'`
if [ "$testArgs1" = "xls" ];
then
xls2csv "$renameFile" | awk -F";" '{ print $1".jpg",$21".jpg"}' | sed 's/\"//g' | grep -v vendor >> "$renameFile"_new
else
cat "$renameFile" | awk -F, '{ print $1".jpg",$2".jpg"}' | sed 's/\"//g' | grep -v vendor >> "$renameFile"_new

fi;



###Rename files from dboutput
while read line; 
do 
oldname=`echo "$line" | awk '{ print $1 }'`; 
newname=`echo "$line" | awk '{ print $2 }'`; 
mv $oldname $newname; 
done <"$renameFile"_new


exit;











exit;


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
