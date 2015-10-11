# -*- coding: utf-8 -*-
"""
Created on WED JUL 24 11:23:55 2013

@author: jb
"""
###
## Make Lowres Thumnails from Image files or Directory Full of Image Files
def make_lowres_thumbnails_dir_or_singlefile(pathname):
    from PIL import Image
    import glob, os, re
    size = 600, 720
    regex_jpeg = re.compile(r'.+?\.[jpgJPG]{3}$')
#    regex_jpeg_colorstyle = re.compile(r'.+?[0-9]{9}_[1-6][.jpg|.JPG]$')

    if re.findall(regex_jpeg, pathname):
    ## If input variable is a single File Create 1 Thumb
        if os.path.isfile(pathname):
            try:
                infile = os.path.abspath(pathname)
                filename, ext = os.path.splitext(infile)
                im = Image.open(infile)
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(filename , "JPEG")
            except:
                print "Error Creating Single File Thumbnail for {0}".format(infile)
    ## If input variable is a Directory Decend into Dir and Crate Thumnails for all jpgs
        elif os.path.isdir(pathname):
            dirname = os.path.abspath(pathname)
            for infile in glob.glob(os.path.join(dirname, "*.jpg")):
                try:
                    filename, ext = os.path.splitext(infile)
                    im = Image.open(infile)
                    im.thumbnail(size, Image.ANTIALIAS)
                    im.save(filename, "JPEG")
                except:
                    print "Error Creating Thumbnail for {0}".format(infile)
