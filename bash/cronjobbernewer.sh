#!/bin/bash
. ~/.bash_profile


REMRUN=~/Dropbox/Apps/PythonistaAppOnly/remrun/run
#cd $REMRUN

if [ `find $REMRUN -mmin -1 -type f | wc -l` -gt 0 ];
then
    for f in `find $REMRUN -mmin -1`;
    do
    ext=`basename "$f" | awk -F. '{ print $NF }'`
    cd $REMRUN
    echo $ext
    if [ $ext == "sh" ];
        then
        /bin/bash $f
        echo "Bash File: $f was Executed at "`date`
        echo "Bash File: $f was Executed at "`date` >> .cronjoblogfile.txt
    elif [ $ext == "py" ];
        then
        /usr/bin/python $f
        echo "Python File: $f was Executed at "`date`
        echo "Python File: $f was Executed at "`date` >> .cronjoblogfile.txt
    else
    echo "File: $f Was Received and Passed Over at "`date`
    echo "File: $f Was Received and Passed Over at "`date` >> .cronjoblogfile.txt
    fi;

    done;
fi;