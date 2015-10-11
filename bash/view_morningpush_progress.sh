#!/bin/bash

. ~/.bash_profile



mysql -H -u root -pmysql data_imagepaths<<ENDOFMYSQL
SELECT * FROM data_imagepaths.viewcount_prdsnapshot_pushselects_brand ORDER BY brand ASC;
ENDOFMYSQL


mysql -H -u root -pmysql data_imagepaths<<ENDOFMYSQL
SELECT * FROM data_imagepaths.viewcount_prdsnapshot_pushselects_category ORDER BY category ASC;
ENDOFMYSQL

mysql -H -u root -pmysql data_imagepaths<<ENDOFMYSQL
SELECT * FROM data_imagepaths.viewcount_prdsnapshot_pushselects_gender ORDER BY gender ASC;
ENDOFMYSQL

