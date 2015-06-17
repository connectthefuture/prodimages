#!/bin/bash

# . ~/.bash_profile

shopt -s xpg_echo expand_aliases direxpand
shopt -u hostcomplete extquote

query_marketplace_inprog="/usr/local/batchRunScripts/sql/marketplace_update_filter.sql"

sqlcmd="sqlplus -S prod_team_ro/9thfl00r@//borac101-vip.l3.bluefly.com:1521/bfyprd1 @${query_marketplace_inprog}"
# sqlcmd="sqlplus -S prod_team_ro/9thfl00r@//borac101-vip.l3.bluefly.com:1521/bfyprd1 @/usr/local/batchRunScripts/sql/marketplace_update_filter.sql"
runit=$(${sqlcmd} | /bin/bash)
res=$(${runit})
res="$sqlcmd"

#cd /usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace
echo "Total to Update ...." ;

# for f in `echo "$res" | xargs -n1 | grep -v selected`; do
# 	/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py "$f" ;
# 	#echo Completed "$f" ;
# done

##parallel -P2 -X --progress echo {} :::
echo ${runit}
echo $(echo ${res} | grep -v selected | xargs -n1) | wc -l

echo $(shopt)
##/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py
