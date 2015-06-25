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


def place_watermark_on_image(img, destdir=None, watermark_src=None, dpi=None):
    import subprocess, os

    ext = img.split('.')[-1]
    filename = img.split('/')[-1].split('.')[0]
    os.chdir(os.path.dirname(img))

    ## Define Watermark Image
    if not dpi:
        dpi = '72'

    if not watermark_src:
        watermark = 'img/Bluefly_Logo_Watermark.png'
        ## 'img/Bluefly_Logo_WatermarkSmall.png'
    else:
        watermark = watermark_src

    ## Destination name
    if not destdir:
        destdir = os.path.join(os.path.dirname(img), 'WATERMARKED')
        try:
            os.makedirs(destdir)
        except:
            pass
    else:
        destdir = os.path.abspath(destdir)

    outfile = os.path.abspath(os.path.join(destdir, filename + ext))

    subprocess.call([
        'convert',
        '-format',
        format,
        img,

        ## Adjust Image DPI and Depth of outfile
        '-depth',
        '8',
        "-density",
        dpi,
        "-units",
        "pixelsperinch",

        ## Format and apply Watermark setting to Sequence
        '-fill',
        'grey50',
        '-colorize',
        '40',
        'miff:-',
        '|',
        'composite',
        '-dissolve',
        '15',
        '-tile',
        '-',
        ## Set Colorspace for Web
        "-colorspace",
        "sRGB",
        '-quality',
        '95',
        watermark,
        outfile
    ])

    return outfile



if __name__ == '__main__':
    import sys
    img = sys.argv[1]
    try:
        destdir = sys.argv[2]
    except IndexError:
        destdir = ''

    place_watermark_on_image(img, destdir=destdir)



