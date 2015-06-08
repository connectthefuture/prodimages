#!/bin/bash

. ~/.bash_profile



fname=$(find /mnt/Post_Complete/ImageDrop/bkup/*LSTransfer* -type f -mmin -20 -exec ls -cltrs {} \;| awk '{ print $NF }' | tail -1)

allfiles=`cat "$fname" | grep \.png | wc -l`
primaryonly=`cat "$fname" | grep \_m.jpg | wc -l`
altonly=`cat "$fname" | grep \_alt0?.jpg | wc -l`

echo "${allfiles} -- ${primaryonly} -- ${altonly}"
