#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Walk Root Directory and Return List or all Files in all Subdirs too
def recursive_dirlist(rootdir):
    import os,re
    regex_bflyfile = re.compile(r'^(.*?/?)?.*?([0-9]{9})((_[1-7xX])|(_alt0[1-6]))?(\.[jpngJPNG]{3,4})?$')
    walkedlist = []
    for dirname, subdirnames, filenames in os.walk(rootdir):
        # append path of all filenames to walkedlist
        for filename in filenames:
            file_path = os.path.abspath(os.path.join(dirname, filename))
            if os.path.isfile(file_path) and regex_bflyfile.findall(file_path):
                walkedlist.append(file_path)
    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    #if '.git' in dirnames:
    # don't go into any .git directories.
    #    dirnames.remove('.git')
    return walkedlist


def get_exif_all_data(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(image_filepath)#['XMP:DateCreated'][:10].replace(':','-')
    return metadata


def getparse_metadata_from_imagefile(image_filepath):
    import os, re
    from collections import defaultdict
    image_filepath = os.path.abspath(image_filepath)
    mdata = get_exif_all_data(image_filepath)
    mdatainsert = {} #defaultdict(list)
    groupdict = defaultdict(list)
    for k,v in mdata.iteritems():
        try:
            mgroup, mtag = k.split(':')
            mvalue = v
            metakvpairs = {mtag: mvalue}
            groupdict[mgroup].append(metakvpairs)
            #print mgroup, mtag, mvalue, '----_----', metagroupdict, '----\n----',groupdict
            #metagroupdict[mgroup].append(metatagval)
        except ValueError:
            pass
    #print groupdict  datagroupkey, datagroupvalues = groupdict.popitem()
    mdatainsert[image_filepath] = groupdict #.items()
    return mdatainsert


def insert_gridfs_extract_metadata(image_filepath):    
    from mongo_gridfs_insert_file import insert_file_gridfs_file7
    metadata = getparse_metadata_from_imagefile(image_filepath).items()[0][1]
    print image_filepath, metadata
    insert_record = insert_file_gridfs_file7(filepath=image_filepath, metadata=metadata, db_name='gridfs_file7')
    return #insert_record


if __name__ == '__main__':
    import sys,os
    try:
        directory = sys.argv[1]
        dirfileslist = recursive_dirlist(directory)
        for f in dirfileslist:
            insert_gridfs_extract_metadata(f)
        #print dirfileslist
    except IndexError:
        print 'FAILED INDEX ERROR'
        pass


