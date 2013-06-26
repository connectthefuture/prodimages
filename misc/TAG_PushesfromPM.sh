#!/bin/bash
. ~/.bash_profile
. ~/.bashrc
####first Tag All Followed by only Event Tags
aFullerGreatMetaTagDirect.sh ${pushFashion}
#/usr/local/batchRunScripts/anEventCentricMetaTagDirect.sh /mnt/Post_Ready/eFashionPush
aFullerGreatMetaTagDirect.sh ${pushStill}
#/usr/local/batchRunScripts/anEventCentricMetaTagDirect.sh /mnt/Post_Ready/aPhotoPush
exit;
