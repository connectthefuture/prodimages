#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_dimensions(img):
    from PIL import Image
    try:
        im = Image.open(img)
        w,h = im.size
        dimensions = "{0}x{1}".format(int(w),int(h))
        return dimensions
    except IOError:
        pass

def get_aspect_ratio(img):
    from PIL import Image
    try:
        im = Image.open(img)
        w,h = im.size
        aspect_ratio = str(round(float(int(h))/float(int(w)),2))
        return aspect_ratio
    except IOError:
        pass

def get_color_profile_mode(img):
    from PIL import Image
    try:
        im = Image.open(img)
        color_profile_mode = im.mode
        return color_profile_mode
    except IOError:
        pass

def get_color_profile_name(img):
    import exiftool
    try:
        exif=exiftool.ExifTool()
        exif.start()
        mdata=exif.get_metadata(img)
        exif.terminate()
        color_profile_name = mdata['XMP:ICCProfileName']
        return color_profile_name
    except IOError:
        pass

################################## COLOR PROFILE CONVERSIONS #####################

def convert_colorprofile(image_file,inprofile,outprofile):
    import subprocess
    format = image_file.split('.')[-1]
    subprocess.call([
                    'convert',
                    image_file,
                    '-format',
                    format,
                    '-profile', 
                    inprofile,
                    '+repage',
                    '-profile',
                    outprofile,
                    "+repage",
                    '-colorspace',
                    'sRGB',
                    str(os.path.abspath(image_file))
                    ])
    return
################################ RUN #############################################
## CMYK Profile Files
cmyk_uswebcoat='/usr/local/color_profiles/USWebCoatedSWOP.icc'
cmyk_ussheetfedcoat='/usr/local/color_profiles/USSheetfedCoated.icc'
cmyk_jpn01coat='/usr/local/color_profiles/JapanColor2001Coated.icc'
cmyk_FOGRA39coat='/usr/local/color_profiles/CoatedFOGRA39.icc'
cmyk_FOGRA27coat='/usr/local/color_profiles/CoatedFOGRA27.icc'

## RGB Profile Files
adobe98='/usr/local/color_profiles/AdobeRGB1998.icc'
srgb_webrdy='/usr/local/color_profiles/sRGB.icm'

import sys,os

def main(image_file=None,inprofile=None,outprofile=None):
    if not image_file:
        image_file = sys.argv[1]
    image_file = os.path.abspath(image_file)

    if not outprofile:
        outprofile = srgb_webrdy

    inmode = get_color_profile_mode(image_file).lower()

    if inmode == 'cmyk' and not inprofile:
        inprofile = cmyk_ussheetfedcoat
        #elif inmode == 'rgb' and not inprofile:
        #    inprofile  = srgb_webrdy
        #elif not inprofile:
        #    inprofile  = srgb_webrdy
        
        ret = convert_colorprofile(image_file,inprofile,outprofile)
        # print image_file, inmode, inprofile, outprofile
    #return ret


if __name__ == '__main__':
    main()