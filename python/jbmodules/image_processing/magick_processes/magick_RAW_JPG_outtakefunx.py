#!/usr/bin/env python
import os, sys, re, csv












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



def subproc_mogrify_RAWtoJPG5616h(srcdir):
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