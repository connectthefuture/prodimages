#!/usr/bin/env python
import os, sys, re, csv,subprocess

def sharpen_image(img, destdir=None):
    import subprocess,re,os,sys
    regex_coded = re.compile(r'^.+?/[1-9][0-9]{8}_[1-6]\.jpg$')
    regex_alt = re.compile(r'^.+?/[1-9][0-9]{8}_\w+?0[1-6]\.[JjPpNnGg]{3}$')
    regex_valid_style = re.compile(r'^.+?/[1-9][0-9]{8}_?.*?\.[JjPpNnGg]{3}$')

    if not destdir:
        destdir = '.'
    #imgdestpng_out = os.path.join(tmp_processing, os.path.basename(imgsrc_jpg))
    os.chdir(os.path.dirname(img))
    
    
    format = img.split('.')[-1]
    
    os.chdir(os.path.dirname(img))

    ## Destination name
    if not destdir:
        destdir = os.path.abspath('.')
    else:
        destdir = os.path.abspath(destdir)
 
    outfile = os.path.join(destdir, img.split('/')[-1].split('.')[0] + '.png')
    
    subprocess.call([
            'mogrify',
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
            
       
            '-adaptive-sharpen',
            '33',
            '-unsharp',
            '1.5x0.85+.80+0.0096',
            "-colorspace",
            "sRGB",
            '-quality', 
            '95'
            ])
    #os.rename(img,outfile)
    print 'Done {}'.format(img)
    return os.path.join(destdir, img.split('/')[-1].split('.')[0] + '.png')
    

if __name__ == '__main__':
    
    sharpen_image(img, destdir=None)
    
