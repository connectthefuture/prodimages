#!/bin/bash


. ~/.bash_profile

vendorDrop=$PRODSRV/var/consignment
completeDir=$vendorDrop/_complete
textFileDir=$vendorDrop/_textFiles
zipArch=$PRODSRV/tmp/_consignZipArch
tmp=$vendorDrop/_tmp
#### Extract Zip Files in Comsignmnt Folder To start all as Dirs & begin script Purpose to rename from Database query style/vendor

zipFiles=`find $vendorDrop -type f -iname \*.zip`

for z in "$zipFiles" ;
do
cd "$vendorDrop" ;
extractDir=`basename $z | sed 's/.zip//g'`;
mkdir "$extractDir";
cd "$extractDir"
unzip -o -qq $z ;
#mv $z $zipArch ;
done;
######

###Move zip Files to store on tmp dir
find "$vendorDrop" -type f -iname \*.zip -exec mv -f {} $zipArch \;
allDirs=`find "$vendorDrop" -type d -maxdepth 1 -iname \*\[0-9]\*`
echo $allDirs ;
###### End Unzip Process
#########################

####################################################################################################
#######----get All Files into Top level Dir Of unZipped Folder(PONumber)
for d in $allDirs ;
do
cd "$vendorDrop" ;
cd $d ;
###---------------------------Delete all left over files from zip extract And remove superfluous sub folders
rm -R __MACOSX ;
find . -iname ._\*.* -exec rm {} \;
#########################
find $d -type f -iname \*.\*g -exec mv -f {} $d \;
find $d -type d -maxdepth 1 -mindepth 1 -exec rm -R {} \;
######################<-------------------
done;

allDirs2=`find "$vendorDrop" -type d -maxdepth 1 -iname \*\[0-9]\*`
##################REMOVE SPACES FROM ALL FILENAMES FIRST
for d in "$allDirs2"
do
cd "$d" ;

ls -1 | while read file; do new_file="$(echo "$file" | sed 's/\ //g')"; mv "$file" "$new_file"; done ;
sleep .4;
#renamebadcharDir.sh $d ;

done;
##########################################################

#allFiles=`find $d -type f -iname \*.\*g`
#cd $d;
#ls -1 | while read file; do new_file=$(echo $file | sed 's/\ //g'); mv "$file" "$new_file"; done;

####################
#####UP OK
############################ REMOVE BAD CHARACTERS
###allDirs21=`find "$vendorDrop" -type d -maxdepth 1 -iname \*\[0-9]\* | xargs -L1`

#for d in `find "$vendorDrop" -type d -maxdepth 1 -iname \*\[0-9]\* | xargs -L1`
#do
#cd $vendorDrop ;
#find "$d" -type f -iname \*.\*g | sed s/\ /'\\ '/g | xargs exiftool -'Directory' -csv | awk '{ split($1, a, "//"); print $0" "a[3] }' | awk '{ split($1, a, ","); print "exiftool -f -overwrite_original -P -fast2 -m -'IPTC:PONumber'="$NF" "a[1] }' | /bin/bash ;
#done ;
######################


###allDirs22=`find "$vendorDrop" -type d -maxdepth 1 -iname \*\[0-9]\* | xargs -L1`
# for d in `find "$vendorDrop" -type d -maxdepth 1 -iname \*\[0-9]\* | xargs -L1` ;
# do
# cd "$vendorDrop" ;
# #allFiles=`find $d -type f -iname \*.\*g`
# cd "$d" ;
# #ls -1 | while read file; do new_file=$(echo $file | sed 's/\ //g'); mv "$file" "$new_file";
# for file in `find "$d" -type f -iname \*.\*g`
# do
# cleanFile="${file//[\?%\+]/_}";
#     mv -f "$file" "$cleanFile"
#     echo "$cleanFile";
# done;
# done;


###allDirs23=`find "$vendorDrop" -type d -maxdepth 1 -iname \*\[0-9]\* | xargs -L1`
##### For loop of Dir in last cmd For Replace bad Chars in files
# for d in `find "$vendorDrop" -type d -maxdepth 1 -iname \*\[0-9]\* | xargs -L1` ;
# do
# for f in `find "$d" -type f -iname \*.\*g`
# do
# cd $vendorDrop ;
#     echo "$f"
#  	FILENAME="${f//[\?%\+\:\&\#\(\)]/_}";
#  	mv -f "$f" "$FILENAME"
# done;
# done;

##----

##allDirs24=`find "$vendorDrop" -type d -maxdepth 1 -iname \*\[0-9]\* | xargs -L1`

