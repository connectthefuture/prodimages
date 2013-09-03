#!/bin/bash
. ~/.bash_profile

unzip - -u -o -qq ~/Dropbox/aSharedFolder/UNION_SQUARE/\*.zip -d /mnt/Post_Ready/eFashionPush/

find ~/Dropbox/aSharedFolder/UNION_SQUARE/ -iname \*.zip -exec mv {} /mnt/Post_Ready/x_original/ \;

rm -R /mnt/Post_Ready/eFashionPush/__MACOSX;

exit;
