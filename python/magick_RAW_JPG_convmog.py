#!/usr/bin/env python

##    "-gamma",
##    "1.8/1.2/1.6",
def subproc_mogrify_RAWtoJPG5616h(srcdir):
    import subprocess, os, re, sys

#    regex_CR2 = re.compile(r'.+?\.[CR2cr2]')
#    regex_jpg = re.compile(r'.+?\.[JPGjpg]')
#    if re.findall(regex_CR2, file):
    os.chdir(srcdir)

    subprocess.call([
    "mogrify",
    "-define",
    'jpeg:size=3744x5616',
    "-format",
    "jpg",
<<<<<<< HEAD
    "-profile",
=======
    "-profile", 
>>>>>>> e5e9380bad0337a7672eee19d85600c77b1d3f85
    "/usr/local/color_profiles/AdobeRGB1998.icc",
    "-colorspace",
    "sRGB",
    "-type",
    "TrueColor",
<<<<<<< HEAD
    "-depth",
    "16",
    "-density",
    "350x350",
    '*.CR2',
    "-define",
    'jpeg:size=3744x5616',
    "-profile",
    '/usr/local/color_profiles/sRGB.icm',
=======
    "-depth", 
    "16",
    "-density",
    "350x350",
    '*.CR2', 
    "-define",
    'jpeg:size=3744x5616',   
    "-profile",
    '/usr/local/color_profiles/sRGB.icm', 
>>>>>>> e5e9380bad0337a7672eee19d85600c77b1d3f85
    "-colorspace",
    'sRGB',
    "-auto-gamma",
    "-sampling-factor",
    "1x1,1x1,1x1",
    "-density",
    "350x350",
    "-filter",
    "Mitchell",
    "-compress",
    "JPEG",
    "-depth",
    "8",
    "-adaptive-sharpen",
    "10",
    "-quality",
    "100",
    "-unsharp",
    "4.2x3.5+175+0.0",
    ])

import sys
if sys.argv[1]:
    srcdir = sys.argv[1]
else:
    srcdir = '.'

subproc_mogrify_RAWtoJPG5616h(srcdir)
