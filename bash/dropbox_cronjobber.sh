#!/bin/bash

. ~/.bash_profile


logTime=`date`
dropboxRunDir=/Users/johnb/Dropbox/Dropbox_sites/prodjohn8_scriptrun/prodjohn8_run
dropboxDunDir=/Users/johnb/Dropbox/Dropbox_sites/prodjohn8_scriptrun/prodjohn8_complete

testArgs1=`ls "$dropboxRunDir" | wc -l`

if [ "$testArgs1" -gt 0 ];
	then
	echo "$logTime__$testArgs1" >> "$dropBoxDunDir"/cronscriptrunlog.log

	search=`find $dropboxRunDir -type f -name \*.sh`
	testSearch=`echo $search | wc -l`

	
	if [ "$testSearch" -gt 0 ];
		then
		
		for f `find $dropboxRunDir -type f -name \*.sh`
		do
		echo "RUNNING--$logTime__$f" >> "$dropBoxDunDir"/cronscriptrunlog.log;
		/bin/bash $f;
		sleep 1;
		echo "COMPLETED--$logTime__$f" >> "$dropBoxDunDir"/cronscriptrunlog.log
		mv $f $dropboxRunDir
		done;


	fi;
fi;

exit;
