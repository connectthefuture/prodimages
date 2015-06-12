#!/bin/bash

. ~/.bash_profile


query_marketplace_inprog="/usr/local/batchRunScripts/sql/marketplace_update_filter.sql"

sqlcmd="sqlplus -S prod_team_ro/9thfl00r@//borac101-vip.l3.bluefly.com:1521/bfyprd1 @${query_marketplace_inprog}"
runit=$(echo "$sqlcmd")
res=$(${runit})

cd /usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace
echo "Total to Update ...." ;

# for f in `echo "$res" | xargs -n1 | grep -v selected`; do
# 	/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py "$f" ;
# 	#echo Completed "$f" ;
# done

parallel -P2 --progress /usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py {} ::: `echo "$res" | grep -v selected`