#!/bin/bash

. /home/johnb/.bash_profile
TODAY=`date`

export -f recent_styles_uploaded;
STYLES=$(recent_styles_uploaded | xargs -n1 | sort -nru)
STCOUNT=$(echo "${STYLES[@]}" | xargs -n1 | wc -l)
for f in $STYLES; do
	echo -e "Date: ${TODAY}\tStyle: ${f}\tTotal: ${STCOUNT[@]}\n" 2>&1 >> /mnt/Post_Complete/Complete_Archive/AUTOCCLEARLOG.log
	/usr/local/batchRunScripts/python/anotherTest_Sites_CacheClear.py "$f" 2>&1 > /dev/null && echo -e "Date: ${TODAY}\tStyle: ${f}\tTotal: ${STCOUNT}\n"
done;
