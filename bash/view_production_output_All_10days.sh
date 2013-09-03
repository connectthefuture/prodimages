#!/bin/bash

. ~/.bash_profile


mysql -H -uroot -pmysql data_imagepaths<<EOFMYSQL
SELECT * FROM data_imagepaths.view_count_completions_allteams_past10days;
EOFMYSQL
