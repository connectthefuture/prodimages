#!/bin/bash
. ~/.bash_profile

##rm -r $tmpPhotoSelects/
mkdir $tmpPhotoSelects/

        ## Get Selects for push folders and Sort to tmp Server folder
cd $tmpPhotoSelects;
exiftool -r -o "'"$tmpPhotoSelects"'" '-Directory='"$tmpPhotoSelects"'/%4f' '-Filename=%f.%e' /mnt/Post_Ready/eFashionPush -ext jpg & exiftool -r -o "'"$tmpPhotoSelects"'" '-Directory='"$tmpPhotoSelects"'/%4f' '-Filename=%f.%e' /mnt/Post_Ready/aPhotoPush -ext jpg \;

        ### Sync Temp folder with primary image repo---aka images_jpg_PhotoSelects
sleep 30 && rsync -CtavzP $tmpPhotoSelects/ $PRODSRV/images/images_jpg_PhotoSelects/

exit;
