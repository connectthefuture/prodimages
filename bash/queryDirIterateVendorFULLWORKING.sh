#!/bin/bash
. ~/.bash_profile

searchDir="$1"
#searchDir=/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/rugs
echo "$#"


#ls -1 | awk -v ORS=, 'gsub(".jpg", "");gsub(".JPG", "");{ print $0 }'

## First get Raw list of file names
cd $searchDir;
tmpRawFile=../tmpRawFile.csv
touch $tmpRawFile
tmpRawPath=`dirname $tmpRawFile`
ls -1 | awk -v ORS=, '{ print $0 }' > $tmpRawPath/tmpRawFile.csv
find $tmpRawPath -type f -iname \*tmp\*.csv -maxdepth 1 -exec sed -i -e 's/.jpg//g' {} \;
find $tmpRawPath -type f -iname \*tmp\*.csv -maxdepth 1 -exec sed -i -e 's/.JPG//g' {} \;

##1Aly---> Strip the _1.jpg replace just the .jpg from the file and make all of the ext LOWERCASE

replaceIn1For2With3.sh $searchDir ".JPG" ".jpg"
replaceIn1For2With3.sh $searchDir "_1.jpg" ".jpg"


### Secondly replace all Spaces for Files Names with Double Underscore to wrap for Exiftool
replaceSpaceDblUScore.sh $searchDir
#replaceSpace.sh $searchDir

## Thirdly Remove other Bad Chars
for f in `find $searchDir -type f -iname \*.\*g`
do
cd $d ;
echo "$f"
 	FILENAME="${f//[\?%\+\:\&\#\(\)]/_}";
 	mv -f "$f" "$FILENAME"
done;

cd $searchDir;
dirPoName=`pwd | awk -F"/" '{ print $NF }'`
# if [ "$dirPoName" -eq "$dirPoName" >& /dev/null ];
# then
# echo "$dirPoName"
# exit;
# fi;

##Format the WHERE to use iterated directory Search
find $searchDir -iname \*.jpg | sort | uniq | xargs -L1 exiftool -r -p $LIBSRV/exifFormatFile_sqlIterateVend.txt > $LIMBO/sqlIterateFoundVend.csv;

##Complete Composing of SELECT Statement infront of generated WHEREs
### Checks for only 1 Arg, which should mean po number is dirname
## Check Whether Directory is PO number, if so use PO in Query, else just use vendor style numbers from filenames

if [ "$#" -le "1" ];
then

echo 'SELECT DISTINCT POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE as "vendor_style_no", POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID as "colorstyle", POMGR_SNP.PO_LINE.PO_HDR_ID AS "ponumber" FROM POMGR_SNP.PRODUCT_COLOR INNER JOIN POMGR_SNP.PO_LINE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID WHERE (' > $LIMBO/sqlIteratetmpVend.csv && cat $LIMBO/sqlIterateFoundVend.csv | sed 's/_1//g' >> $LIMBO/sqlIteratetmpVend.csv && echo '( POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID = '"'999999999'"' ) ) ORDER by POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE DESC, POMGR_SNP.PO_LINE.PO_HDR_ID DESC ;' >> $LIMBO/sqlIteratetmpVend.csv;

#### Include PO number in Query qith more than 1 Arg, ie arg1=dirname" arg2=notset"
else
echo 'SELECT DISTINCT POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE as "vendor_style_no", POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID as "colorstyle", POMGR_SNP.PO_LINE.PO_HDR_ID AS "ponumber" FROM POMGR_SNP.PRODUCT_COLOR INNER JOIN POMGR_SNP.PO_LINE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR_SNP.PO_LINE.PO_HDR_ID = '$dirPoName' AND (' > $LIMBO/sqlIteratetmpVend.csv && cat $LIMBO/sqlIterateFoundVend.csv | sed 's/_1//g' >> $LIMBO/sqlIteratetmpVend.csv && echo '( POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID = '"'999999999'"' ) ) ORDER by POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE DESC, POMGR_SNP.PO_LINE.PO_HDR_ID DESC ;' >> $LIMBO/sqlIteratetmpVend.csv;
fi;

