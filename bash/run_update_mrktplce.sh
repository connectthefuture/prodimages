#!/bin/bash

. ~/.bash_profile


query_marketplace_inprog="/usr/local/batchRunScripts/sql/marketplace_update_filter.sql"
result=`sqlplus -S prod_team_ro:9thfl00r\\@borac101-vip.l3.bluefly.com:1521/bfyprd11 @$query_marketplace_inprog`

cd /usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace
echo "Total to Update ...." ;
echo "$result" | xargs -n1 | wc -l ;

for f in "$result"; do
/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py "$f" ;
echo Completed "$f" ;
done
