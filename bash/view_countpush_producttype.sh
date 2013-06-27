#!/bin/bash

. ~/bash_profile



mysql -u root -pmysql data_imagepaths<<EOFMYSQL
SELECT * FROM data_imagepaths.viewcount_prdsnapshot_pushselects_producttype ORDER BY producttype ASC;
EOFMYSQL
