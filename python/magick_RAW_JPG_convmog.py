#!/usr/bin/env python

##    "-gamma",
##    "1.8/1.2/1.6",

### Coefficients a,b,c from Lensfun for EF 24-105mm f/4: IS USM
coefficients =  [{'focal': 24,  'a': 0.017263,  'b': -0.049244,  'c': 0},
                 {'focal': 28,  'a': 0.010878,  'b': -0.024454,  'c': 0},
                 {'focal': 35,  'a': 0.007152,  'b': -0.009799,  'c': 0},
                 {'focal': 50,  'a': 0.002502,  'b': 0.004803,  'c': 0},
                 {'focal': 70,  'a': 0,  'b': 0.009685,  'c': 0},
                 {'focal': 88,  'a': 0,  'b': 0.008781,  'c': 0},
                 {'focal': 105, 'a': 0,  'b': 0.009598,  'c': 0},]


def test_return_coefficients(focallength,coefficients):
    foundce = {}
    for item in coefficients:
        if item['focal'] == focallength:
            tmp_found = {}
            tmp_found['a'] = item['a']
            tmp_found['b'] = item['a']
            tmp_found['c'] = item['a']
            tmp_found['d'] = 1 - item['a'] - item['b'] - item['c']
            foundce[item['focal']] = tmp_found
    return foundce


def subproc_identify_focallength(filepath,coefficients):
    import subprocess, os, re, sys
    focallength = subprocess.call([
    "identify",
    "-format",
    '""%[EXIF:FocalLength]""',
    filepath,
    ])
    return filepath

    
def subproc_convert_rawtojpg(filepath,coefficients):
    import subprocess, os, re, sys
    dngcmd = str("dng:" + filepath)
    outfile = filepath.replace('.CR2','.jpg')
    barrelparams = 
    subprocess.call([
    "convert",
    "-define",
    'dng:size=3744x',
    "-define",
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
    '',
    '',
    "-format",
    "jpg",
    "-unsharp", 
    "0x0.75+0.75+0.008",
    outfile,
    ])
    return outfile
    


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