#!/bin/bash
. ~/.bash_profile

fileInput=$LIMBO/newTmp.txt
#$1
#sourceDir=$1
#$1
DAYR=`date "+%Y-%m-%d-RetouchToDo"`
DAYR_DIR=/mnt/Post_Ready/Daily/"$DAYR"
sourceDir="$DAYR_DIR"
TODAY=$(date +"%m-%d-%Y")
FormatFile=$PRODSRV/lib/exifFormatFilePrdStatsCsv_ex.txt
#headersExif=`cat $FormatFile | grep -v "#"`
rm $LIMBO/dailySummary.txt
metaKey=`$SCRIPTS/key_exiftoolPM.sh $PRODSRV/lib/exifFormatFilePrdStatsCsv_ex.txt`

find $sourceDir -type f -iname \*_1.jpg | xargs -L1 exiftool -d %d-%b-%Y -m -f -r -p ${FormatFile} | sort | uniq > $fileInput

##### Sums Count "c"(styleNumuniq) of each "a"record($4=Brand), totalSum of records for "b"

for col in `echo $metaKey | awk '{ print NF }' | xargs seq 1`
do
header=`echo $metaKey | xargs -n1 | cat | grep -E $col`

awk -v name="$header" -v field="$col" -F"," '{a[$field]++;b[$3]++;c[$1]++}END{for (i in a) print i,a[i],b[i],c[i]}' $fileInput | sort -d | sed s/"'"//g > $LIMBO/totals_$header.txt

done;

cat $LIMBO/totals_1,Style_Number.txt | grep -E ^[2-9,{9}] | wc -l | awk '{ print "Total Styles "$0}' > $LIMBO/Style_Number.txt
sleep 10
####Pull Title of each Report from Last Piece of FilesName
filesAll="$LIMBO/Style_Number.txt $LIMBO/totals_2,Photo_Date.txt $LIMBO/totals_3,Product_Category.txt $LIMBO/totals_4,Brand_Name.txt $LIMBO/totals_5,Event_Group.txt $LIMBO/totals_6,Sample_Status.txt $LIMBO/totals_7,Production_Status.txt $LIMBO/totals_8,Start_Date.txt $LIMBO/totals_9,Sample_Status_Date.txt"

####Replace Junk
fileAttach=$LIMBO/compiledReport.csv
fileHTML=$LIMBO/compiledReport.html
cat $filesAll | grep -v "^-" | awk -v ORS=";" '{ print $0 }' | sed 's/2\ 2\ 1/\-----Photo_Date-----/1' | sed 's/2\ 2\ 1/\-----Product_Type-----/1' | sed 's/2\ 2\ 1/\-----Brand-----/1' | sed 's/2\ 2\ 1/\-----Event_ID-----/1' | sed 's/2\ 2\ 1/\-----Sample_Status-----/1' | sed 's/2\ 2\ 1/\-----Production_Status-----/1' | sed 's/2\ 2\ 1/\-----Copy_Ready_DT-----/1' | sed 's/2\ 2\ 1/\-----Sample_Status_DT-----/1' | awk -v RS=";" '{ print $1,$2,$3,$4,$5,$6 }' > $fileAttach

#styleCount=`find /mnt/Post_Ready/Daily/$DAY -type f | awk -F'/' '{ print $NF }' | awk -F'_' '{ print $1 }' | sort | uniq | wc -l`

fileCount=`find /mnt/Post_Ready/Daily/$DAYR -type f | awk -F'/' '{ print $NF }' | sort | wc -l`
myMailAddress="jbragato@bluefly.com john.bragato@gmail.com"
allMailAddress='<jbragato@bluefly.com> <james.hoetker@bluefly.com> <conrad.sanderson@bluefly.com> <stephen.parker@bluefly.com> <jennifer.folks@bluefly.com>'
stylesTotal=`cat $fileAttach | head -1`

mail -s "$stylesTotal Total Files $fileCount" "$allMailAddress" < "$fileAttach"
##awk -F="\n" 'BEGIN{print "<table>"} {print "<tr>";for(i=1;i<=NF;i++)print "<td>" $i"</td>";print "</tr>"} END{print "</table>"}' $fileAttach > $fileHTML ;
##mutt -i "fileHTML" -s "$stylesTotal Total Files $fileCount" -- "$allMailAddress"

exit;


