#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


## Extract All Metadata from Image File as Dict using PIL
def get_exif_pil(file_path):
    from PIL import Image
    from PIL.ExifTags import TAGS
    exifdata = {}
    im = Image.open(file_path)
    info = im._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        exifdata[decoded] = value
    return exifdata

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


###
## Convert Walked Dir List To Lines with path,photo_date,stylenum,alt. Depends on above "get_exif_all_data" function
def walkeddir_parse_to_kvdict(filepaths_listdict):
    import re,os
    #regex = re.compile(r'.*?[0-9]{9}_[1-6]\.[jpngJPNG]{3}$')
    regex = re.compile(r'^(.*?/?)?.*?([0-9]{9})(_alt0[1-6])?(\.[jpngJPNG]{3})?$')
    datarows = []
    datarowsdict = {}
    for filepathpair in filepaths_listdict.items():
        datarowsdict_tmp = {}
        md5checksum = filepathpair[0]
        filepath    = filepathpair[1]
        #print filepath, ' \t',
        #print md5checksum, ' \n'
        #if regex.findall(filepath):
        try:
            filename = filepath.split('/')[-1].split('.')[0]
            colorstyle = filename.split('_')[0]
            alt_ext = filepath.split('_')[-1]
            alt = alt_ext.split('.')[0]
            ext = alt_ext.split('.')[-1]
            try:
                create_dt = get_exif_all_data(filepath)['File:FileModifyDate'][:10]
            except KeyError:
                try:
                    create_dt = get_exif_pil(filepath)['DateTime'][:10]
                except KeyError:
                    try:
                        create_dt = get_exif_pil(filepath)['DateTimeOriginal'][:10]
                    except KeyError:
                        create_dt = '0000-00-00'
            except ValueError:
                    try:
                        create_dt = get_exif_all_data(filepath)['File:FileModifyDate'][:10]
                    except:
                        create_dt = '0000-00-00'
            create_dt = str(create_dt)
            create_dt = create_dt.replace(':','-')
            datarowsdict_tmp['colorstyle'] = colorstyle
            # Increment alt# on files with _alt0# naming to match _1,_2 etc.
            if not alt:
                alt = 1
            elif len(alt) == 1:
                pass
            elif len(alt) > 1 and len(alt) < 7:
                if alt[-1].isdigit():
                    alt = int(alt[-1])
                    alt = alt + 1
                else:
                    alt = 0
            else:
                alt = 0
            datarowsdict_tmp['alt'] = alt
            datarowsdict_tmp['ext'] = ext
            datarowsdict_tmp['filepath'] = filepath
            datarowsdict_tmp['filename'] = filename
            datarowsdict_tmp['md5checksum'] = md5checksum
            datarowsdict_tmp['create_dt'] = create_dt
            datarowsdict[md5checksum] = datarowsdict_tmp
            ## Format CSV Rows
            row = "{0},{1},{2},{3},{4}".format(md5checksum,colorstyle,create_dt,filepath,alt)
            #print row
            #print datarowsdict,
            #print datarowsdict_tmp, ' \n'
            datarows.append(row)
        except IOError:
            print "IOError on {0}".format(filepath)
            #except AttributeError:
            #    print "AttributeError on {0}".format(filepath)
    return datarowsdict


