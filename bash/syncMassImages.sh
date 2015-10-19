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

## Below line automates posting Looklet to site immediately
find $orignameLL -type f -maxdepth 1 -iname \*_[1-6x].jpg -exec cp {} /mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly/JamesHoetker/ \;

find $orignameLL -type f -maxdepth 1 -iname \*_[1-6x].jpg -exec mv {} $syncdnameLL \;
chmod -R ugo+rx $syncpardnameLL ;
chmod -R ugo+rx $syncdnameLL ;


#############################################
## Sync Looklet Images Stripped for Design ##
#############################################
orignameLLDes='/mnt/Post_Ready/xsyncma/looklet/'
syncpardnameLLDes="/mnt/Design/LookletSync/${DATE}_LLD/"
syncdnameLLDes="/mnt/Design/LookletSync/${DATE}_LLD/"

mkdir -p $syncdnameLLDes

find $orignameLLDes -type f -maxdepth 1 -iname \*_[B1-9x][B1-9x].jpg -exec mv {} $syncdnameLLDes \;
chmod -R ugo+rx $syncpardnameLLDes ;
chmod -R ugo+rx $syncdnameLLDes ;


######################################################
## Sync Looklet Editorials for Design And Merchants ##
######################################################
orignameLLED='/mnt/Post_Ready/xsyncma/looklet/'
syncpardnameLLED="/mnt/Design/LookletEditorial/${DATE}_ED/"
syncdnameLLED="/mnt/Design/LookletEditorial/${DATE}_ED/"

mkdir -p $syncdnameLLED

find $orignameLLED -type f -maxdepth 1 -iname \*[0-9][0-9][0-9][0-9][0-9][0-9]_[lL]\*_ED\*.jpg -exec mv {} $syncdnameLLED \;

chmod -R ugo+rx $syncpardnameLLED ;
chmod -R ugo+rx $syncdnameLLED ;

### TODO: Embed Metadata in Files if Product Style Can be Retrieved
##---#
##################################
### TODO: Now Sync Editorial to ##
###  Shared GDrive FolderUrls ####
########################Ø#########


#########################
## Remove empty folders #
#########################
find /mnt/Post_Ready/aPhotoPush -mindepth 1 -type d -empty -exec rmdir {} \;
find /mnt/Design/LookletSync -mindepth 1 -type d -empty -exec rmdir {} \;
find /mnt/Design/LookletEditorial -mindepth 1 -type d -empty -exec rmdir {} \;

# /usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/x_vendorget_module_cronjobDloader.py Editorial ALL 12

#############
## sync crontab
cd /root && crontab crontabmain ;
