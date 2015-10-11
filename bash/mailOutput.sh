#!/bin/bash

bodyContent=$1
subj=$2
emailAddress=$3
TODAY=`date "+%a-%b-%d"`

echo "" $bodyContent | mail -s "$TODAY $subj" $emailAddress
