#!/bin/bash

. ~/.bash_profile


filepath=$1

filename=`basename $filepath`
directory=`dirname $filepath`
capture1settings="${directory}/CaptureOne/Settings50/${filename}.cos"

exiftool -j -G1 -All $capture1settings
