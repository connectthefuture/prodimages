#!/bin/bash

. ~/.bash_profile





## Generate HTML email of event progress replacing TR tag on Incomplete rows with sed to show in Red/Salmon mmmmm

##/usr/local/batchRunScripts/view_events_progress.sh | sed -e 's/<TD>Production\ Incomplete<\/TD>/<TD\ style\=\"background\-color\:rgb\(250,75,90\)\">Production\ Incomplete<\/TD>/g' > /Users/johnb/Dropbox/Dropbox_sites/queries_run_search/Reports/event_progress_14days.html && php -f /usr/local/batchRunScripts/mail_sql/eventmail_sp.php


/usr/local/batchRunScripts/bash/view_events_progress.sh | sed -e 's/<TD>Production\ Incomplete<\/TD>/<TD\ style\=\"background\-color\:rgb\(250,75,90\)\">Production\ Incomplete<\/TD>/g' > /mnt/Post_Ready/zImages_1/dag/sites/queries_PHP-test1/Reports/event_progress_14days.html ;

/usr/local/batchRunScripts/bash/view_events_incomplete.sh | sed -e 's/<TR>/<TR\ style\=\"background\-color\:rgb\(200,175,220\)\">/g' | sed -e 's/<TR>/<TR\ style\=\"background\-color\:rgb\(200,75,160\)\">/1' | sed -e 's/\(<\/TD>\)/<\/strong>\1/g' | sed -e 's/\(<TD>\)/\1<strong>/g' | sed -e 's/<\(TD\)><strong>\([0-9][0-9][0-9][0-9]\)<\/strong><\/TD><TD><strong>\(2[0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]\)<\/strong>/<\1><b><a href\=\"http\:\/\/pm.bluefly.corp\/manager\/event\/editevent.html\?id\=\2\">\2<\/a><\/b><\/TD><TD><b><a href\=\"http\:\/\/pm.bluefly.corp\/manager\/event\/viewproductimages.html\?id\=\2\">\3<\/a><\/b>/g' > /mnt/Post_Ready/zImages_1/dag/sites/queries_PHP-test1/Reports/event_incomplete_14days.html ;