##### Strip File of everything except First block of vchars/digits(aka vendor style num) make csv ponum,vendornum
for d in `find "$vendorDrop" -type d -maxdepth 1 -iname \*\[0-9]\* | xargs -L1` ;
do
for filename in `find "$d" -type f -iname \*.\*g`
do
directory=`dirname "$filename"`
extension=`basename "$filename" | awk -F"." '{ print $NF }'`
fname=`basename "$filename" | awk -F".\?\?g" '{ print $1 }'`
dname=`dirname "$filename" | awk -F"/" '{ print $NF }'`
finalfname=`echo "$fname" | awk -F"." '{ print $1 }'` 

    echo -e "$dname","$finalfname" >> $textFileDir/"$dname".csv ;
    mv "$filename" "$directory"/"$finalfname"."$extension"
    done;

    for filename in `find "$d" -type f -iname \*.\*g`
        do
        directory=`dirname "$filename"`
        echo -e "$directory","$filename" | sort | uniq | grep -E [0-9A-Za-z] >> $tmp/"$dname"_paths.csv ;
        done;
done;
##################################__CSV_NOW_READY_FOR_QUERY__############################ALL CORRECT ABOVE


####### -------------->>>>>>    Query DB for Style Numbers   <<<<<<<--------------------

dbOutRaw=$LIMBO/iterateSpool.csv
dbOutClean=$pmaImport/sqlConsigRenameComplete.csv

#rm $dbOutRaw ;
#touch $dbOutClean ;
#touch $dbOutRaw ;
textFiles=`find "$textFileDir" -iname \*.csv`
rm $dbOutClean ;
for textff in $textFiles
do
textf=`echo textff | sed 's/\.csv//g'`
##echo $line ;
lines=`cat "$textf".csv_done.csv | xargs -L1` ;

for line in $lines
    do
    recCount=`echo $line | awk -F"," '{ print NF }'`
    ponumsql=`echo $line | awk -F"," '{ print $1 }'`
    vendornumsql=`echo $line | awk -F"," '{ print $2 }'`
    
##if [ "$(eval "echo \${$recCount[*]}")" != '2' ] ;
        ##echo $recCount
       

##    else ;
    
    sqlQuery='SELECT DISTINCT POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_STYLE_NO AS "vendor_style", POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE AS "colorstyle", POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR AS "ponumber" FROM POMGR_SNP.PRODUCT_SNAPSHOT WHERE POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR = '"'$ponumsql'"' AND POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_STYLE_NO = '"'$vendornumsql'"' ;'
    
    echo -e "$sqlQuery" > $LIMBO/sqlIteratetmp.csv ;
    
    ##Bring in Spool settings to complete SQL file to run through SQLplus
    cat $LIBSRV/settingsSqlSpool.csv $LIMBO/sqlIteratetmp.csv > $LIMBO/sqlIterateSelect.csv;
    echo 'spool off' >> $LIMBO/sqlIterateSelect.csv;
    echo 'exit;' >> $LIMBO/sqlIterateSelect.csv;
    
    dbOutRaw=$LIMBO/iterateSpool.csv
    dbOutClean=$pmaImport/sqlConsigRenameComplete.csv
    ###<----Make dbOutRaw
    $DSSPRDLOGIN @$LIMBO/sqlIterateSelect.csv;
    
    ###<----Fix the syntax errors migrating from oracle to mysql
    cat "$dbOutRaw" | sed s/'  '//g | sed s/'--'//g | sed s/' ,'/','/g | grep -e "," | sed s/', '/','/g >> "$dbOutClean" ;
    
    
##fi ;
    done;
        
        cat "$dbOutClean" | sort -t, -k2.1,2.9 -dr | uniq | grep -E [0-9A-Za-z] > "$textf".csv_done.csv ;
        
done;



####### -------------->>>>>>    END Query DB CSV READY FOR RENAMING  <<<<<<<--------------------
##dir=/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/116309
##ponum=`echo $dir | awk -F"\/" '{ print $NF }'`


filedirs=`find $vendorDrop -type d -maxdepth 1 -iname \*\[0-9]\* | xargs -L1`
for dir in $filedirs
do

allFiles=`find $dir -type f -iname \*.jpg`
#echo $allFiles;
for f in "'"$allFiles"'" ;
do
##dir=/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/116309 ;
cd $dir ;
ponum=`echo $dir | awk -F"\/" '{ print $NF }'` ;
textfiledone="$textFileDir"/116309_done.csv
textfilepaths="$tmp"/"$ponum"_paths.csv
vendbase=`basename $f | sed "s/\'//g"`
vendornum=`echo $vendbase | awk -F"." '{ print $1 }'` ;
currentName=`echo "'"$f"'"` ;

