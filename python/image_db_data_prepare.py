#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


def insert_file_gridfs_file7(filepath=None, metadata=None, db_name=None):
    import os
    db, fs = connect_gridfs_mongodb(db_name=db_name)
    try:
        filename = os.path.basename(filepath)
        content_type = {"content_type": 'image/' + filename.split('.')[-1]}
        if not metadata:
            exif_data,iptc_data,xmp_data,custom_data = get_metadata_for_gridfs(filepath)
            metadata['exif'] = exif_data
            metadata['iptc'] = iptc_data
            metadata['xmp']  = xmp_data
            metadata['content-type'] = content_type
        elif not metadata['content-type']:
            metadata['content-type'] = content_type
        print metadata
        with fs.new_file(filename=filename, metadata=metadata) as fp:
            with open(filepath) as filedata:
                fp.write(filedata.read())
        return fp, db
    except AttributeError:
        print 'Failed ', filepath


def make_thumb(fileslist):
	for f in fileslist:
		from PIL import Image
		size = 400, 480
		file, ext = os.path.splitext(f)
		print f
		try:
			im = Image.open(f)
			print im.getbbox()
			print im.getcolors()
			im.thumbnail(size, Image.ANTIALIAS)
			im.save(file + ".thumbnail", "JPEG")
		except:
			print 'failed {0}'.format(f)
			continue

	


# if sys.argv[1]:
#     directory = sys.argv[1]
#     print directory
# else:

if __name__ == '__main__':
    import sys,os
    try:
        directory = sys.argv[1]
        dirfileslist = recursive_dirlist(directory)
        #print dirfileslist
    except IndexError:
        print 'Using Curdir'
        directory = os.path.abspath(os.curdir)
        dirfileslist = recursive_dirlist(directory)
        #print dirfileslist
    

def test():
    import sys,os
    rootdir='/Users/johnb/Dropbox/DEVROOT/mnt/Post_Ready/Retouch_Still'
    os.chdir('/Users/johnb/virtualenvs/GitHub-prodimages/python')
    recursive_dirlist = recursive_dirlist(rootdir)
    print recursive_dirlist
    return recursive_dirlist


#thumbs = makethumb(dirfileslist)
#thumbs
ret =test()
#print ret
import mongo_gridfs_insert_file
for f in ret:
    mongo_gridfs_insert_file.main(filepath=os.path.abspath(f),metadata=None,db_name=None)