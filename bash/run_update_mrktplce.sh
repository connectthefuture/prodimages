#!/bin/bash

. ~/.bash_profile


query_marketplace_inprog="/usr/local/batchRunScripts/sql/marketplace_update_filter.sql"


echo "Total to Update ...." ;

for f in $(echo -e `$BFYPRDLOGIN '@'$query_marketplace_inprog`); 
do 
echo -e "$f" ; 
# /usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py "$f" ;
done ;