cat $textfiledone | awk -v finaldir="$completeDir" -v vendbase="$vendbase" -v current="$currentName" -v vendornum="$vendornum" '$1 ~ vendbase { print "cp "current" "finaldir"/"$2,".jpg" }' >> "$tmp"/done.csv
##cat $textfiledone
done;
done;


#cat $textf | awk -v vendornum="$vendornum" '$1 ~ searchStyle' >> $dailyDownloadFile



# newName=`echo $f | sed 's/\\\\ /_/g' | sed 's/\:/_/g' | sed 's/\-/_/g' | sed 's/\&//g' | sed 's/\+//g' | sed 's/\\\\(//g' | sed 's/\\\\)//g' | sed 's/\//\\\\\\//g' | sed 's/\!//g' | sed 's/\#//g' | sed 's/\*//g' | sed 's/\@//g' | sed 's/\?//g' | sed 's/\%//g' | sed 's/\^//g' | sed 's/\=//g' | sed 's/\;//g' | sed 's/\[//g' | sed 's/\]//g' | sed 's/\"//g' | sed 's/\|//g' | sed 's/\\\\{//g' | sed 's/\\\\}//g' | sed "s/\'//g"` ;
# newName=`echo $f | sed 's/\\\\ /_/g'` ;
# echo $oldName;
# ##awk -v old="$oldName" -v new="$newName" -FS"\n" '{ print "mv "old" "new }' | echo ;
# done;

##-v OFS="," -F","

