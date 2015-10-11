#!/bin/bash
. ~/.bash_profile
. ~/.bashrc

DATE=`date "+%Y-%m-%d"`
DAY=`date "+%Y-%m-%d-RetouchToDo"`
#loggerX=`date >> ~/Dropbox/logger.txt`
#echo $loggerX
postReadySummary=$DATASRV/sql/post_ready_summary.csv
## RUN SQL Query spooling ProdSnapshot to CSV
dailySnapshot=$SCRIPTS/sql/outputRawAllPrdSnp.sql
dbOutRaw=$LIMBO/outputRawAllPrdSnpSpool.csv
dbOutClean=$LIMBO/outputSnapshotForImport.csv

###<----Make dbOutRaw RUN SQL
$DSSPRDLOGIN @$dailySnapshot;

cat $dbOutRaw | sed s/'  '//g | sed s/'--'//g | sed s/' ,'/','/g | sed s/'Spec'/'SpecialInstructions'/1 | sed s/'Simi'/'SimilarityIndex'/1 | sort -k1 -t"," -du > $dbOutClean ;

sleep 10
###<--------Import to Localhost MySQL db dailyImports
sleep 5
mysqlimport --host=127.0.0.1 --port=3306 --user=root --password=mysql --fields-terminated-by=" " --delete --replace --columns=COLORSTYLE,Photo_Date,SourceFile --local dailyImports "$dbOutClean"


exit;

