#!/bin/bash
. ~/.bash_profile


exiftool -r -m '-Directory=%9f/' '-Filename=%9f%+.nc.%e' $1

exit;
