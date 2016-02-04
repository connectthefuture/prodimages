#!/bin/bash

ZEROBYTE=`find /mnt/Post_Complete/Complete_Archive/MARKETPLACE/*/*/*.* -size -5k -type f` ;
find /mnt/Post_Complete/Complete_Archive/MARKETPLACE/*/*/*.* -size -3k -type f -exec mv {} /mnt/Post_Complete/Complete_to_Load/test0kb/ \;
parallel -q cp {} /mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly/JohnBragato/ ::: /mnt/Post_Complete/Complete_Archive/MARKETPLACE/*/*/*.* ;

chmod -R 777 /mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly/JohnBragato/ & \
REPORT_CONTENT=$(echo -e \'"$ZEROBYTE"\' | sed 's/^ *//g' | awk -v RS='\n' -F/ '{ split($0, a, "/"); print "\nVendor: "a[6], "\nPO: "a[7], "\nBF_IMAGEID: "a[8] }') ;
MAIL_CONTENT=$(echo -e "$REPORT_CONTENT" | grep -v PO | grep -v BF_IMAGE | sort -rud) ;
mailGmailStdOut.py 'john.bragato@bluefly.com' "$ZEROBYTE"
# "$MAIL_CONTENT"
