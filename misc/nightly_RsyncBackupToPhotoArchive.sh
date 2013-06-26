#!/bin/bash
. ~/.bash_profile

    #Sync push Folders to Archives
rsync -CtavzP ${pushStill} ${archStill} & rsync -CtavzP ${pushFashion} ${archFashion} \;

    ##Sort Selects to TmpFolder on Server
sleep 25 && exiftool -r -o ${tmpPhotoSelects}/ '-Directory='${tmpPhotoSelects}'/%4f/%9f' ${pushStill}/ -ext jpg & exiftool -r -o ${tmpPhotoSelects}/ '-Directory='${tmpPhotoSelects}'/%4f/%9f' ${pushFashion}/ -ext jpg \;

    ##Sync TempFolder to Image_Jpg_PhotoSelects on PRODSRV
sleep 25 && rsync -CtavzP ${tmpPhotoSelects}/ ${PRODSRV}/images/images_photoselects_jpg/

    ##After copy and sync, clear any Folders in the push folders more than 5 days old, move to TmpDelete Folder
sleep 25 && find ${pushStill} ${pushFashion} -type d -mindepth 1 -maxdepth 1 -mtime +5 -exec mv -p {} ${tmpDeletePhoto} \;
    ##Clear TempDelete Folder, DELETING ALL FOLDERS over 10 days old
find ${tmpDeletePhoto} -type d -mindepth 1 -maxdepth 1 -mtime +10 -exec rm -R {} \;

    ##Delete TmpSelects Folder and Remake
##rm -R ${tmpPhotoSelects}/ && mkdir ${tmpPhotoSelects}/

exit;
