#!/bin/bash

. ~/bash_profile


/Applications/AMPPS/mysql/bin/mysql -u root -proot data_imagepaths<<EOFMYSQL
SELECT * FROM data_imagepaths.viewcount_prdsnapshot_pushselects_category ORDER BY category ASC;
EOFMYSQL
