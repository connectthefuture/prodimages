#!/bin/bash

. ~/.bash_profile


query_marketplace_inprog="/usr/local/batchRunScripts/sql/marketplace_update_filter.sql"

echo "Total to Update ...." ;

for f in $(echo -e `$BFYPRDLOGIN '@'$query_marketplace_inprog`);
do
echo -e "/mnt/Post_Complete/Complete_Archive/MARKETPLACE/*/*/${f}/"
/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x_vendorget_module_cronjobDloader.py "$f" ;
echo -e "Loaded: \t${f}"
find /mnt/Post_Complete/Complete_Archive/MARKETPLACE/*/*/${f}/ -type f -exec rm {} \;
echo -e "Deleted: \t${f}"
done ;
