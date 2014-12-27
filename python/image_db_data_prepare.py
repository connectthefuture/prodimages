#!/usr/bin/env python
# -*- coding: utf-8 -*-


def raw_bfly_url_parser(url):
    import re
    regex_url  = re.compile(r'^(?:.+?\.ms\?\w+=)(?P<colorstyle>[1-9][0-9]{8})(?:.*?)?&(?:.*?)?(?:(?:w=)|(?:width=)|(?:outputx=))?(?P<width>\d+)?(?:(?:&h=)|(?:&height=)|(?:&outputy=))?(?P<height>\d+)?(?:.*?)?((?:&ver=)(?P<version>\d+))?(?:&level=\d)?$', re.U)
    ## Clear Local image servers first
    kvpairs = []
    try:
        matched    = regex_url.match(url_purge)
        colorstyle = matched.group('colorstyle')
        version    = matched.group('version')
        width      = matched.group('width')
        height     = matched.group('height')
        pair = ((colorstyle, version),(width,height))
        kvpairs.append(pair)
        return kvpairs
    except:
        print 'FAILED', url
        pass

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


def get_PNG_datecreate(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        datecreated = et.get_metadata(image_filepath)['PNG:datecreate'][:10]
    return datecreated


def get_exif_all_data(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(image_filepath)#['XMP:DateCreated'][:10].replace(':','-')
    return metadata


def get_metadata_for_gridfs(image_filepath):
    metadata = get_exif_all_data(image_filepath)
    exif_data    = metadata['exif'] 
    iptc_data    = metadata['iptc'] 
    xmp_data     = metadata['xmp'] 
    content_type = metadata['content-type']
    return


def getparse_metadata_from_imagefile(image_filepath):
    import os, re
    #mongo_gridfs_insert_file.main(filepath=os.path.abspath(f),metadata=None,db_name=None)
    image_filepath = os.path.abspath(image_filepath)
    mdata = get_exif_all_data(image_filepath)
    from collections import defaultdict
    mdatainsert = defaultdict(list)
    for d in mdata.items():
        metadict = {} #defaultdict(list)
        try:
            #print d[1]
            mgroup, mtag = d[0].split(':')
            mvalue = d[1]
            metadict['metagroup'] = mgroup
            metadict['metatag']   = mtag
            metadict['metavalue'] = mvalue
            mdatainsert[image_filepath].append(metadict)
        except ValueError:
            pass
    #mdatainsert[image_filepath] = metadict
    return mdatainsert.keys()[0], mdatainsert.values()[0]


def insert_gridfs_extract_metadata(filename):    
    from mongo_gridfs_insert_file import insert_file_gridfs_file7
    image_filepath, metadata = getparse_metadata_from_imagefile(filename)
    print image_filepath, metadata
    insert_record = insert_file_gridfs_file7(filepath=image_filepath, metadata=metadata, db_name='gridfs_file7')
    return insert_record


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
        #directory = os.path.abspath(os.curdir)
        #dirfileslist = recursive_dirlist(directory)
        #print dirfileslist
    

def test():
    import sys,os
    rootdir='/Users/johnb/Dropbox/DEVROOT/mnt/Post_Ready/Retouch_Still'
    os.chdir('/Users/johnb/virtualenvs/GitHub-prodimages/python')
    dirfileslist = recursive_dirlist(rootdir)
    #print dirfileslist
    return dirfileslist


#thumbs = makethumb(dirfileslist)
#thumbs
#ret =test()
#print ret



