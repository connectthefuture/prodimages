#!/bin/bash
. ~/.bash_profile




## Search Database for single style output for load to Tool. As in copy over descriptions
query=`$DSSPRDLOGIN @/mnt/Post_Ready/zProd_Server/imageServer7/scripts/sql/copy_over_colorstyles.sql "$1"` 

if [ "$#" -gt 1 ]; 
then 
echo "$query" | sed "s/$1/$2/1" | sed "s/\'/\\\'/g" | xargs oracle_output_cleaner.sh;
 
elif [ "$#" -eq 1 ];
then
echo '$query' | sed "s/\'/\\\'/g" | xargs oracle_output_cleaner.sh; 

fi;
exit;
