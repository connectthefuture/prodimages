# -*- coding: utf-8 -*-
"""
Created on WED JUL 24 11:23:55 2013

@author: jb
"""

def writeXmp(imgfile,xmpkey,xmpvalue):
    import pyexiv2
    metadata = pyexiv2.ImageMetadata(imgfile)
    metadata[xmpkey] = xmpvalue

def writeIptc(imgfile,iptckey,iptcvalue):
    import pyexiv2
    metadata = pyexiv2.ImageMetadata(imgfile)
    metadata[iptckey] = iptcvalue

def writeExif(imgfile,exifkey,exifvalue):
    import pyexiv2
    metadata = pyexiv2.ImageMetadata(imgfile)
    metadata[exifkey] = exifvalue

def readIptc(imgfile):
    import pyexiv2
    metadata = pyexiv2.ImageMetadata(imgfile)
    mdataprint = metadata.read()
    print metadata

###
## Extract All Metadata from Image File as Dict
def get_exif_all(file_path):
    from PIL import Image
    from PIL.ExifTags import TAGS
    exifdata = {}
    im = Image.open(file_path)
    info = im._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        exifdata[decoded] = value
    return exifdata
