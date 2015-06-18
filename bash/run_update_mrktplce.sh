#!/bin/bash

. ~/.bash_profile


query_marketplace_inprog="/usr/local/batchRunScripts/sql/marketplace_update_filter.sql"


echo "Total to Update ...." ;

for f in $(echo -e `$BFYPRDLOGIN '@'$query_marketplace_inprog`); 
do 
/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py "$f" ;
echo "Done with ${f}"
find /mnt/Post_Complete/Complete_Archive/MARKETPLACE/*/*/${f}/ -type f -exec rm {} \;
done ;
