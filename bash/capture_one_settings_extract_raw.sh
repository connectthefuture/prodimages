#!/bin/bash

. ~/.bash_profile


filepath=$1

filename=`basename $filepath`
directory=`dirname $filepath`
capture1settings="${directory}/CaptureOne/Settings50/${filename}.cos"

exiftool -j -G1 -All $capture1settings
"XML:Color_tag_index": 0,#
"XML:Color_tag_index": 3,#
"XML:Color_tag_index": 4,



def get_exif_all_data(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(image_filepath)#['XMP:DateCreated'][:10].replace(':','-')
    return metadata