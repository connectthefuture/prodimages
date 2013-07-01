#!/bin/bash

. ~/.bash_profile


mysql -H -uroot -pmysql data_imports<<EOFMYSQL
SELECT * FROM data_imports.view_event_only_incomplete;
EOFMYSQL
