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
    walkedset = list(set(sorted(walkedlist)))
    return walkedset


def get_exif_all_data(image_filepath):
    import exiftool
    metadata = {}
    with exiftool.ExifTool() as et:
        try:
            metadata = et.get_metadata(image_filepath)#['XMP:DateCreated'][:10].replace(':','-')
        except ValueError:
            pass
    return metadata


def md5_checksummer(filepath):
    import __builtin__, hashlib
    try:
        _file = __builtin__.open(filepath, "rb")
        content = _file.read()
        _file.close()
        md5 = hashlib.md5(content)
        _hash = md5.hexdigest()
        return { "md5": _hash }
    except:
        pass

## Returns False if file is Zero KB, True if file is valid - does not catch corrupt files greater than 1KB
def zero_byte_file_filter(image_filepath,error_dir=None):
    import os, shutil
    if not error_dir:
        imagedir  = os.path.dirname(image_filepath)
        rootdir   = os.path.dirname(imagedir)
        error_root = os.path.join(rootdir,'zero_byte_errors')
        error_details_drop_dir = os.path.join(error_root, 'originated_in_' + imagedir.split('/')[-1])
    mdata = get_exif_all_data(os.path.abspath(image_filepath))
    if mdata.get('File:FileSize') <= 1:
        try:
            os.makedirs(error_details_drop_dir, 16877)
        except:
            pass
        error_file_stored = os.path.join(error_details_drop_dir, os.path.basename(image_filepath))
        if os.path.isfile(error_file_stored):
            os.remove(error_file_stored)
            shutil.move(image_filepath, error_file_stored)
        else:
            shutil.move(image_filepath, error_file_stored)
        return False
    else:
        return True


def getparse_metadata_from_imagefile(image_filepath):
    import os, re
    from collections import defaultdict
    print 'mongo Prep ', image_filepath
    #image_filepath = os.path.abspath(image_filepath)
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


###
### Actually Updates Mongo
def update_filerecord_pymongo(db_name=None, collection_name=None, filename=None, filepath=None, metadata=None, colorstyle=None, alt=None, format=None, timestamp=None, **kwargs):
    import pymongo, bson
    from bson import Binary, Code
    from bson.json_util import dumps
    import datetime
    import mongo_gridfs_insert_file
    mongo_db, fs = mongo_gridfs_insert_file.connect_gridfs_mongodb(db_name=db_name)
    if fs:
        collection_name = 'fs.files'
        if not alt:
            alt = '1'

    tmpfilename          = str(filepath.split('/')[-1])
    colorstyle           = str(tmpfilename[:9])
    image_number         = str(tmpfilename.split('.')[-2][-1])
    alt                  = image_number
    if not kwargs.get('content_type'):
        content_type  = str(tmpfilename.split('.')[-1]).lower().replace('jpg', 'jpeg')
    else:
        content_type = kwargs.get('content_type')
    if not timestamp:
        timestamp = datetime.datetime.now()

    mongo_collection = mongo_db[collection_name]
    md5 = md5_checksummer(filepath)
    key = {'md5': md5}  #, 'alt': alt, 'upload_ct': 1}
    # data = { "$set":{'format': format,'metadata': metadata,'alt': alt, upload_ct: 1,'timestamp': timestamp}},
    datarow = {'colorstyle': colorstyle, 'format': format,'metadata': metadata,'alt': alt, 'upload_ct': "1",'timestamp': timestamp}
    key_str = key.keys()[0]
    restest = mongo_collection.distinct({key_str: md5})
    #print ' distinct Res Test --> ', restest
    check = mongo_collection.find({key_str: md5}).count()
    #check = mongo_collection.find({key_str: tmpfilename}).count()
    if check:
        
        data = { "$set":{
                        "colorstyle": colorstyle,
                        "alt": {"$min": {"alt": alt}},
                        "format": format,
                        "metadata": metadata,
                        "content_type": content_type,
                        #"upload_ct":
                        "$inc": {"upload_ct": "1"},
                        #"$inc": {"upload_ct": int(1)},
                        "timestamp": { "$max": {"timestamp": timestamp}}
                        }
                    }
        print 'REFRESH IT ', check, data
        return check, data

    else:

        data = { "$set":{'colorstyle': colorstyle, 'format': format, 'metadata': metadata, 'alt': alt, "$setOnInsert": {"upload_ct": 1},'timestamp': timestamp}}
        print 'NEW ', check, data
        # mongo_collection.ensure_index([("md5", pymongo.ASCENDING)], unique=True, sparse=True, background=True)
    try:
        mongo_collection.ensure_index(key_str, unique=True, background=True)
    except pymongo.errors.DuplicateKeyError:
        print ' DuplicateKey Error', key_str
        pass
    mongo_collection.create_index([("colorstyle", pymongo.DECENDING),("md5", pymongo.ASCENDING)], background=True)

    upsertobjid = mongo_collection.findAndModify(key, data, multi=True, safe=True, new=True)
    #upsertobjid = mongo_collection.update(key, data, upsert=True, multi=True, safe=True)
    print "Inserted: {0}\nImageNumber: {1}\nFormat: {2}\nID: {3}\nCheck: {4}".format(colorstyle,alt, format, upsertobjid, check)
    return check, upsertobjid


