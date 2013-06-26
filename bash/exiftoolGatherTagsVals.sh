#!/bin/bash
. ~/.bash_profile



exiftool -f -r -fast2 -q -m -IPTC:All -XMP:All -d %d-%b-%Y -G -csv ${PRODSRV}/images > ${PRODSRV}/data/csv/exifdata_imgsrv7.csv



exit;
