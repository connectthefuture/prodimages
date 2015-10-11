#!/bin/bash
. ~/.bash_profile

rsync --progress --log-file=/mnt/Post_Ready/zProd_Server/imageServer7/logs/rsync_pushToTmpImageSrv7.txt -avzdi /mnt/Post_Ready/aPhotoPush/ /mnt/Post_Ready/Retouch_Still & rsync --progress --log-file=/mnt/Post_Ready/zProd_Server/imageServer7/logs/rsync_pushToTmpImageSrv7.txt -avzdi /mnt/Post_Ready/eFashionPush/ /mnt/Post_Ready/Retouch_Fashion \;