def find_md5_and_dups(files_list, ext=None):
    import hashlib, re
    import os, __builtin__

    hash_table_jpg     = {}
    hash_table_png     = {}
    hash_table_general = {}
    dups               = []

    if type(files_list) == str and os.path.isdir(files_list):
        files_list = os.path.abspath(files_list)
        os.chdir(os.path.abspath(files_list))
        checklist = os.listdir(files_list)
    else:
        checklist = files_list

    #if not ext:
    ## Use basic regex excluding . (dot) files
    regex_notdot = re.compile(r'^.+?\..+?$')
    regex_jpg    = re.compile(r'^.+?\.[jpg]{3}$', re.I)
    regex_png    = re.compile(r'^.+?\.[png]{3}$', re.I)
    #regex_images = re.compile(r'^.+?\.[jpngsdtif]{3}$', re.I)
    for f in checklist:
        #print f
        if regex_notdot.findall(f):
            if os.path.isfile(f):
                filepath = os.path.abspath(f)
            try:
                _file = __builtin__.open(filepath, "rb")
                content = _file.read()
                _file.close()
                md5 = hashlib.md5(content)
                _hash = md5.hexdigest()
                if regex_jpg.findall(filepath):
                    if _hash in hash_table_jpg.keys():
                        dups.append(_hash, os.path.abspath(filepath))
                    else:
                        hash_table_jpg[_hash] = filepath
                elif regex_png.findall(filepath):
                    if _hash in hash_table_png.keys():
                        dups.append(_hash, os.path.abspath(filepath))
                    else:
                        hash_table_png[_hash] = filepath
                else:
                    if _hash in hash_table_general.keys():
                        dups.append(_hash, os.path.abspath(filepath))
                    else:
                        hash_table_general[_hash] = filepath
            except:
                pass
    if not hash_table_jpg and not hash_table_png:
        return hash_table_general, dups
    else:
        return hash_table_jpg, hash_table_png, dups



def update_filerecord_pymongo(database_name=None, collection_name=None, md5checksum=None, filename=None, filepath=None, colorstyle=None, alt=None, ext=None, create_dt=None):
    # Insert a New Document
    import pymongo, bson, datetime
    from bson import Binary, Code
    from bson.json_util import dumps
    mongo = pymongo.Connection('127.0.0.1')
    mongo_db = mongo[database_name]
    mongo_collection = mongo_db[collection_name]

    key = {'md5checksum': md5checksum}
    key_str = key.keys()[0]
    key_val = key.values()[0]
    

    #, 'alt': alt, 'upload_ct': 1}
    #data = { "$set":{'ext': ext,'md5checksum': md5checksum,'alt': alt, upload_ct: 1,'create_dt': create_dt}},
    # Convert date string to date obj
    create_dt = datetime.datetime.strptime(create_dt, '%Y-%m-%d')
    datarow = {'md5checksum': md5checksum, 'colorstyle': colorstyle, 'ext': ext, 'alt': alt, 'filepath': filepath,'filename': filename,'upload_ct': 1,'create_dt': create_dt}
    
    ## Check if key exists in db
    check = mongo_collection.find({key_str: key_val}).count()
    if check == 1:
        print 'UPDATING IT ', check
        data = { "$set":{
                        "md5checksum": md5checksum,
                        "colorstyle": colorstyle,
                        "alt": {"$min": {"alt": alt}},
                        "ext": ext,
                        "filename": filename,
                        "filepath": filepath,
                        #"upload_ct":
                        "$inc": {"upload_ct": 1},
                        "create_dt": { "$min": {"create_dt": create_dt}},
                        "modify_dt": { "$max": {"modify_dt": create_dt}}
                        }
                    }
        #return data, check
    else:
        print 'NEW IT ', check
        data = { "$set":{
                         "colorstyle": colorstyle,
                         "alt": alt,
                         "ext": ext,
                         "filename": filename,
                         "filepath": filepath,
                         "upload_ct": 1,
                         "create_dt": {"$min": {"create_dt": create_dt}},
                         "modify_dt": {"$max": {"modify_dt": create_dt}}
                        }
        }
    #data = { "$set":{'colorstyle': colorstyle,'ext': ext,'alt': alt, 'upload_ct': 1,'create_dt': create_dt}}
    #mongo_collection.create_index([("colorstyle", pymongo.DECENDING)], unique=True, sparse=False, background=True)
    #print data, key, key_str, key_val
    mongo_collection.create_index([(key_str, pymongo.ASCENDING)], unique=True, sparse=False, background=True)
    mongo_collection.create_index([("colorstyle", pymongo.DESCENDING),("ext", pymongo.ASCENDING),("alt", pymongo.ASCENDING)], sparse=False, background=True)
    new_insertobj_id = mongo_collection.update(key, data, upsert=True, multi=True)
    print "Upserted: {0}\nImageNumber: {1}\nFormat: {2}\nID: {3}".format(colorstyle, alt, ext, new_insertobj_id)
    return new_insertobj_id


    #print locals()
    ## Perform the Insert to mongodb
    #md5checksums.find({'colorstyle': colorstyle, 'app_config_id':{'$in':app_config_ids}})
    #expr = { "$or": [ {"md5checksums": { "$exists": False }}, {"colorstyle": colorstyle}]}
    #for c in collection_name.find(expr):
    #    print [ k.upper() for k in sorted(c.keys()) ]

    #except StopIteration:
        #print "Successful Batch Update Completed md5checksums..."

