#!/usr/bin/env python

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


def place_watermark_on_image(img, destdir='', watermark='', dpi='', opacity='', wmarktype=''):
    import subprocess, os
    #import pdb;pdb.set_trace()
    ext = img.split('.')[-1]
    filename = img.split('/')[-1].split('.')[0]
    os.chdir(os.path.dirname(img))

    ## Define Watermark Image
    if not watermark:
        # watermark = os.path.join(os.path.dirname(os.path.realpath(__file__)),'img/Bluefly_Logo_Watermark.png')
        #watermark = os.path.join(os.path.dirname(os.path.realpath(__file__)),'img/Bluefly_Logo_Watermark.png')
        watermark =  os.path.join('/usr/local/batchRunScripts/python/jbmodules/image_processing/magick_tweaks/img', 'Bluefly_Logo_Watermark.png' )
        ## 'img/Bluefly_Logo_WatermarkSmall.png'
    else:
        pass

    ## Opacity and type of Watermark
    if not wmarktype:
        wmarktype = "-tile"

    if not opacity:
        opacity = "5"

    if not dpi:
        dpi = str('40')
    else:
        dpi = str(dpi)

    ## Destination name
    if not destdir:
        destdir = os.path.join(os.path.dirname(img), 'WATERMARKED')
        try:
            os.makedirs(destdir)
        except:
            print destdir
            pass
    else:
        destdir = os.path.abspath(destdir)

    outfileWmark = os.path.abspath(os.path.join(destdir, filename + '_smplmark.' + ext))
    outfileLres = os.path.abspath(os.path.join(destdir, filename + '_smpl.' + ext))

    if len(sys.argv) >= 3:
        subprocess.call([
            "composite",
            "-dissolve",
            "55",
            "-format",
            ext,
            img,
            ## Set Colorspace for Web
            "-depth",
            "8",
            "-density",
            dpi,
            "-units",
            "pixelsperinch",
            "-colorspace",
            "sRGB",
            "-quality",
            "95",
            "-tile",
            "-strip",
            unicode(watermark),
            unicode(outfileWmark)
        ])

    subprocess.call([
            "convert",
            "-format",
            ext,
            img,
            ## Set Colorspace for Web
            "-depth",
            "8",
            "-density",
            dpi,
            "-units",
            "pixelsperinch",
            "-colorspace",
            "sRGB",
            "-format",
            "jpeg",
            "-quality",
            "55",
            "-resize",
            "x600",
            "-strip",
            unicode(outfileLres.replace('.png','.jpg'))
        ])

#    cmd1 = ("convert", "-format", unicode(ext), unicode(img), "-depth", "8", "-density", unicode(dpi), "-units", "pixelsperinch", "-fill", "grey50", "-colorize", "40", "miff:-")
#    cmd2 = ("composite", "-dissolve", unicode(opacity), unicode(wmarktype), "-", "-colorspace", "sRGB", "-quality", "95", unicode(watermark), unicode(outfile))
#
#    #args1 = shlex.split(cmd1)
#    #args2 = shlex.split(cmd2)
#    print ' '.join((cmd1 + cmd2))
#    ps = subprocess.Popen(cmd1, stdout=subprocess.PIPE, bufsize=-1, shell=True)
#    output = subprocess.check_output(cmd2, stdin=ps.stdout, bufsize=-1, shell=True)
#    ps.wait()

    return outfileWmark


if __name__ == '__main__':
    import sys, os
    arg1 = os.path.abspath(sys.argv[1])
    
    try:
        destdir = sys.argv[2]
    except IndexError:
        if os.path.isdir(arg1):
            destdir = arg1
        else:
            destdir = os.path.dirname(arg1)
    
    if os.path.isdir(arg1):
        import glob
        for i in glob.glob(os.path.join(arg1,'*.??g')):
            place_watermark_on_image(i, destdir=destdir)
    else:
        place_watermark_on_image(arg1, destdir=destdir)
    
