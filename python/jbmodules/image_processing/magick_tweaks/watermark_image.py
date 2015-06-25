#!/usr/bin/env python
import os, sys, re, csv,subprocess

import re
regex_coded = re.compile(r'^.+?/[1-9][0-9]{8}_[1-6]\.jpg$')
regex_alt = re.compile(r'^.+?/[1-9][0-9]{8}_\w+?0[1-6]\.[JjPpNnGg]{3}$')
regex_valid_style = re.compile(r'^.+?/[1-9][0-9]{8}_?.*?\.[JjPpNnGg]{3}$')


def replace_alpha_withbg(img):
    import subprocess
    ext = img.split('.')[-1]
    imgout = img.replace('.' + ext,'_bg.' + ext)
    subprocess.call([
    'convert',
    img,
    '-alpha',
    'transparent',
    '-alpha',
    'opaque',
    '-strip',
    imgout
    ])
    return imgout


def place_watermark_on_image(img, destdir=None, watermark_src=None):
    import subprocess, os

    ext = img.split('.')[-1]
    filename = img.split('/')[-1].split('.')[0]
    os.chdir(os.path.dirname(img))

    ## Define Watermark Image
    if not watermark_src:
        watermark = 'img/Bluefly_Logo_Watermark.png'
        ## 'img/Bluefly_Logo_WatermarkSmall.png'
    else:
        watermark = watermark_src

    ## Destination name
    if not destdir:
        destdir = os.path.dirname(img)
    else:
        destdir = os.path.abspath(destdir)

    outfile = os.path.join(destdir, filename + ext)

    subprocess.call([
    'convert',
    '-format',
    format,
    img,
    '-depth',
    '8',

    ## Adjust Image DPI
    "-density",
    dpi,
    "-units",
    "pixelsperinch",


    "-colorspace",
    "sRGB",
    '-quality',
    '95',
    os.path.abspath(img)
    ])



def sharpen_image(img, destdir=None):
    import subprocess,os

    if not destdir:
        destdir = os.path.dirname(img)
    #imgdestpng_out = os.path.join(tmp_processing, os.path.basename(imgsrc_jpg))
    os.chdir(os.path.dirname(img))

    format = img.split('.')[-1]

    os.chdir(os.path.dirname(img))

    ## Destination name
    if not destdir:
        destdir = os.path.dirname(img)
    else:
        destdir = os.path.abspath(destdir)

    outfile = os.path.join(destdir, img.split('/')[-1].split('.')[0] + '.png')

    subprocess.call([
            'convert',
            '-format',
            format,
             "-colorspace",
             "LAB",
            img,
            '-define',
            'png:preserve-colormap',
            '-define',
            'png:format\=png24',
            '-define',
            'png:compression-level\=N',
            '-define',
            'png:compression-strategy\=N',
            '-define',
            'png:compression-filter\=N',
            '-format',
            'png',
#            "-filter",
#            "Spline",



            '-unsharp',
            "-1x1.2+0.50+0.0087",
            "-colorspace",
            "sRGB",
            '-quality',
            '95',
            os.path.abspath(img)
            ])
    #os.rename(img,outfile)
    print 'Done {}'.format(img)
    return os.path.join(destdir, img.split('/')[-1].split('.')[0] + '.png')


if __name__ == '__main__':
    import sys
    img = sys.argv[1]
    sharpen_image(img, destdir=None)



