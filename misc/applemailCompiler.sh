#!/bin/bash

. ~/.bash_profile


sampleMail=`find /Users/johnb/Library/Mail/Mailboxes/AutoDownloads.mbox/Attachments -type f -iname \*Daily\*`




for f in $sampleMail; do cat $f | sed 's/\ //g' >> ~/Documents/samplesDailycompile.txt; done;


exit;
