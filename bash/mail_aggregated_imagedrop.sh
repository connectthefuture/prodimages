#!/bin/bash

. ~/.bash_profile



fname=$(find /mnt/Post_Complete/ImageDrop/bkup/*LSTransfer* -type f -cmin -5 -exec ls -cltrs {} \;| tail -1 | awk '{ print $NF }')

allfiles=`cat "$fname" | grep \.png | wc -l`
primaryonly=`cat "$fname" | grep \.png | wc -l`
altonly=`cat "$fname" | grep \_alt0?.png | wc -l`


