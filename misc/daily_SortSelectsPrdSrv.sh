#!/bin/bash
. ~/.bash_profile



exiftool -r -o $tmpPhotoSelects/ '-Directory=$PRODSRV/tmp/$tmpPhotoSelects/%4f/%9f' /mnt/Post_Ready/eFashionPush -ext jpg & exiftool -r -o $tmpPhotoSelects/ '-Directory=$PRODSRV/tmp/$tmpPhotoSelects/%4f/%9f' /mnt/Post_Ready/aPhotoPush -ext jpg \;
sleep 10 &&

rsync -avz $tmpPhotoSelects/ $PRODSRV/images/images_jpg_PhotoSelects/


exit;
