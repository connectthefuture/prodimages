#!/bin/bash
. ~/.bash_profile

$SCRIPTS/styleStringPro.sh $PRODSRV/images/images_jpg_PhotoSelects $PRODSRV/data/csv/ &
$SCRIPTS/styleStringPro.sh $PRODSRV/images/images_jpg_Retouched $PRODSRV/data/csv/ &
$SCRIPTS/styleStringPro.sh $PRODSRV/images/images_jpg-png_AltUpload $PRODSRV/data/csv/ &
$SCRIPTS/styleStringPro.sh $PRODSRV/images/images_jpg-png_PrimaryUpload $PRODSRV/data/csv/ \;

exit;
