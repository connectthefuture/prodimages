#!/bin/bash

. ~/.bash_profile
. ~/.bashrc

DATE=`date "+%Y-%m-%d"`
DAY=`date "+%Y-%m-%d-RetouchToDo"`

## RUN SQL Query spooling Queryt to CSV

dailyPhpMyAdminForImport=$SCRIPTS/sql/DailyImportTophpMyAdmin_SQL.sql

dbOutRaw=$LIMBO/spoolphpmyAdminClean.csv
dbOutClean=$DATASRV/csv/phpmyAdminCleanToImport.csv

###<----Make dbOutRaw
$DSSPRDLOGIN @$dailyPhpMyAdminForImport;


###<----
cat $dbOutRaw | sed 's/^ *//g' | sed s/'  '//g | sed s/'--'//g | sed s/' ,'/','/g | sed s/'Sample_Da'/'Sample_Date'/1 | sed s/'Copy_Read'/'Copy_Ready_Date'/1 | sort -k1.1,1.9 -t"," -dur | grep -e "," | sed 's/^ *//g' > $dbOutClean

##source ~/.bash_profile && sudo port load mysql55-server && sudo mysql5 --socket=/Applications/MAMP/tmp/mysql/mysql.sock --password=mysql --database=imageMetaData < $dbOutClean ;
sleep 10
###<--------Import to Localhost MySQL db dailyImports

mysqlimport5 --host=127.0.0.1 --port=3306 --user=root --password=mysql --fields-terminated-by="," --delete --replace --ignore-lines=1 --columns=COLORSTYLE,BRAND,EVENT_GROUP_NAME,COPY_READY,LEVEL4_NAME,PRODUCTION_STATUS,EVENT_GROUP_ID,SAMPLE_STATUS,SAMPLE_STATUS_DATE --local data_imports "$dbOutClean"

exit;