##Bring in Spool settings to complete SQL file to run through SQLplus
cat $LIBSRV/settingsSqlSpool.csv $LIMBO/sqlIteratetmpVend.csv > $LIMBO/sqlIterateSelectVend.csv;
echo 'spool off' >> $LIMBO/sqlIterateSelectVend.csv;
echo 'exit;' >> $LIMBO/sqlIterateSelectVend.csv;

## Unwrap Exiftool Double Underscore for SQL Query
find $LIMBO -type f -iname \*sqlIterateSelectVend.csv -maxdepth 1 -exec sed -i -e 's/__/\ /g' {} \;

## replaceIn1For2With3.sh $LIMBO/sqlIterateSelectVend.csv "_2" \"\"

dbOutRaw=$LIMBO/iterateSpool.csv
dbOutClean="$searchDir"/../sqlIterateCompleteVend_"$dirPoName".csv

###<----Make dbOutRaw
$DSSPRDLOGIN @$LIMBO/sqlIterateSelectVend.csv;


###<----Fix the syntax errors migrating from oracle to mysql
cat $dbOutRaw | sed s/'  '//g | sed s/'--'//g | sed s/' ,'/','/g | grep -e "," | sed s/', '/','/g | sort -dur | sed 's/^ *//g' | grep -e [1-9] > $dbOutClean;







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
xls2csv "$renameFile" | awk -F";" '{ print $1".jpg",$2".jpg"}' | sed 's/\"//g' | grep -v vendor_style_no >> "$renameFile"_new
else
cat "$renameFile" | awk -F, '{ print $1".jpg",$2".jpg"}' | sed 's/\"//g' | grep -v vendor_style_no >> "$renameFile"_new

fi;



###Rename files from dboutput
while read line; 
do 
oldname=`echo "$line" | awk '{ print $1 }'`; 
newname=`echo "$line" | awk '{ print $2 }'`; 

mv $oldname $newname;

done <"$renameFile"_new



#####################--------------->
##
### Add back the _1.jpg to the RenameFile Only so the next we can rename the csv and the files for Alts
#rm "$renameFile"_new
cat "$renameFile" | awk -F, '{ print $1"_1.jpg",$2"_1.jpg"}' | sed 's/\"//g' | grep -v vendor_style_no > "$renameFile"_new

#find "$renameFile"_new -type f -maxdepth 0 -exec sed -i -e 's/.jpg/_1.jpg/g'
####
#### Now Do All the Alts 1 and a time Renaming the RenameFile incrementally as you go. Sure I could serialize with seq 1 5
####
##########
for num in `seq 2 6 | xargs`; 
do 
ext=`echo _"$num".jpg`;

find "$renameFile"_new -type f -maxdepth 0 -exec sed -i -e s/_[1-6].jpg/$ext/g {} \;
#
#
#
while read line; 
do 
oldname=`echo "$line" | awk '{ print $1 }'`; 
newname=`echo "$line" | awk '{ print $2 }'`; 

mv $oldname $newname;

done <"$renameFile"_new


done;

##################### DONE#########DONE## dun

# find "$renameFile"_new -type f -maxdepth 0 -exec sed -i -e 's/.jpg/_2.jpg/g' {} \;
# 
# 
# 
# 
# 
# 
# 
# find "$renameFile"_new -type f -maxdepth 0 -exec sed -i -e 's/_2.jpg/_3.jpg/g' {} \;
# 
# 
# 
# 
# 
# 
# 
# 
# find "$renameFile"_new -type f -maxdepth 0 -exec sed -i -e 's/_3.jpg/_4.jpg/g' {} \;
# 
# 
# 
# 
# 
# find "$renameFile"_new -type f -maxdepth 0 -exec sed -i -e 's/_4.jpg/_5.jpg/g' {} \;
# 







cd "$renameDir"
ls -la;
echo $tmpRawPath/tmpRawFile.csv
#rm $tmpRawPath/tmpRawFile.csv
#rm $tmpRawPath/tmpRawFile.csv-e
#rm "$dbOutClean"_new
 
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
