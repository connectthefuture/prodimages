#!/bin/bash

. /home/johnb/.bash_profile
TODAY=`date`

function recent_styles_uploaded () 
		{
		
		if [[ "$#" > 0 ]]; then
	    	MINUTESAGO=$1
	    else
	        MINUTESAGO=60
	    fi;
		QUERY=`echo -e "select distinct t1.colorstyle from www_django.image_update t1 join product_snapshot_live t2 on t1.colorstyle=t2.colorstyle where create_dt < date_sub(now(), interval $MINUTESAGO minute) and (t2.image_ready_dt is not null and t2.image_ready_dt != \"0000-00-00\");"`
		$(mysql --host=127.0.0.1 --port=3301 --column-names=False --user=root --password=mysql -e "$QUERY" -D www_django;)
	}

#logdate=echo "$TODAY $f" >> /mnt/Post_Complete/Complete_Archive/AUTOCCLEARLOG.log
#`mysql --host=127.0.0.1 --port=3301 --column-names=False --user=root --password=mysql -e "$QUERY" -D www_django;` | parallel -X -N1 --jobs 16 --progress "/usr/local/batchRunScripts/python/newAll_Sites_CacheClear.py {}; $logdate"


export -f recent_styles_uploaded ;
STYLES=`recent_styles_uploaded() | xargs -n1 | sort -nru`
STCOUNT=`echo $STYLES | xargs -n1 | wc -l`
echo -e "${TODAY}\v${STCOUNT}\n" >> /mnt/Post_Complete/Complete_Archive/AUTOCCLEARLOG.log

parallel -P2 --memfree 2G --jobs 800% -q /usr/local/batchRunScripts/python/newAll_Sites_CacheClear.py {} ::: echo $STYLES




