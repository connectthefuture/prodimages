#!/usr/bin/env python
# -*- coding: utf-8 -*-


def connect_gridfs_mongodb(hostname=None,db_name=None):
    import pymongo, gridfs
    if not hostname:
        hostname='127.0.0.1'
    try:
        mongo = pymongo.MongoClient(hostname, waitQueueMultiple=10)
    except pymongo.errors.ConnectionFailure:
        hostname = '192.168.20.59'
        mongo = pymongo.MongoClient(hostname, waitQueueMultiple=10)
    
    mongo_db = mongo[db_name]
    #mongo_db = mongo[db_name]
    mongo_db.authenticate('mongo', 'mongo')
    fs = ''
    fs = gridfs.GridFS(mongo_db)
    return mongo_db, fs


def insert_filerecord_pymongo(db_name=None, collection_name=None, filename=None, metadata=None, colorstyle=None, alt=None, format=None, timestamp=None, **kwargs):
    # Insert a New Document
    import pymongo
    mongo = pymongo.MongoClient('127.0.0.1', waitQueueMultiple=10)
    mongo_db = mongo[db_name]
    mongo_collection = mongo_db[collection_name]

    # Returns the '_id' key associated with the newly created document
    new_insertobj_id = mongo_collection.insert({'colorstyle': colorstyle,'format': format,'metadata': metadata,'alt': alt, 'upload_ct': 1,'timestamp': timestamp})
    #    new_insertobj_id = mongo_collection.insert({'colorstyle': colorstyle,'format': format,'metadata': metadata,'alt': alt, 'upload_ct': 1,'timestamp': timestamp})
    # new_insertobj_id = mongo_collection.insert({'colorstyle': colorstyle,'format': format,'metadata': metadata,'alt': alt, 'upload_ct': 1,'timestamp': timestamp}, continue_on_error=True, upsert=True)
    print "Inserted: {0}\nImageNumber: {1}\nFormat: {2}\nID: {3}".format(colorstyle,alt, format,new_insertobj_id)
    return new_insertobj_id


def update_filerecord_pymongo(db_name=None, collection_name=None, filename=None, filepath=None, metadata=None, colorstyle=None, alt=None, format=None, timestamp=None, **kwargs):
    # Insert a New Document
    # (filepath=None, metadata=None, db_name=None):
    import os
    import pymongo, bson
    from bson import Binary, Code
    from bson.json_util import dumps
    import datetime
    mongo_db, fs = connect_gridfs_mongodb(db_name=db_name)
    if fs:
        collection_name = 'fs.files'
        if not alt:
            alt = '1'

    tmpfilename          = str(filepath.split('/')[-1])
    colorstyle           = str(tmpfilename[:9])
    image_number         = str(tmpfilename.split('.')[-2][-1])
    alt                  = image_number
    content_type         = str(tmpfilename.split('.')[-1]).lower().replace('jpg', 'jpeg')

    if not timestamp:
        timestamp = datetime.datetime.now()

    mongo_collection = mongo_db[collection_name]
    key = {'colorstyle': colorstyle}  #, 'alt': alt, 'upload_ct': 1}
    # data = { "$set":{'format': format,'metadata': metadata,'alt': alt, upload_ct: 1,'timestamp': timestamp}},
    datarow = {'colorstyle': colorstyle, 'format': format,'metadata': metadata,'alt': alt, 'upload_ct': 1,'timestamp': timestamp}
    key_str = key.keys()[0]
    check = mongo_collection.find({key_str: colorstyle}).count()
    if check == 1:
        print 'REFRESH IT ', check
        data = { "$set":{
                        'colorstyle': colorstyle,
                        'alt': {'$min': {'alt': alt}},
                        'format': format,
                        'metadata': metadata,
                        'content_type': content_type,
                        #'upload_ct':
                        '$inc': {'upload_ct': 1},
                        'timestamp': { '$max': {'timestamp': timestamp}}
                        }
                    }
        return check
    else:
        print 'NEW IT ', check
        data = { "$set":{ 'colorstyle': colorstyle, 'format': format, 'metadata': metadata, 'alt': alt, 'upload_ct': 1,'timestamp': timestamp}}
        # mongo_collection.create_index([("colorstyle", pymongo.ASCENDING)], unique=True, sparse=True, background=True)
    try:
        mongo_collection.create_index("md5", unique=True, sparse=False, background=True)
    except pymongo.errors.DuplicateKeyError:
        print ' DuplicateKey Error', key_str
        pass
    # mongo_collection.create_index([("colorstyle", pymongo.ASCENDING),("alt", pymongo.DECENDING)], background=True)
    
    new_insertobj_id = mongo_collection.update(key, data, upsert=True, multi=True)
    print "Inserted: {0}\nImageNumber: {1}\nFormat: {2}\nID: {3}".format(colorstyle,alt, format,new_insertobj_id)
    return new_insertobj_id


