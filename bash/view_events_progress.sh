#!/bin/bash

. ~/.bash_profile



mysql -H -u root -proot data_imports<<EOFMYSQL
SELECT * FROM data_imports.view_event_upcoming_incomplete;
EOFMYSQL
