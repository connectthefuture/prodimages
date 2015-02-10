#!/bin/bash
. ~/.bash_profile

DATE=`date +%m%d%y`

##########################
## Sync Mass Studio Images
##########################
origname='/mnt/Post_Ready/xsyncma/'

syncpardname="/mnt/Post_Ready/aPhotoPush/${DATE}_MA/"
syncdname="/mnt/Post_Ready/aPhotoPush/${DATE}_MA/999999999/"

mkdir -p $syncdname

find $origname -type f -maxdepth 1 -iname \*_[1-6].jpg -exec mv {} $syncdname \;

chmod -R ugo+rx $syncpardname ;
chmod -R ugo+rx $syncdname ;

######################
## Sync Looklet Images
######################
orignameLL='/mnt/Post_Ready/xsyncma/looklet/'
syncpardnameLL="/mnt/Post_Ready/aPhotoPush/${DATE}_LL/"
syncdnameLL="/mnt/Post_Ready/aPhotoPush/${DATE}_LL/999999999/"

mkdir -p $syncdnameLL


find $orignameLL -type f -maxdepth 1 -iname \*_[1-6x].jpg -exec cp {} /mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly/JamesHoetker/ \;
find $orignameLL -type f -maxdepth 1 -iname \*_[1-6x].jpg -exec mv {} $syncdnameLL \;
chmod -R ugo+rx $syncpardnameLL ;
chmod -R ugo+rx $syncdnameLL ;

######################
## Remove empty folders
######################
find /mnt/Post_Ready/aPhotoPush -type d -mindepth 1 -empty -exec rmdir {} \;
