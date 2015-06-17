#!/bin/bash -xv

. ~/.bash_profile


query_marketplace_inprog="/usr/local/batchRunScripts/sql/marketplace_update_filter.sql"

cnx=$($BFYPRDLOGIN \"@\"$query_marketplace_inprog;)

echo "Total to Update ...." ;

for f in $cnx ;
do
# 	/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py "$f" ;
echo Completed "$f" ;
done

##parallel -P2 -X --progress echo {} :::
# echo $(env | sort)
#echo $(echo ${res} | grep -v selected | xargs -n1) ##| wc -l

##/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py