def update_file_gridfs(filepath=None, metadata=None, db_name=None, **kwargs):
    import os, mongo_gridfs_insert_file
    db, fs = mongo_gridfs_insert_file.connect_gridfs_mongodb(db_name=db_name)
    try:
        filename = os.path.basename(filepath)
        ext = filename.split('.')[-1].lower()
        if not kwargs.get('content_type'):
            if ext == 'jpg' or ext == 'jpeg':
                content_type = 'image/jpeg'
            elif ext == 'tif' or ext == 'tiff':
                content_type= 'image/tiff'
            else:
                content_type= 'image/' + str(ext)
        else:
            content_type = kwargs.get('content_type')
        md5 = md5_checksummer(filepath)
        if not mongo_gridfs_insert_file.find_record_gridfs(key={'md5': md5}, db_name=db_name, collection_name='fs.files'):
            try:
                ## Actually do an insert to gridfs instead
                with fs.new_file(filename=filename, content_type=content_type, metadata=metadata) as fp:
                    with open(filepath) as filedata:
                        fp.write(filedata.read())
                return fp, db
            except IOError:
                print ' IO ERROR '
                return False, False
        else:
            # = mongo_gridfs_insert_file.find_record_gridfs(key={"filename": filename}, db_name=db_name, collection_name='fs.files')
            check, res = update_filerecord_pymongo(filepath=filepath,metadata=metadata,db_name=db_name, content_type=content_type)
            return check, res
    except OSError:
        print 'Failed ', filepath


def update_gridfs_extract_metadata(image_filepath,**kwargs):
    import os,sys
    try:
        db_name = kwargs.get('db_name')
        if not db_name:
            db_name = sys.argv[2]
    except UnboundLocalError:
        db_name='gridfs_file7'
    except IndexError:
        db_name='gridfs_file7'
    #print ' is file --> ', image_filepath, db_name

    if kwargs.get('image_url'):
        image_url = kwargs.get('image_url')
    else:
        image_url = ''

    if os.path.isfile(image_filepath):
        metadata = getparse_metadata_from_imagefile(image_filepath).items()[0][1]
        metadata['image_url'] = image_url
    else:
        if not kwargs.get('metadata'):
            metadata = {}
            metadata['ERROR_PATH'] = image_filepath
            metadata['ERROR_URL']  = image_url
        else:
            metadata = kwargs.get('metadata')
            metadata['ERROR_PATH'] = image_filepath
            metadata['ERROR_URL'] = image_url

    checked_ct, update_record = update_file_gridfs(filepath=image_filepath, metadata=metadata, db_name=db_name)
    if checked_ct is False:
        return False, image_filepath
    elif str(checked_ct).isdigit():
        return checked_ct, image_filepath


if __name__ == '__main__':
    import sys,os
    try:
        directory = sys.argv[1]
        dirfileslist = recursive_dirlist(directory)
        for f in dirfileslist:
            update_gridfs_extract_metadata(f)
        #print dirfileslist
    except IndexError:
        print 'FAILED INDEX ERROR'
        pass


