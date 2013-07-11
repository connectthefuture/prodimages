#!/bin/bash

. ~/.bash_profile

styleStringTest=$DATASRV/csv/StyleStringTest.csv
styleStringImport=$DATASRV/csv/push_photoselects.csv
styleStringImportZ=$DATASRV/csv/zimages1_photoselects.csv

cp $styleStringTest $styleStringImport;


mysqlimport --host=127.0.0.1 --port=3301 --user=root --password=mysql --fields-terminated-by="\ " --default-character-set=utf8 --fields-enclosed-by="\'" --fields-escaped-by="\"" --delete --replace --ignore-lines=0 --columns="colorstyle,photo_date,file_path,alt" --local data_imagepaths "$styleStringImport" ;

mysqlimport --host=127.0.0.1 --port=3301 --user=root --password=mysql --fields-terminated-by="\ " --default-character-set=utf8 --fields-enclosed-by="\'" --fields-escaped-by="\"" --delete --replace --ignore-lines=0 --columns="colorstyle,photo_date,file_path,alt" --local data_imagepaths "$styleStringImportZ" ;