############################################
############ RUN ###########################
############################################


def main(files_list=None, database_name='images', collection_name='md5checksums'):
    import sys, os, re, sqlalchemy, json, pymongo
    regex_valid_colorstyle_file = re.compile(r'^(?:.*?/?)?.+?/([1-9][0-9]{8})(?:_)?([1-6x]|alt0[1-6])?\.([jpng]{3})?$', re.I)
    if not files_list:
        try:
            rootdir = sys.argv[1]
            files_list = recursive_dirlist(rootdir)
        except IndexError:
            print 'You need to define files_list= or as sys.argv[1]'
            raise
    res = find_md5_and_dups(files_list)
    insertkvdict = {}
    if len(res) <= 2:
        md5checksum_pairs, duplicates = res
        unique_files = md5checksum_pairs.values()
        insertkvdict = walkeddir_parse_to_kvdict(unique_files)
        return unique_files, duplicates, md5checksum_pairs
    elif len(res) == 3:
        hash_table_jpg, hash_table_png, dups = res
        if hash_table_jpg:
            #files_list = [ f for f in hash_table_jpg.items() if regex_valid_colorstyle_file.findall(f) ]
            insertkvdict = walkeddir_parse_to_kvdict(hash_table_jpg)
        if hash_table_png:
            #files_list = [ f for f in hash_table_png.items() if regex_valid_colorstyle_file.findall(f) ]
            insertkvdict = walkeddir_parse_to_kvdict(hash_table_png)

        for k,v in insertkvdict.iteritems():
            if not collection_name:
                collection_name = 'md5checksums'
            # # Build object of key/values for insert
            md5checksum = k #.keys()[0] #v['md5checksum']
            colorstyle  = v['colorstyle']
            alt         = v['alt']
            ext         = v['ext']
            filepath    = v['filepath'] #k.values()[1:]
            filename    = v['filename'] #k.values()[1:]
            create_dt   = v['create_dt']

            #print locals()
            ## Perform the Insert to mongodb
            #md5checksums.find({'colorstyle': colorstyle, 'app_config_id':{'$in':app_config_ids}})
            #expr = { "$or": [ {"md5checksums": { "$exists": False }}, {"colorstyle": colorstyle}]}
            #for c in collection_name.find(expr):
            #    print [ k.upper() for k in sorted(c.keys()) ]
            if regex_valid_colorstyle_file.findall(v['filepath']):
                ## inserts only, not updates, will create multiple records if exists already
                try:
                    update_filerecord_pymongo(database_name=database_name, collection_name=collection_name,
                                              md5checksum=md5checksum, filepath=filepath, filename=filename,
                                              colorstyle=colorstyle, alt=alt, ext=ext,
                                              create_dt=create_dt)
                    print "Successful Insert to --->\n\t {0} {1} --> {2}".format(collection_name, k, v)
                except pymongo.errors.ConnectionFailure:
                    import time
                    time.sleep(5)
                    pass
            else:
                print 'Failed Regex Validation --->\t ', v['filepath']
                pass
        if dups:
            return dups
        else:
            return
        #insertkvdict
        #return hash_table_jpg, hash_table_png, dups


if __name__ == '__main__':
    main()
