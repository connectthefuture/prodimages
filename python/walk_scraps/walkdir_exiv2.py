#!/usr/bin/env python

import os,sys
import PIL


def recursive_dirlist(rootdir):
    walkedlist = []
    for dirname, dirnames, filenames in os.walk(rootdir):
        # print path to all subdirectories first.
        #for subdirname in dirnames:
            #print os.path.join(dirname, subdirname)
        # print path to all filenames.
        for filename in filenames:
            file_path = os.path.abspath(os.path.join(dirname, filename))
            if os.path.isfile(file_path):
                walkedlist.append(file_path)
        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
        if '.git' in dirnames:
            # don't go into any .git directories.
            dirnames.remove('.git')
    walkedset = list(set(sorted(walkedlist)))
    return walkedset


def get_exif(filepath):
    ret = {}
    i = Image.open(filepath)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

#######

from PIL import Image
import pyexiv2

#Exif.Photo.DateTimeOriginal

#for k,v in mdata.iteritems():
#    print k,v

rootdir = sys.argv[1]



for line in walkedout:
    file_path = line
    filename = file_path.split('/')[-1]
    colorstyle = filename.split('_')[0]
    alt = file_path.split('_')[-1]
    alt = alt.strip('.jpg')
    photodate = pyexiv2.ImageMetadata(file_path)['DateTimeOriginal']
    print "{0},{1},{2},{3}".format(colorstyle,photodate,file_path,alt)
    
    
def resize_image(source_path, dest_path, size):
    from PIL import *
    import pyexiv2
    # resize image
    image = Image.open(source_path)
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(dest_path, "JPEG")

    # copy EXIF data
    source_image = pyexiv2.Image(source_path)
    source_image.readMetadata()
    dest_image = pyexiv2.Image(dest_path)
    dest_image.readMetadata()
    source_image.copyMetadataTo(dest_image)

    # set EXIF image size info to resized size
    dest_image["Exif.Photo.PixelXDimension"] = image.size[0]
    dest_image["Exif.Photo.PixelYDimension"] = image.size[1]
    dest_image.writeMetadata()