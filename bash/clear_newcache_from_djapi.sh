#!/bin/bash

. /home/johnb/.bash_profile

MINUTESAGO=$1
QUERY="select distinct t1.colorstyle from image_update t1 join product_snapshot_live t2 on t1.colorstyle=t2.colorstyle where create_dt > date_sub(now(), interval $MINUTESAGO minute) and (t2.image_ready_dt is not null and t2.image_ready_dt != \"0000-00-00\");"

for f in $(mysql --host=127.0.0.1 --port=3301 --column-names=False --user=root --password=mysql -e $QUERY -D www_django); do 
	/usr/local/batchRunScripts/python/newAll_Sites_CacheClear.py $f ; 
	echo "`date` $f"
done 

