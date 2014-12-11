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
    return walkedlist


def find_duplicate_files(dirname, file_type=None):
    import hashlib, re
    import os, __builtin__

    hash_table_jpg     = {}
    hash_table_png     = {}
    hash_table_general = {}
    dups               = []

    if type(dirname) == str:
        dirname = os.path.abspath(dirname)
        os.chdir(os.path.abspath(dirname))
        checklist = os.listdir(dirname)
    else:
        checklist = dirname

    if not file_type:
        ## Use basic regex excluding . (dot) files
        regex = re.compile(r'^.+?\..+?$')
        regex_jpg = re.compile(r'^.+?\.[jpg]{3}$', re.I)
        regex_png = re.compile(r'^.+?\.[png]{3}$', re.I)
        #regex_images = re.compile(r'^.+?\.[jpngJPNG]{3}$')
    for f in checklist:
        #print f
        if regex.findall(f):
            if os.path.isfile(f):
                filepath = os.path.join(dirname, f)
            
            try:  
                _file = __builtin__.open(filepath, "rb")
                content = _file.read()
                _file.close()
                md5 = hashlib.md5(content)
                _hash = md5.hexdigest()
                if regex_jpg.findall(filepath):
                    if _hash in hash_table_jpg.keys():
                        dups.append(os.path.abspath(filepath))
                    else:
                        hash_table_jpg[_hash] = f
                elif regex_png.findall(filepath):
                    if _hash in hash_table_png.keys():
                        dups.append(os.path.abspath(filepath))
                    else:
                        hash_table_png[_hash] = f
                else:
                    if _hash in hash_table_general.keys():
                        dups.append(os.path.abspath(filepath))
                    else:
                        hash_table_general[_hash] = f               
            except:
                pass
    if not hash_table_png and hash_table_png:
        return hash_table_general, dups
    else:
        return hash_table_jpg, hash_table_png, dups



def update_filerecord_pymongo(database_name=None, collection_name=None, md5checksum=None, colorstyle=None, alt=None, format=None, timestamp=None):
    # Insert a New Document
    import pymongo, bson
    from bson import Binary, Code
    from bson.json_util import dumps
    mongo = pymongo.Connection('127.0.0.1')
    mongo_db = mongo[database_name]
    mongo_collection = mongo_db[collection_name]

    key = {'colorstyle': colorstyle}  #, 'alt': alt, 'upload_ct': 1}
    #data = { "$set":{'format': format,'md5checksum': md5checksum,'alt': alt, upload_ct: 1,'timestamp': timestamp}},
    datarow = {'colorstyle': colorstyle, 'format': format, 'md5checksum': md5checksum, 'alt': alt, 'upload_ct': 1,'timestamp': timestamp}
    key_str = key.keys()[0]
    check = mongo_collection.find({key_str: colorstyle}).count()
    if check == 1:
        print 'REFRESH IT ', check
        data = { "$set":{
                        'colorstyle': colorstyle,
                        'alt': {'$min': {'alt': alt}},
                        'format': format,
                        'md5checksum': md5checksum,
                        #'upload_ct':
                        '$inc': {'upload_ct': 1},
                        'timestamp': { '$max': {'timestamp': timestamp}}
                        }
                    }
        return check
    else:
        print 'NEW IT ', check
        data = { "$set":{'format': format,'md5checksum': md5checksum,'alt': alt, 'upload_ct': 1,'timestamp': timestamp}}
        #mongo_collection.create_index([("colorstyle", pymongo.ASCENDING)], unique=True, sparse=True, background=True)
    mongo_collection.create_index("colorstyle", unique=True, sparse=False, background=True)
    #mongo_collection.create_index([("colorstyle", pymongo.ASCENDING),("alt", pymongo.DECENDING)], background=True)
    new_insertobj_id = mongo_collection.update(key, data, upsert=True, multi=True)
    print "Inserted: {0}\nImageNumber: {1}\nFormat: {2}\nID: {3}".format(colorstyle,alt, format,new_insertobj_id)
    return new_insertobj_id


def main_update(dirname=None, database_name='images', collection_name=None):
    import sys,os,re, sqlalchemy, json, pymongo
    regex_valid_colorstyle_file = re.compile(r'^(.*?/?)?.*?([0-9]{9})(_alt0[1-6])?(\.[jpngJPNG]{3})?$')
    if not dirname:
        try:
            dirname = sys.argv[1]
        except:
            dirname = '/mnt/Post_Complete/ImageDrop'
    ## Take the compiled k/v pairs and Format + Insert into Mongo DB
    hash_table_jpg, hash_table_png, dups = find_duplicate_files(dirname)
    #try:sorted(data, reverse=True)
    if hash_table_png:
        hash_table = hash_table_png
    elif hash_table_jpg:
        hash_table = hash_table_jpg
    
    for batch in hash_table.iteritems():
        if not collection_name:
            collection_name = 'md5checksums'
        for k,v in hash_table.items():
            ## Build object of key/values for insert
            md5checksum = row['md5checksum']
            colorstyle = row['colorstyle']
            alt = row['alt']
            format = row['format']
            timestamp = row['timestamp']
            #print locals()
            ## Perform the Insert to mongodb
            #md5checksums.find({'colorstyle': colorstyle, 'app_config_id':{'$in':app_config_ids}})
            #expr = { "$or": [ {"md5checksums": { "$exists": False }}, {"colorstyle": colorstyle}]}
            #for c in collection_name.find(expr):
            #    print [ k.upper() for k in sorted(c.keys()) ]
            if regex_valid_colorstyle_file.findall(row['filename']):
                ## inserts only, not updates, will create multiple records if exists already
                try:
                    update_filerecord_pymongo(database_name=database_name, collection_name=collection_name, md5checksum=md5checksum, colorstyle=colorstyle, alt=alt, format=format, timestamp=timestamp)
                    print "Successful Insert to md5checksums {0} --> {1}".format(k,v)
                except pymongo.errors.ConnectionFailure:
                    import time
                    time.sleep(5)
                    pass
                else:
                    pass
        return dups
        #except StopIteration:
            #print "Successful Batch Update Completed md5checksums..."

############################################
############ RUN ###########################
############################################

import os,sys


def main(dirname=None):
    if not dirname:
        try:
            dirname = sys.argv[1]
        except IndexError:
            print 'You need to define dirname= or as sys.argv[1]'
            raise
    res = find_duplicate_files(dirname)
    if len(res) <= 2:
        md5checksum_pairs, duplicates = res
        unique_files = md5checksum_pairs.values()
        return unique_files, duplicates, md5checksum_pairs
    elif len(res) == 3:
        hash_table_jpg, hash_table_png, dups = res
        return hash_table_jpg, hash_table_png, dups
    
    


if __name__ == '__main__':
    unique_files, duplicates, md5checksum_pairs = main()
    print unique_files, duplicates, md5checksum_pairs

