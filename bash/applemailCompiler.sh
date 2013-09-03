#!/bin/bash

. ~/.bash_profile

compiledFile=$DATASRV/csv/samplesNightlyCompiled.txt
sampleMail=`find /Users/johnb/Library/Mail/Mailboxes/AutoDownloads.mbox/Attachments -type f -ctime 48h -iname \*Daily\*`

##for f in $sampleMail; do cat $f | sed 's/\ //g' | grep -av \( >> $compiledFile;
##find /Users/johnb/Library/Mail/Mailboxes/AutoDownloads.mbox/Attachments -type f -ctime 18h -iname \*Daily\*


for f in $sampleMail
do
cat $f | sed 's/\ //g' | grep -av \( >> $compiledFile; 
echo -e \t\t"$TODAY" >> $compiledFile;
done;


exit;
