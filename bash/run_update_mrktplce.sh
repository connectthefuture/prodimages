#!/bin/bash -xv

# . ~/.bash_profile

# shopt -s xpg_echo expand_aliases direxpand
# shopt -u hostcomplete extquote
# export LANGUAGE="en" ;
query_marketplace_inprog="/usr/local/batchRunScripts/sql/marketplace_update_filter.sql"

RES='$(sqlplus prod_team_ro/9thfl00r@//borac101-vip.l3.bluefly.com:1521/bfyprd1 @$query_marketplace_inprog) | xargs -n1 | grep -v selected'
#res='sqlplus -S prod_team_ro/9thfl00r@//borac101-vip.l3.bluefly.com:1521/bfyprd1 @/usr/local/batchRunScripts/sql/marketplace_update_filter.sql'
#runit=$(${sqlcmd} | /bin/bash)
#res=$runit
#res=`$sqlcmd`
cat 
#locale ;
#cd /usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace
echo "Total to Update ...." ;
echo $RES ;
echo 'ENDDDN'
for f in `${RES}` ;
do
# 	/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py "$f" ;
echo Completed "$f" ;
done

##parallel -P2 -X --progress echo {} :::
# echo $(env | sort)
#echo $(echo ${res} | grep -v selected | xargs -n1) ##| wc -l

##/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x-vendorget-module-cronjobDloader.py
