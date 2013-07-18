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
    return walkedlist


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

Exif.Photo.DateTimeOriginal

for k,v in mdata.iteritems():
    print k,v

rootdir = sys.argv[1]



for line in walkedout:
    file_path = line
    filename = file_path.split('/')[-1]
    colorstyle = filename.split('_')[0]
    alt = file_path.split('_')[-1]
    alt = alt.strip('.jpg')
    print "{0},{1},{2},{3}".format(colorstyle,alt,file_path,alt)
    
    
 