################### GET PO NUMBER FROM DIR NAME & VENDOR NUMBER FROM FIRST DELIMITER "_" in fileName
# cd $vendorDrop;
# 
# poNums=`find $vendorDrop -type d --exec basename {} \;| awk -F"." '{ print $1 }'`
# 
# echo $poNums/$zipFiles;
# 
# 
# dirsByPo=`find "$vendorDrop" -type d -maxdepth 1 -iname \*\[0-9]\*`
# for d in $dirsByPo
# do
# cd $d
# ##for filename in `find "$d" -type f -iname \*.\*g`
# 
# for f in `find "$d" -type f -iname \*.\*g`
# do
# ponum=`dirname "$f" | awk -F"/" '{ print $NF }'`
# vendornum=`basename "$f" | awk -F".\?\?g" '{ print $1 }'`
# textf=`ls "$textFileDir" | grep '$ponum'`
# 
# cat $textf | awk -v vendornum="$vendornum" '$1 ~ searchStyle' >> $dailyDownloadFile
# done;
# ##find . -type f -iname \*.\*g | sed 's/\ //g'
# cat $textFileDir/$fname | awk '{ print "mv "$1".jpg "$2".jpg" }' | xargs -L1 | /bin/bash
# done;
# done;
# 
# 
# 
# 
# 
# 
# 
# 
# ######################## 
# 
# for dir in `cd $vendorDrop && ls`; 
# do
# cd $vendorDrop;
# cd $dir ; 
# po=`echo $dir | sed 's/\ //g' | sed 's/\:/_/g' | sed 's/\-/_/g' | awk -F\/ '{ print $NF }'` ; 
# origNames=`find . -type f -iname \*.\*g` ; 
# echo $dir ;
# echo $po ;
# echo $origNames ;
# 
# for f in $origNames; 
# do 
# echo $f ;
# 
# echo $f, >> ${textFileDir}/${dir}_Renameing.txt ; 
# echo $f | sed 's/\ //g' | sed 's/\:/_/g' | sed 's/\-/_/g' | sed 's/\//_/g' | awk -F"_" '{ print $1"," }' >> ${textFileDir}/${dir}_Renameing.txt ; 
# done; 
# echo NEXT ;
# done;
# 
# 
# 
# ########### File Name Format Cleaner - End
# ### Begin Query and Style Rename
# 
# sqlQuery='SELECT DISTINCT POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_STYLE_NO AS "vendor_style", POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE AS "colorstyle", POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR AS "ponumber" FROM POMGR_SNP.PRODUCT_SNAPSHOT WHERE POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR = '115796';'
# 
# 
# 
# 
# ##Format the WHERE to use iterated directory Search
# find $searchDir -iname \*_1.\* | sort | uniq | xargs -L1 exiftool -r -p $LIBSRV/exifFormatFile_sqlIterateStyleVendPO.txt > $LIMBO/sqlIterateFoundStyleVendPO.csv;
# 
# ##Complete Composing of SELECT Statement infront of generated WHEREs
# echo 'SELECT DISTINCT POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_STYLE_NO AS "vendor_style", POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE AS "colorstyle", POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR AS "ponumber" FROM POMGR_SNP.PRODUCT_SNAPSHOT WHERE (' > $LIMBO/sqlIteratetmp.csv && cat $LIMBO/sqlIterateFound.csv | sed 's/_1//g' >> $LIMBO/sqlIteratetmp.csv && echo '( POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE = '"'999999999'"' ) ) GROUP BY POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE, POMGR_SNP.PRODUCT_SNAPSHOT.BRAND, POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME, to_date(POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE, '"'YYYY-MM-DD'"'), POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS ORDER by SUM(POMGR_SNP.PRODUCT_SNAPSHOT.AVAILABLE_ON_HAND) DESC, POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE DESC;' >> $LIMBO/sqlIteratetmp.csv;
# 
# ##Bring in Spool settings to complete SQL file to run through SQLplus
# cat $LIBSRV/settingsSqlSpool.csv $LIMBO/sqlIteratetmp.csv > $LIMBO/sqlIterateSelect.csv;
# echo 'spool off' >> $LIMBO/sqlIterateSelect.csv;
# echo 'exit;' >> $LIMBO/sqlIterateSelect.csv;
# 
# 
# dbOutRaw=$LIMBO/iterateSpool.csv
# dbOutClean=$pmaImport/sqlIterateComplete.csv
# 
# ###<----Make dbOutRaw
# $DSSPRDLOGIN @$LIMBO/sqlIterateSelect.csv;
# 
# 
# ###<----Fix the syntax errors migrating from oracle to mysql
# cat $dbOutRaw | sed s/'  '//g | sed s/'--'//g | sed s/' ,'/','/g | grep -e "," | sed s/', '/','/g | sed 's/05-/2005-/g' | sed 's/06-/2006-/g' | sed 's/07-/2007-/g' | sed 's/08-/2008-/g' | sed 's/09-/2009-/g' | sed 's/10-/2010-/g' | sed 's/11-/2011-/g' | sed 's/12-/2012-/g' | sed 's/13-/2013-/g' | sed 's/14-/2014-/g' | sed 's/15-/2015-/g' | sed 's/16-/2016-/g' | sed 's/17-/2017-/g' | sed 's/18-/2018-/g' | sed 's/19-/2019-/g' | sed 's/20-/2020-/g' | sed 's/21-/2021-/g' | sed 's/22-/2022-/g' | sed 's/23-/2023-/g' | sed 's/24-/2024-/g' | sed 's/25-/2025-/g' | sed 's/-JAN-/-01-/g' | sed 's/-FEB-/-02-/g' | sed 's/-MAR-/-03-/g' | sed 's/-APR-/-04-/g' | sed 's/-MAY-/-05-/g' | sed 's/-JUN-/-06-/g' | sed 's/-JUL-/-07-/g' | sed 's/-AUG-/-08-/g' | sed 's/-SEP-/-09-/g' | sed 's/-OCT-/-10-/g' | sed 's/-NOV-/-11-/g' | sed 's/-DEC-/-12-/g' | sort -k1.1,1.10 -t"," -dur > $dbOutClean;
# exit;
# 
# 
# #awkHTMLTableFr1Input.sh $dbOutClean > $dbOutClean_html
# 
# 
# # searchDir="$1"
# # foundPaths=`find $searchDir -iname \*_1.\* | sort | uniq`
# # ##Format the WHERE to use iterated directory Search
# # echo $foundPaths | xargs -L1 exiftool -r -p $LIBSRV/exifFormatFile_sqlIterate.txt > $LIMBO/sqlIterateFound.csv;
# # 
# # headers=`head -1 $dbOutClean`
# # ##stylesOnly=`cat $dbOutClean | awk -F, '{ print $1 }' | xargs -n1`
# # 
# # for stylePath in $foundPaths
# # do
# # styleOnly=`echo $stylePath | xargs basename | sed -e 's/_1.jpg//g'`
# # cat $dbOutClean | awk -v OFS="," -F"," -v awKPath="$stylePath" -v awKStyle="$styleOnly" '$1 ~ awKStyle { print $1, $2, $3, $4, $5, $6 }' >> $dbOutClean_withinv;
# # done;
