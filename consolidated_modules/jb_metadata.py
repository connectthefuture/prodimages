# -*- coding: utf-8 -*-
"""
Created on WED JUL 24 11:23:55 2013

@author: jb
"""

<<<<<<< HEAD
=======
##### PIL - Less Complete Metadata Ops

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


            #######  Glob or Reg Search Dir for CSV output as filename(ie.style), photo_date(ie.createdate), file_location(url or filepath)
###
def csv_read_exiftags(list_or_glob):
    ret = {}
    from PIL import Image
    from PIL.ExifTags import TAGS
    for f in list_or_glob:
        i = Image.open(f)
        info = i._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
    return ret


##
##### Pyexiv2 -- Much better Metadata Ops -- Use these if possible
##
def embed_exif_metadata(image_filepath, exiftag=None, exifvalue=None):
    from PIL import Image
    import pyexiv2
    # Read EXIF data to initialize
    image_metadata = pyexiv2.ImageMetadata(image_filepath)
    image_metadata.read()
    # Add and Write new Tag to File
    image_metadata[exiftag] = exifvalue
    image_metadata.write()
    return image_filepath


def get_exif_metadata_value(image_filepath, exiftag=None, exifvalue=None):
    from PIL import Image
    import pyexiv2
    if exifvalue:
        pass
    else:

        # Read EXIF data to initialize
        image_metadata = pyexiv2.ImageMetadata(image_filepath)
        metadata = image_metadata.read()
        # Add and Write new Tag to File
        exifvalue = metadata[exiftag]
        # image_metadata[exiftag] = exifvalue
        # image_metadata.write()
#    else:
#        print "Not Yet Built"
    return image_filepath

####
def write_metadata_file(filename):
    import sys
    import os
    import glob
    import sqlalchemy
    metadict = get_dbinfo_for_metatags_singlefile(filename)
    exiftags = []
    exifdict = {}
    for k,v in metadict.items():
        metatags = []
        for val in v:
            #m = []
            filename = str(k)
            exiftag = val
            exifvalue = v[val]
            #exifpart = str(' -' + "'" + str(exiftag) + "=" + str(exifvalue) + "'" + ''),
            exifpart = "-'{exiftag}'='{exifvalue}'".format(exiftag=exiftag,exifvalue=exifvalue)
            metatags.append(exifpart)
            #print metatags
            #m.append(exifpart)
            #print val,v[val]
        #exifdict[filename] = [x for x in metatags]
        #metatags = (str(tag) for tag in metatags)
        exifdict[filename] = " ".join(metatags)

        execlist = []
        for key,value in exifdict.iteritems():
            execstring = "exiftool -m -overwrite_original_in_place -fast2 -q {0} {1}".format(value,key)
            execlist.append(execstring)

        for line in execlist:
            try:
                os.system(line)
                print line
            except:
                pass


>>>>>>> 00d5c280c263b375d191833004cfc6cf50e480b0
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
<<<<<<< HEAD
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
=======
#####################
###  END SECTION  ###
###########################################################################################################################################################
>>>>>>> 00d5c280c263b375d191833004cfc6cf50e480b0
