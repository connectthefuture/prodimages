#!/usr/bin/env python

def subproc_mogrify_RAWtoJPG5616h(srcdir):
    import subprocess, os, re, sys

#    regex_CR2 = re.compile(r'.+?\.[CR2cr2]')
#    regex_jpg = re.compile(r'.+?\.[JPGjpg]')
#    if re.findall(regex_CR2, file):
    os.chdir(srcdir)

    subprocess.call([
    "mogrify",
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
    "-define",
    'rgb:size=3744x5616', 
    '*.CR2', 
    "-define",
    'jpeg:size=3744x5616',   
    "-define",
    'jpeg:profile=/usr/local/color_profiles/sRGB.icm', 
    "-depth", 
    "16",
    "-define",
    'jpeg:colorspace=sRGB',
    "-define",
    'jpeg:fancy-upsampling=on',
    "-define",
    "jpeg:density=350x350",
    "-auto-gamma",
#    "-level",
#    "0\%,100\%,1.3",
    "-adaptive-sharpen",
    "20",
    "-unsharp",
    "80",
    "-quality",
    "100",
    ])

import sys
if sys.argv[1]:
    srcdir = sys.argv[1]
else:
    srcdir = '.'
    
subproc_mogrify_RAWtoJPG4800h(srcdir)

