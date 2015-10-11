#!/bin/bash
. ~/.bash_profile



exiftool -f -r -fast2 -q -m -IPTC:All -XMP:All -d %Y-%m-%d -G -csv ${PRODSRV}/images > ${PRODSRV}/data/csv/exifdata_imgsrv7.csv ;



cp ${PRODSRV}/data/csv/exifdata_imgsrv7.csv ~/Dropbox/exifdata_imgsrv7.csv ;


exit;
