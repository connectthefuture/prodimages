#!/bin/bash

. ~/.bash_profile

# shopt -s xpg_echo expand_aliases direxpand
# shopt -u hostcomplete extquote
export LANGUAGE="en" ;
query_marketplace_inprog="/usr/local/batchRunScripts/sql/marketplace_update_filter.sql"

##res=`sqlplus -S prod_team_ro/9thfl00r@//borac101-vip.l3.bluefly.com:1521/bfyprd1 @$query_marketplace_inprog | xargs -n1 | grep -v selected`
res='sqlplus -S prod_team_ro/9thfl00r@//borac101-vip.l3.bluefly.com:1521/bfyprd1 @/usr/local/batchRunScripts/sql/marketplace_update_filter.sql'
#runit=$(${sqlcmd} | /bin/bash)
#res=$runit
#res=`$sqlcmd`
locale ;
#cd /usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace
echo "Total to Update ...." ;

for f in `$res`; do
# 	/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py "$f" ;
echo Completed "$f" ;
done

##parallel -P2 -X --progress echo {} :::
echo "$ENV"
#echo $(echo ${res} | grep -v selected | xargs -n1) ##| wc -l

##/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py
