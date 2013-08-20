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
    "-define",
<<<<<<< HEAD
    'jpg:size=3744x5616',     
=======
    'jpg:size=3744x5616', 
>>>>>>> 3f0b8642a320fb73a3e22660ab54b96d15943d85
    "-define",
    'jpg:profile=/usr/local/color_profiles/sRGB.icm', 
    "-define",
    'jpg:colorspace=sRGB',
<<<<<<< HEAD
    "-define",
    'jpeg:fancy-upsampling=on',
=======
    "-resample",
>>>>>>> 3f0b8642a320fb73a3e22660ab54b96d15943d85
    "-density",
    "350x350",
    "-auto-gamma",
    "-level",
    "10\%,90\%,1.3",
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

