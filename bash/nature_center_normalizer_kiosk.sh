#!/bin/bash

. ~/.bash_profile

export PWD=/mnt/Post_Complete/Complete_to_Load/nature_center
echo "`date`_`pwd`" >> ~/.naturecenter.log


regex_matcherator_matched=`python py-scriptReturning-Styles.py`

if [ "$regex_matcherator_matched" == "" ]; then
echo "NothingToDo `date`_`pwd`" > ~/.naturecenter.log
else
# echo "ELSE"
for f in regex_matcherator_matched; do
    some_image_func "$f" ;
    echo "SomethingsBeenDone `date`_${f}" > ~/.naturecenter.log
done;
fi;
