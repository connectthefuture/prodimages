m#!/usr/bin/env python


def get_exif_all_data(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(image_filepath)
        #['XMP:DateCreated'][:10].replace(':','-')
    return metadata
    

def capture_one_colorconv(colortagindex):
    capture_one_colortag = ''
    if colortagindex       == 0:
        capture_one_colortag = 'None'
    elif colortagindex     == 1:
        capture_one_colortag = 'Issues-RED'
    elif colortagindex     == 2:    
        capture_one_colortag = 'Special-Blue'
    elif colortagindex     == 3:    
        capture_one_colortag = 'PreSelect-YELLOW'
    elif colortagindex     == 4:
        capture_one_colortag = 'Select-GREEN'
    return capture_one_colortag




#print os.environ


#var="exiftool -if '$jpgfromraw' -b -jpgfromraw -w %d%f_%ue.jpg -execute -if '$previewimage' -b -previewimage -w %d%f_%ue.jpg -execute -tagsfromfile @ -srcfile %d%f_%ue.jpg -overwrite_original -common_args --ext jpg DIR"


#exifcmd = list(var.split(' '))
def extract_preselect_jpg_fr_RAW(rawimgdir,cp1indx):
    import os,sys,subprocess,shutil
    
    #rawimgdir = os.path.abspath(os.path.dirname(rawimgdir))
    outdir = os.path.join(rawimgdir,'../../PRESELECT_OUTPUT')
    try:
        if os.path.isdir(outdir):
            shutil.makedirs(outdir)
    except:
        pass
    if cp1indx >= 3:
        
        subprocess.call([
                
                 'exiftool',
                 '-if',
                 '$jpgfromraw',
                 '-b',
                 '-jpgfromraw',
                 '-w',
                 '%d/../../PRESELECT_OUTPUT/%f_%ue.jpg',
                 '-execute',
                 '-if',
                 '$previewimage',
                 '-b',
                 '-previewimage',
                 '-w',
                 '%d/../../PRESELECT_OUTPUT/%f_%ue.jpg',
                 '-execute',
                 '-tagsfromfile',
                 '@',
                 '-srcfile',
                 '%d/../../PRESELECT_OUTPUT/%f_%ue.jpg',
                 '-overwrite_original',
                 '-common_args',
                 '-ext',
                 'CR2',
                 rawimgdir])

######################   
import os,sys,re
# from collections import defaultdict
filepath = os.path.abspath(sys.argv[1])

directory = os.path.dirname(filepath)
filename  = os.path.basename(filepath)

capture1settings="{0}/CaptureOne/Settings50/{1}.cos".format(directory,filename)
    
    
mdata         = get_exif_all_data(filepath)
capture1data  = get_exif_all_data(capture1settings)


#mdata                   = sorted(mdata.items())
#capture1data            = sorted(capture1data.items())
cp1indx                 = capture1data.get('XML:Color_tag_index')
capture_one_colortag    = capture_one_colorconv(cp1indx)
capture_one_rating      = capture1data.get('XML:Rating')

if int(cp1indx) >= 3:
    cp1indx
    extract_preselect_jpg_fr_RAW(filepath)
    print "{1}: {0}\t\n\vRating {2}".format(filepath, capture_one_colortag, capture_one_rating)

