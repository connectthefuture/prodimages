#/bin/bash
. ~/.bash_profile
exiftool -o renamed/ '-filename=%5f%+.nc.%e' $1
exit;
