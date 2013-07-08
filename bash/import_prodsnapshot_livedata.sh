#!/bin/bash

. ~/.bash_profile
. ~/.bashrc

DATE=`date "+%Y-%m-%d"`
DAY=`date "+%Y-%m-%d-RetouchToDo"`

## RUN SQL Query spooling Queryt to CSV

#dailyPhpMyAdminForImport=/mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/phpImportTOrelation_PM_SchemasTables_sqlInsert/DailyImportTophpMyAdmin_SQL.sql
dailyPhpMyAdminForImport=$SCRIPTS/sql/prodsnapshot_import_livedata.sql

dbOutRaw=$PRODSRV/tmp/limbo/spoolpmaimportprodsnapshotlive.csv
dbOutClean=$PRODSRV/data/csv/product_snapshot_live.csv

###<----Make dbOutRaw
$DSSPRDLOGIN @$dailyPhpMyAdminForImport;

##headersPma=$LIBSRV/headers_productsnpimport.csv

###<----Fix the syntax errors migrating from oracle to mysql
cat $dbOutRaw | sed 's/^ *//g' |sed s/'  '//g | sed s/'--'//g | sed s/' ,'/','/g | sed s/', '/','/g | sort -k1.1,1.9 -t"," -nu | grep -e "," | sed s/'status_dt'/'status_dt'/1 | sed s/'copy_read,'/'copy_ready_dt'/1 | sed s/'image_rea,'/'image_ready_dt'/1 | sed s/'start_dt'/'start_dt'/1 | sed s/'orig_star,'/'orig_start_dt'/1 | sed s/'productio,'/'production_complete_dt,'/1 | sed s/'sample_im,'/'sample_image_dt'/1 | sed 's/05-/2005-/g' | sed 's/06-/2006-/g' | sed 's/07-/2007-/g' | sed 's/08-/2008-/g' | sed 's/09-/2009-/g' | sed 's/10-/2010-/g' | sed 's/11-/2011-/g' | sed 's/12-/2012-/g' | sed 's/13-/2013-/g' | sed 's/14-/2014-/g' | sed 's/15-/2015-/g' | sed 's/16-/2016-/g' | sed 's/17-/2017-/g' | sed 's/18-/2018-/g' | sed 's/19-/2019-/g' | sed 's/20-/2020-/g' | sed 's/21-/2021-/g' | sed 's/22-/2022-/g' | sed 's/23-/2023-/g' | sed 's/24-/2024-/g' | sed 's/25-/2025-/g' | sed 's/-JAN-/-01-/g' | sed 's/-FEB-/-02-/g' | sed 's/-MAR-/-03-/g' | sed 's/-APR-/-04-/g' | sed 's/-MAY-/-05-/g' | sed 's/-JUN-/-06-/g' | sed 's/-JUL-/-07-/g' | sed 's/-AUG-/-08-/g' | sed 's/-SEP-/-09-/g' | sed 's/-OCT-/-10-/g' | sed 's/-NOV-/-11-/g' | sed 's/-DEC-/-12-/g' | sed 's/^ *//g' > $dbOutClean

cols="colorstyle,brand,production_status,po_number,sample_status,status_dt,copy_ready_dt,image_ready_dt,production_complete_dt,start_dt,orig_start_dt,gender,category,product_type,sample_image_dt,vendor_style,color,product_subtype,sample_id,sku,track_number,track_dt,sample_location,track_user,po_type"
#cols=`cat $LIBSRV/headers_productsnpimport.csv`

##source ~/.bash_profile && sudo port load mysql55-server && sudo mysql5 --socket=/Applications/MAMP/tmp/mysql/mysql.sock --password=mysql --database=imageMetaData < $dbOutClean ;
sleep 2
###<--------Import to Localhost MySQL db dailyImports
#importMysql=mysqlimport

#colNames=`head -1 $dbOutClean | xargs -L1`
colNames=`echo -e $cols`

mysqlimport --host=127.0.0.1 --port=3301 --user=root --password=mysql --fields-terminated-by="," --default-character-set=utf8 --fields-enclosed-by="'" --fields-escaped-by="\"" --delete --replace --ignore-lines=1 --columns="$cols" --local data_imports "$dbOutClean"

mysqlimport --host=127.0.0.1 --port=3301 --user=root --password=mysql --fields-terminated-by="," --default-character-set=utf8 --fields-enclosed-by="'" --fields-escaped-by="\"" --delete --replace --ignore-lines=1 --columns="$cols" --local data_imagepaths "$dbOutClean"

exit;

