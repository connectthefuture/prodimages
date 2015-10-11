#!/bin/bash

. ~/.bash_profile




mysqldump -u root -pmysql -T/var/tmp www_django --fields-terminated-by=, --fields-enclosed-by=\"


mongoimport -d www_django --headerline -c zimages -type csv -f fields-sep-by-coma --drop /var/tmp/zimages1_photoselects.txt

mongoimport -d www_django --headerline -c pushselects -type csv -f fields-sep-by-coma --drop /var/tmp/push_photoselects.txt

mongoimport -d www_django --headerline -c archselects -type csv -f field]s-sep-by-coma --drop /var/tmp/post_ready_original.txt
mongoimport -d www_django --headerline -c outtakes -type csv -f field]s-sep-by-coma --drop /var/tmp/production_raw_zimages.txt
mongoimport -d www_django --headerline -c pmdata -type csv -f field]s-sep-by-coma --drop /var/tmp/product_snapshot_live.txt
