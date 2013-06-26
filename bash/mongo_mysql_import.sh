#!/bin/bash

. ~/.bash_profile




mysqldump -u root -pmysql -T/var/tmp data_imagepaths --fields-terminated-by=, --fields-enclosed-by=\"




mongoimport -d data_imagepaths --headerline -c zimages -type csv -f fields-sep-by-coma --drop /var/tmp/zimages1_photoselects.txt

mongoimport -d data_imagepaths --headerline -c pushselects -type csv -f fields-sep-by-coma --drop /var/tmp/push_photoselects.txt

mongoimport -d data_imagepaths --headerline -c archselects -type csv -f fields-sep-by-coma --drop /var/tmp/post_ready_original.txt
