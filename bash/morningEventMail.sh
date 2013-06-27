#!/bin/bash

. ~/.bash_profile





## Generate HTML email of event progress replacing TR tag on Incomplete rows with sed to show in Red/Salmon mmmmm

##/usr/local/batchRunScripts/view_events_progress.sh | sed -e 's/\<TD\>Production\ Incomplete\<\/TD\>/\<TD\ style\=\"background\-color\:rgb\(250,75,90\)\"\>Production\ Incomplete\<\/TD\>/g' > /Users/johnb/Dropbox/Dropbox_sites/queries_run_search/Reports/event_progress_14days.html && php -f /usr/local/batchRunScripts/mail_sql/eventmail_sp.php


/usr/local/batchRunScripts/bash/view_events_progress.sh | sed -e 's/\<TD\>Production\ Incomplete\<\/TD\>/\<TD\ style\=\"background\-color\:rgb\(250,75,90\)\"\>Production\ Incomplete\<\/TD\>/g' > /mnt/Post_Ready/zImages_1/dag/sites/queries_PHP-test1/Reports/event_progress_14days.html






