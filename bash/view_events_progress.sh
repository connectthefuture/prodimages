#!/bin/bash

. ~/.bash_profile



mysql -H -u root -pmysql data_imports<<EOFMYSQL
SELECT * FROM data_imports.view_event_upcoming_incomplete;
EOFMYSQL
