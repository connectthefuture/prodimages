#!/bin/bash

#. ~/.bash_profile

styles=`find /mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/4_Archive/JPG/LIST_PAGE_LOADED -iname \*_l.jpg -mtime -2 -exec basename {} \; | sed 's/_l.jpg//g' | xargs`

for s in $styles; do 
/bin/bash/python blueflypdp_AllServer_cache_clear.py $s; 
echo "$s";
done