def get_duplicate_records(db_name=None, collection_name=None):
    # Insert a New Document
    import pymongo, bson, datetime
    from bson import Binary, Code
    from bson.json_util import dumps
    db, fs = connect_gridfs_mongodb(db_name=db_name)
    mongo_collection = db[collection_name]
    data = { "$group": {"_id": { "firstField": "$filename","secondField": "$md5" },"uniqueIds": { "$addToSet": "$_id" },"count": { "$sum": 1 }}},{ "$match": {"count": { "$gt": 1 }}}
    res = mongo_collection.aggregate([data][0])
    return res


def retrieve_last_instance_gridfs(filepath=None, db_name=None):
    db, fs = connect_gridfs_mongodb(db_name=db_name)
    return fs


def find_record_gridfs(key=None, md5checksum=None, db_name=None, collection_name=None):
    import pymongo, bson, datetime
    from bson import Binary, Code
    from bson.json_util import dumps
    # client = .authenticate('user', 'password', mechanism='SCRAM-SHA-1')
    db, fs = connect_gridfs_mongodb(db_name=db_name)
    mongo_collection = db[collection_name]
    if not key:
        key = {'md5checksum': md5checksum}
    key_str = key.keys()[0]
    key_val = key.values()[0]
    check = mongo_collection.find({key_str: key_val}).count()
    return check


def insert_file_gridfs(filepath=None, metadata=None, db_name=None, **kwargs):
    import os
    db, fs = connect_gridfs_mongodb(db_name=db_name)
    try:
        filename = os.path.basename(filepath)
        ext = filename.split('.')[-1].lower()
        if ext == 'jpg' or ext == 'jpeg':
            content_type = 'image/jpeg'
        elif ext == 'tif' or ext == 'tiff':
            content_type= 'image/tiff'
        else:
            content_type= 'image/' + str(ext)
        #content-type=content_type
        if not find_record_gridfs(key={"filename": filename}, db_name=db_name, collection_name='fs.files'):
            try:
                with fs.new_file(filename=filename, content_type=content_type, metadata=metadata) as fp:
                    with open(filepath) as filedata:
                        fp.write(filedata.read())
                return fp, db
            except IOError:
                print ' IO ERROR '
                return False
        else:
            r = find_record_gridfs(key={"filename": filename}, db_name=db_name, collection_name='fs.files')
            print r
    except OSError:
        print 'Failed ', filepath


def update_file_gridfs(filepath=None, metadata=None, db_name=None, **kwargs):
    import os
    db, fs = connect_gridfs_mongodb(db_name=db_name)
    try:
        filename = os.path.basename(filepath)
        ext = filename.split('.')[-1].lower()
        if ext == 'jpg' or ext == 'jpeg':
            content_type = 'image/jpeg'
        elif ext == 'tif' or ext == 'tiff':
            content_type= 'image/tiff'
        else:
            content_type= 'image/' + str(ext)
        #content-type=content_type
        if not find_record_gridfs(key={"filename": filename}, db_name=db_name, collection_name='fs.files'):
            try:
                with fs.new_file(filename=filename, content_type=content_type, metadata=metadata) as fp:
                    with open(filepath) as filedata:
                        fp.write(filedata.read())
                return fp, db
            except IOError:
                print ' IO ERROR '
                return False
        else:
            
            r = find_record_gridfs(key={"filename": filename}, db_name=db_name, collection_name='fs.files')
            update_filerecord_pymongo(filepath=filepath,metadata=metadata,db_name=db_name)
            print r
    except OSError:
        print 'Failed ', filepath


def main(filepath=None,metadata=None,db_name=None):
    print filepath
    if not db_name:
        db_name = 'gridfs_file7'
    insert_res = insert_file_gridfs(filepath=filepath,metadata=metadata,db_name=db_name)
    try:
        return insert_res.items()
    except AttributeError:
        return insert_res



if __name__ == '__main__':
    import sys
    try:
        filepath = sys.argv[1]
        res = insert_file_gridfs(filepath=filepath)[0]
        print res._id 
    except IndexError:
        print 'No File supplied for insert'
