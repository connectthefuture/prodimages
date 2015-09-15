#!/bin/bash

. /home/johnb/.bash_profile
TODAY=`date "+Date:%Y-%m-%d_%H:%M:%S"`

## Need to get recent_styles_uploaded function from ~/.bash_functions 
## -- ~.bash_profile should handle the initial import to environment
export -f recent_styles_uploaded;
local STYLES=$(recent_styles_uploaded | xargs -n1 | sort -nru)
local STCOUNT=$(echo "${STYLES[@]}" | xargs -n1 | wc -l)
echo -e "\n---------\nBatchSize:$STCOUNT\n$TODAY" 2>&1 >> /mnt/Post_Complete/Complete_Archive/AUTOCCLEARLOG.log
for f in $STYLES; do
	echo -e "${TODAY}\tStyle: ${f}\tTotal:${STCOUNT}\n" 2>&1 >> /mnt/Post_Complete/Complete_Archive/AUTOCCLEARLOG.log
	/usr/local/batchRunScripts/python/anotherTest_Sites_CacheClear.py "$f" 2>&1 > /dev/null && echo -e "${TODAY}\tStyle:${f}\tTotal:${STCOUNT}\n"
done;
echo -e "Completed:${TODAY}\tTotal:${STCOUNT}\n"
