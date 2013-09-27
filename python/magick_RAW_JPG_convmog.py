#!/usr/bin/env python
import os, re, sys
##    "-gamma",
##    "1.8/1.2/1.6",
try:
    filepath = sys.argv[1]
except:
    pass

### Coefficients a,b,c from Lensfun for EF 24-105mm f/4: IS USM
coefficients =  [{'focal': 24,  'a': 0.017263,  'b': -0.049244,  'c': 0},
                 {'focal': 28,  'a': 0.010878,  'b': -0.024454,  'c': 0},
                 {'focal': 35,  'a': 0.007152,  'b': -0.009799,  'c': 0},
                 {'focal': 50,  'a': 0.002502,  'b': 0.004803,  'c': 0},
                 {'focal': 70,  'a': 0,  'b': 0.009685,  'c': 0},
                 {'focal': 88,  'a': 0,  'b': 0.008781,  'c': 0},
                 {'focal': 105, 'a': 0,  'b': 0.009598,  'c': 0},]


def subproc_identify_focallength(filepath):
    import subprocess, os, re, sys
    focallength = subprocess.call([
    "identify",
    "-format",
    '%[EXIF:FocalLength]',
    filepath,
    ])
    print 
    return str(focallength)


#print "{:.1}".format(focallength.split('/')[0]/focallength.split('/')[1])
#return "{:.1}".format(focallength.split('/')[0]/focallength.split('/')[1])


## Use the focal length from return above function to return the 4 Barrel coefficients    
def test_return_coefficients(focallength=None):
    ### Coefficients a,b,c from Lensfun for EF 24-105mm f/4: IS USM    
    coefficients =  [{'focal': 24,  'a': 0.017263,  'b': -0.049244,  'c': 0},
                     {'focal': 28,  'a': 0.010878,  'b': -0.024454,  'c': 0},
                     {'focal': 35,  'a': 0.007152,  'b': -0.009799,  'c': 0},
                     {'focal': 50,  'a': 0.002502,  'b': 0.004803,  'c': 0},
                     {'focal': 70,  'a': 0,  'b': 0.009685,  'c': 0},
                     {'focal': 88,  'a': 0,  'b': 0.008781,  'c': 0},
                     {'focal': 105, 'a': 0,  'b': 0.009598,  'c': 0},]
    
    if focallength:
        pass
    else: 
        focallength = 88

    foundce = {}
    for item in coefficients:
        if item['focal'] == focallength:
            tmp_found = {}
            tmp_found['a'] = item['a']
            tmp_found['b'] = item['b']
            tmp_found['c'] = item['c']
            tmp_found['d'] = 1 - item['a'] - item['b'] - item['c']
            foundce[item['focal']] = tmp_found
    return foundce



#### Converter
def subproc_convert_rawtojpg(filepath,foundce=None):
    import subprocess, os, re, sys
    dngcmd = str("dng:" + filepath)
    outfile = filepath.replace('.CR2','.jpg')
    
    ## Breakup Barrel Params as individual a,b,c,d values
    if foundce:    
        
        barrelparams = test_return_coefficients(foundce).values()[0]
        a = barrelparams['a']
        b = barrelparams['b']
        c = barrelparams['c']
        d = barrelparams['d']
        BarrelArgs = "Barrel  {0} {1} {2} {3}".format(a,b,c,d)
    else:
        BarrelArgs = 'Barrel 0.0 0.0 -0.025'
    
    subprocess.call([
    "convert",
    "-define",
    'dng:size=3744x',
    dngcmd,
    "-depth", 
    "16",
    "-density",
    "350x350",
    "-profile", 
    "/usr/local/color_profiles/AdobeRGB1998.icc",
    "-colorspace",
    "RGB",
    "-filter",
    "LanczosSharp",
    "-compress",
    "JPEG",
    "-profile",
    '/usr/local/color_profiles/sRGB.icm', 
    "-colorspace",
    'sRGB',
    "-depth", 
    "8",
    "-distort",
    'Barrel 0.0 0.0 -0.025',
    "-unsharp", 
    "0x0.75+0.75+0.008",
    outfile,
    ])
    return outfile
    
################################
#############        RUN
################################
## Get Focallength
#focallength = subproc_identify_focallength(filepath)
#focallength = get_exif_metadata_value(filepath, exiftag='FocalLength')
## Get Barrel Params using identified focal length
#foundce = test_return_coefficients(focallength=88)

## Convert File
subproc_convert_rawtojpg(filepath)

















def subproc_mogrify_RAWtoJPGshort(srcdir):
    import subprocess, os, re, sys

#    regex_CR2 = re.compile(r'.+?\.[CR2cr2]')
#    regex_jpg = re.compile(r'.+?\.[JPGjpg]')
#    if re.findall(regex_CR2, file):
    os.chdir(srcdir)

    subprocess.call([
    "mogrify",
    "-define",
    'dng:size=3744x',
    '',
    '',
    "-format",
    "jpg",
    '*.CR2',
    "-define",
    'jpeg:size=3744x',
    ])

import sys
if sys.argv[1]:
    srcdir = sys.argv[1]
else:
    srcdir = '.'

subproc_mogrify_RAWtoJPG5616h(srcdir)



def subproc_mogrify_RAWtoJPG5616h(srcdir)
    import subprocess, os, re, sys

#    regex_CR2 = re.compile(r'.+?\.[CR2cr2]')
#    regex_jpg = re.compile(r'.+?\.[JPGjpg]')
#    if re.findall(regex_CR2, file)
    os.chdir(srcdir)

    subprocess.call([
    "mogrify",
    "-define",
    'dcraw8size=3744x5616', 
    "-format",
    "jpg",
    "-depth", 
    "16",
    "-density",
    "350x350",
    "-profile", 
    "/usr/local/color_profiles/AdobeRGB1998.icc",
    "-colorspace",
    "RGB",
    '*.CR2', 
    "-define",
    'jpegsize=3744x5616',   
    "-profile",
    '/usr/local/color_profiles/sRGB.icm', 
    "-colorspace",
    'sRGB',
    "-sampling-factor",
    "1x1,1x1,1x1",
    "-density",
    "350x350",
    "-filter",
    "LanczosSharp",
    "-compress",
    "JPEG",
    "-depth", 
    "16",
    "-resample",
    "-adaptive-sharpen",
    "10",
    "-quality",
    "100",
    "-auto-gamma",
    "-unsharp",
    "4.2x3.5+175+0.0",
    ])