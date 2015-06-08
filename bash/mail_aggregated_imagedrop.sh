#!/bin/bash

. ~/.bash_profile



fname=$(find /mnt/Post_Complete/ImageDrop/bkup/*LSTransfer* -type f -mmin -20 -exec ls -cltrs {} \;| awk '{ print $NF }' | tail -1)

allfiles=`cat "$fname" | grep \.png | wc -l`
primaryonly=`cat "$fname" | grep \_m.jpg | wc -l`
altonly=`cat "$fname" | grep \_alt0?.*ng | wc -l`

subject=$(echo "Uploaded: ${allfiles} files - ${primaryonly} Styles")
content=$("Total Styles:\t${allfiles} \nMain Images Total: \t${primaryonly} \n Total Alts: \t${altonly}")


/usr/local/batchRunScripts/python/mailGmailStdOut.py "${content}" "${subject}"

echo "${subject} -- \n ${text}"