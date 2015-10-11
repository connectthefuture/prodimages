#!/bin/bash

. ~/.bash_profile

DATE=`date "+%Y-%m-%d"`
DAY=`date "+%Y-%m-%d-RetouchToDo"`

## RUN SQL Query spooling Queryt to CSV

dailyPhpMyAdminForImport=$SCRIPTS/sql/event_style_status_live.sql

dbOutRaw=$PRODSRV/tmp/limbo/spooleventstylestatus.csv
dbOutClean=$PRODSRV/data/csv/events_style_status.csv

###<----Make dbOutRaw
$BFYPRDLOGIN @$dailyPhpMyAdminForImport;

###<----Fix the syntax errors migrating from oracle to mysql
cat $dbOutRaw | sed 's/^ *//g' | sed 's/--//g' | sed s/'  '//g | sed 's/productio__/production_complete_dt__/1' | sed 's/copy_read/copy_ready_dt/1' | sed -E 's/ __/__/g' | sort -k1.1,1.9 -dur | grep -e "__" | sed 's/05-/2005-/g' | sed 's/06-/2006-/g' | sed 's/07-/2007-/g' | sed 's/08-/2008-/g' | sed 's/09-/2009-/g' | sed 's/10-/2010-/g' | sed 's/11-/2011-/g' | sed 's/12-/2012-/g' | sed 's/13-/2013-/g' | sed 's/14-/2014-/g' | sed 's/15-/2015-/g' | sed 's/16-/2016-/g' | sed 's/17-/2017-/g' | sed 's/18-/2018-/g' | sed 's/19-/2019-/g' | sed 's/20-/2020-/g' | sed 's/21-/2021-/g' | sed 's/22-/2022-/g' | sed 's/23-/2023-/g' | sed 's/24-/2024-/g' | sed 's/25-/2025-/g' | sed 's/-JAN-/-01-/g' | sed 's/-FEB-/-02-/g' | sed 's/-MAR-/-03-/g' | sed 's/-APR-/-04-/g' | sed 's/-MAY-/-05-/g' | sed 's/-JUN-/-06-/g' | sed 's/-JUL-/-07-/g' | sed 's/-AUG-/-08-/g' | sed 's/-SEP-/-09-/g' | sed 's/-OCT-/-10-/g' | sed 's/-NOV-/-11-/g' | sed 's/-DEC-/-12-/g' | grep -e [A-Za-z] | grep -v "____-__-__" | sed -E 's/\ __\ |__\ |\ __/__/g' > $dbOutClean;

colNames=`head -1 $dbOutClean | xargs -L1 | sed 's/__/,/g'`
#cols=`cat $LIBSRV/headers_productsnpimport.csv`
##source ~/.bash_profile && sudo port load mysql55-server && sudo mysql5 --socket=/Applications/MAMP/tmp/mysql/mysql.sock --password=mysql --database=imageMetaData < $dbOutClean ;
sleep 3
###<--------Import to Localhost MySQL db dailyImports


mysqlimport --host=127.0.0.1 --port=3301 --user=root --password=mysql --fields-terminated-by="__" --default-character-set=utf8 --fields-enclosed-by="'" --fields-escaped-by="\"" --delete --replace --ignore-lines=1 --columns=""$colNames"" --local data_imports "$dbOutClean"

exit;
