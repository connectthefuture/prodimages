#!/usr/bin/env python

def subproc_mogrify_RAWtoJPG4800h(srcdir):
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
    "8",
    "-density",
    "350x350",
    "-profile", 
    "/usr/local/color_profiles/sRGB.icm",
    "-colorspace",
    "sRGB",
    '*.CR2',
#        "-resample",
#        outsize,
    "-define",
    'jpg:size=x4800', 
    "-define",
    'jpg:profile=/usr/local/color_profiles/sRGB.icm', 
    "-define",
    'jpg:colorspace=sRGB',
    "-density",
    "350x350",
    "-level",
    "0\%,100\%,1.3",
    "-adaptive-sharpen",
    "30",
    "-unsharp",
    "70",
    "-quality",
    "100",
    ])

import sys
if sys.argv[1]:
    srcdir = sys.argv[1]
else:
    srcdir = '.'
    
subproc_mogrify_RAWtoJPG4800h(srcdir)

