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
    "-depth", 
    "16",
    "-density",
    "350x350",
    "-profile", 
    "/usr/local/color_profiles/sRGB.icm",
    "-colorspace",
    "sRGB",
    '*.CR2', 
    "-define",
    'jpeg:size=3744x5616',   
    "-define",
    'jpeg:profile=/usr/local/color_profiles/sRGB.icm', 
    "-define",
    'jpeg:colorspace=sRGB',
    "-sampling-factor",
    "1x1,1x1,1x1",
    "-define",
    "jpeg:density=350x350",
    "-compression",
    "none",
    "-depth", 
    "8",
    "-adaptive-sharpen",
    "20",
    "-quality",
    "100",
    "-auto-gamma",
    "-unsharp",
    "4.2x3.5+175+0.0",
    ])

import sys
if sys.argv[1]:
    srcdir = sys.argv[1]
else:
    srcdir = '.'
    
subproc_mogrify_RAWtoJPG4800h(srcdir)

