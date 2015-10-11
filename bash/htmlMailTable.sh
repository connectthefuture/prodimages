#!/bin/bash
. ~/.bash_profile

fileInput=$LIMBO/newTmp.txt
fileInputAll=$LIMBO/newTmpAll.txt
#sourceDir=$1
DAY=`date "+%d-%b-%Y"`
sourceDir=/mnt/Post_Ready/*Push/1126*2/
TODAY=$(date +"%m-%d-%Y")
FormatFile=$PRODSRV/lib/exifFormatFilePhotoStatsCsv_ex.txt
#headersExif=`cat $FormatFile | grep -v "#"`
#rm $LIMBO/dailySummary.txt
metaKey=`$SCRIPTS/bash/key_exiftoolPhotoStats.sh $FormatFile`

####_1 Files only-Style Count
find $sourceDir -type f -iname \*_1.jpg | xargs -L1 exiftool -d %d-%b-%Y -m -f -r -p ${FormatFile} | sort | uniq > $fileInput
####_All Files- Shot Count
find $sourceDir -type f -iname \*_[1-6].jpg | xargs -L1 exiftool -d %d-%b-%Y -m -f -r -p ${FormatFile} | sort | uniq > $fileInputAll

##### Sums STYLE Count "c"(styleNumuniq) of each "a"record($4=Brand), totalSum of records for "b"

for col in `echo $metaKey | awk '{ print NF }' | xargs seq 1`
do
header=`echo $metaKey | xargs -n1 | cat | grep -E $col`

awk -v name="$header" -v field="$col" -F"," '{a[$field]++;b[$3]++;c[$1]++}END{for (i in a) print i,a[i],b[i],c[i]}' $fileInput | sort -d | sed s/"'"//g > $LIMBO/totalsPhotoStyles_$header.txt

done;

##<------------>### SHOT Count "c"(styleNumAll) of each "a"record($4=Brand), totalSum of records for "b"
for col in `echo $metaKey | awk '{ print NF }' | xargs seq 1`
do
header=`echo $metaKey | xargs -n1 | cat | grep -E $col`

awk -v name="$header" -v field="$col" -F"," '{a[$field]++;b[$3]++;c[$1]++}END{for (i in a) print i,a[i],b[i],c[i]}' $fileInputAll | sort -d | sed s/"'"//g > $LIMBO/totalsPhotoShots_$header.txt

done;

cat $LIMBO/totalsPhotoStyles_1,Style_Number.txt | grep -E ^[2-9,{9}] | wc -l | awk '{ print "Total_Styles "$0}' > $LIMBO/PhotoStyle_Number.txt
sleep 1
cat $LIMBO/totalsPhotoShots_1,Style_Number.txt | grep -E ^[2-9,{9}] | wc -l | awk '{ print "Total_Shots "$0}' > $LIMBO/PhotoShot_Number.txt
sleep 1
####Pull Title of each Report from Last Piece of FilesName
filesAll=''$LIMBO'/PhotoStyle_Number.txt '$LIMBO'/totalsPhotoStyles_2,Photo_Date.txt '$LIMBO'/totalsPhotoStyles_3,Product_Category.txt' 
filesAllShots=''$LIMBO'/PhotoShot_Number.txt '$LIMBO'/totalsPhotoShots_2,Photo_Date.txt '$LIMBO'/totalsPhotoShots_3,Product_Category.txt'

#$LIMBO/totalsPhotoStyles_4,Brand_Name.txt $LIMBO/totalsPhotoStyles_5,Event_Group.txt $LIMBO/totalsPhotoStyles_6,Sample_Status.txt $LIMBO/totalsPhotoStyles_7,Production_Status.txt $LIMBO/totalsPhotoStyles_8,Start_Date.txt $LIMBO/totalsPhotoStyles_9,Sample_Status_Date.txt'
#fileCount=`find /mnt/Post_Ready/Daily/$DAYR -type f | awk -F'/' '{ print $NF }' | sort | wc -l`
#styleCount=`cat  | awk -F'/' '{ print $NF }' | sort | wc -l`

fileAttach=$LIMBO/compiledPhotoReport
fileHTML=$LIMBO/compiledPhotoReport.html
htmlHeaders=/mnt/Post_Ready/zProd_Server/imageServer7/mail/forms/headershtmltable.txt
outbox=$PRODSRV/'mail'/outbox
cat $filesAll | grep -v "^-" | awk -v ORS=";" '{ print $0 }' | sed 's/2\ 2\ 1/\---\<b\>Photo_Date\<\/b\>---/1' | sed 's/2\ 2\ 1/\---\<b\>Product_Type\<\/b\>---/1' | sed 's/\ \&\ /_\&_/g' | sed 's/\ shirts/_shirts/g' | sed 's/\ goods/_goods/g' | awk -v RS=";" '{ print $1,$2 }' > ''$fileAttach'_styles.csv'


cat $filesAllShots | grep -v "^-" | awk -v ORS=";" '{ print $0 }' | sed 's/2\ 2\ 1/\---\<b\>Photo_Date\<\/b\>---/1' | sed 's/2\ 2\ 1/\---\<b\>Product_Type\<\/b\>---/1' | awk -v RS=";" '{ print $1,$2,$3,$4,$5,$6 }' > ''$fileAttach'_shots.csv'

cat ''$fileAttach'_shots.csv' | awk '{ print $NF }' > ''$fileAttach'_shotcount.csv'
rm ''$fileAttach'_shots.csv'

paste ''$fileAttach'_styles.csv' ''$fileAttach'_shotcount.csv' | sed 's/---\<b\>Product_Type\<\/b\>---/---\<b\>Styles\<\/b\>---,---\<b\>Shots\<\/b\>---/2' | sed 's/---\<b\>Photo_Date\<\/b\>---/---\<b\>Styles\<\/b\>---,---\<b\>Shots\<\/b\>---/2' | sed 's/-----/--/g' > ''$fileAttach'_combined.csv'
##-------->Make HTML version of Report----------->

htmlTagged=`awkHTMLTableFr1Input.sh ''$fileAttach'_combined.csv'`
##echo "${htmlTagged// / }" | awk '{for (i=1;i<=NF;i++){printf "%s%s",sep,$i;sep=","} print"" }' | sed 's/,\</\</g' | xargs -L1 | awk -F="," '{print "<td>";for(i=1;i<=NF;i++)print $i"</td>";print ""}' > $fileHTML
echo "${htmlTagged// / }" | awk '{for (i=1;i<=NF;i++){printf "%s%s",sep,$i;sep=","} print"" }' | sed 's/,\</\</g' > $fileHTML;

cat $htmlHeaders $fileHTML > $outbox/compiledPhotoReport.html;
echo '</body></html>' >> $outbox/compiledPhotoReport.html;
##mail -s "$stylesTotal Total Files $fileCount" "$myMailAddress" < "$fileAttach"
##awk -F="\n" 'BEGIN{print "<table>"} {print "<tr>";for(i=1;i<=NF;i++)print "<td>" $i"</td>";print "</tr>"} END{print "</table>"}' $fileAttach > $fileHTML ;
##mutt -i "fileHTML" -s "$stylesTotal Total Files $fileCount" -- "$allMailAddress"

##cd /Applications/STACK_8802-3301/php/bin;
php -f $PRODSRV/mail/scripts/mailMimePearEdit.php

#/Applications/STACK_8802-3301/php/bin/php -a
exit;


