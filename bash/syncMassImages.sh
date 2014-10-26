#!/bin/bash


DATE=`date +%m%d%y`

origname='/mnt/Post_Ready/xsyncma/'

syncdname="/mnt/Post_Ready/aPhotoPush/${DATE}_MA/999999999/"


mkdir -p $syncdname

find $origname -type f -maxdepth 1 -iname \*_[1-6].jpg -exec mv {} $syncdname \;

