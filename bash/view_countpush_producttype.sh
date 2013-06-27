#!/bin/bash

. ~/bash_profile



mysql -u root -proot data_imagepaths<<EOFMYSQL
SELECT * FROM data_imagepaths.viewcount_prdsnapshot_pushselects_producttype ORDER BY producttype ASC;
EOFMYSQL
