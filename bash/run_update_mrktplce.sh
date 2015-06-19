#!/bin/bash

#. ~/.bash_profile


query_marketplace_inprog="/usr/local/batchRunScripts/sql/marketplace_update_filter.sql"


echo "Total to Update ...." ;

<<<<<<< HEAD
for f in `echo "$res" | xargs -n1 | grep -v selected`; do
    #/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py "$f" ;
    echo Completed "$f" ;
done

##parallel -P2 -X --progress echo {} ::: 
$runit
echo $(echo "$res" | grep -v selected | xargs -n1) | wc -l

echo $(shopt)
##/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py
=======
for f in $(echo -e `$BFYPRDLOGIN '@'$query_marketplace_inprog`);
do
echo -e "/mnt/Post_Complete/Complete_Archive/MARKETPLACE/*/*/${f}/"
/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py "$f" ;
echo -e "Loaded: \t${f}"
find /mnt/Post_Complete/Complete_Archive/MARKETPLACE/*/*/${f}/ -type f -exec rm {} \;
echo -e "Deleted: \t${f}"
done ;
>>>>>>> 0d27f166230cef17e0b3ba95fdda27ae069e2bc3
