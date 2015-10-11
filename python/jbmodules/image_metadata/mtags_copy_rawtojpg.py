#!/usr/bin/env python
import os, sys, re, csv



def copy_mtags_tofile(infile, dest_file):
    from PIL import Image
    import pyexiv2
    dest_file = dest_file
## Extract Originals Metadata prior to Resizing
    source_metadata = pyexiv2.ImageMetadata(infile)
    source_metadata.read()
# Resize and Save Thumb copy to Zimages
    print infile
    #im = Image.open(infile)
    #im.thumbnail(size, Image.ANTIALIAS)
    #im.save(zimages_filepath , "JPEG")
    #print infile, zimages_filepath
# Copy EXIF data from Source to Resized Image
    dest_metadata = pyexiv2.ImageMetadata(dest_file)
    dest_metadata.read()
    source_metadata.copy(dest_metadata, exif=True, iptc=True, xmp=True, comment=True)
# set EXIF image size info to resized size
#    dest_metadata.read()
#    dest_metadata["Exif.Photo.PixelXDimension"] = im.size[0]
#    dest_metadata["Exif.Photo.PixelYDimension"] = im.size[1]
    dest_metadata.write()
    return dest_file
    
    
    
## Walk Root Directory and Return List or all Files in all Subdirs too
def recursive_dirlist(rootdir):
    import os
    walkedlist = []
    for dirname, subdirnames, filenames in os.walk(rootdir):
        # append path of all filenames to walkedlist
        for filename in filenames:
            file_path = os.path.abspath(os.path.join(dirname, filename))
            if os.path.isfile(file_path):
                walkedlist.append(file_path)
    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    #if '.git' in dirnames:
    # don't go into any .git directories.
    #    dirnames.remove('.git')
    walkedset = list(set(sorted(walkedlist)))
    return walkedset



####
regex = re.compile(r'^/.+?/ON_FIGURE/.+?RAW.*?[0-9]{9}_[1-9]_[0-9]{1,4}\.[jpgJPG]{3}$')

rootdir - sys.argv[1]

dirlist = recursive_dirlist(rootdir)

parsedlist = [ f for f in dirlist if re.findall(regex, f) ]



for f in parsedlist:
    jpg_data = f
    cr2_data = f.replace('.jpg','.CR2')                               
    if os.path.isfile(cr2_data):    
        copy_mtags_tofile(cr2_data, jpg_data)
        print "Success"
    #except:
    #    print "Error{}".format(f