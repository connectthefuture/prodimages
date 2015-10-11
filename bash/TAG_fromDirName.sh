#!/bin/bash

find /home/johnb/mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly -type f -iname \*.jpg | sed s/\ /'\\ '/g | xargs exiftool -'Directory' -csv | awk '{ split($1, a, "//"); print $0" "a[3] }' | awk '{ split($1, a, ","); print "exiftool -f -overwrite_original -P -fast2 -m -'IPTC:RetoucherName'="$NF, a[1] }' | /bin/bash
