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

    dimensions = ''
    ## Get variable values for processing
    aspect_ratio = get_aspect_ratio(img)
    dimensions = get_dimensions(img)
    width  = dimensions.split('x')[0]
    height = dimensions.split('x')[1]
    
    if aspect_ratio == '1.2':
        vert_horiz = '{0}x{1}'.format(width,height)  
        dimensions = '{0}x{1}'.format(int(width),int(height))
    elif float(aspect_ratio) > float(int(1.2)):
        vert_horiz = 'x{0}'.format(height)
        w = float(0.8) * float(height)
        #w = float(round(w,2)*float(aspect_ratio))
        dimensions = '{0}x{1}'.format(int(w),int(height))
        print "W",w, aspect_ratio
    elif float(aspect_ratio) < float(1.2):
        vert_horiz = '{0}x'.format(width)
        h = float(1.2) * float(width)
        #h = float(round(h,2)*float(aspect_ratio))
        dimensions = '{0}x{1}'.format(int(width),int(h))
        print "H",h, aspect_ratio
    
    if not dimensions:
        dimensions = '100%'
        vert_horiz = '100%'
    outfile = os.path.join(destdir, img.split('/')[-1].split('.')[0] + '.png')
    if os.path.isfile(outfile):
        try:
            os.remove(outfile)
        except:
            pass
    else:
        pass
    subprocess.call([
            'mogrify',
            '-format',
            format,
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
            "-filter",
            "Spline",
            '-filter',
            "Cosine",
            "-colorspace",
            "sRGB",
            '-unsharp',
            '3.9x5.7+0.85+0',
            '-quality', 
            '95'
            ])
    os.rename(img,outfile)
    print 'Done {}'.format(img)
    return os.path.join(destdir, img.split('/')[-1].split('.')[0] + '.png')
    

if __name__ == '__main__':
    
    sharpem_image(img, destdir=None)
    
