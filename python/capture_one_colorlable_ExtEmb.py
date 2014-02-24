#!/usr/bin/env python



def get_exif_all_data(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(image_filepath)
        #['XMP:DateCreated'][:10].replace(':','-')
    return metadata
    
    
######################   
import os,sys,re
from collections import defaultdict
filepath = os.path.abspath(sys.argv[1])
directory = os.path.dirname(filepath)
filename  = os.path.basename(filepath)

capture1settings="{0}/CaptureOne/Settings50/{1}.cos".format(directory,filename)


capture_one_colortag = ''
if ['XML:Color_tag_index'] == 0:
    capture_one_colortag = 'None'
elif ['XML:Color_tag_index'] == 1:
    capture_one_colortag = 'Issues-RED'
elif ['XML:Color_tag_index'] == 2:    
    capture_one_colortag = 'Special-Blue'
elif ['XML:Color_tag_index'] == 3:    
    capture_one_colortag = 'PreSelect-YELLOW'
elif ['XML:Color_tag_index'] == 4:
    capture_one_colortag = 'Select-GREEN'
    
    
    
    
mdata         = get_exif_all_data(filepath)
capture1data  = get_exif_all_data(capture1settings)


mdata         = sorted(mdata.items())capture1data  = sorted(capture1data.items())