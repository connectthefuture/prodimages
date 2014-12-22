#!/usr/bin/env python
# -*- coding: utf-8 -*-


def connect_gridfs_mongodb(db_name='None'):
    import pymongo, gridfs, __builtin__
    mongo = pymongo.MongoClient('127.0.0.1')
    mongo_db = mongo[db_name]
    #mongo_db = mongo[db_name]
    mongo_db.authenticate('mongo', 'mongo')
    fs = gridfs.GridFS(mongo_db)
    return mongo_db, fs


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


def insert_file_gridfs_file7(filepath=None, metadata=None, db_name=None):
    import os
    db, fs = connect_gridfs_mongodb(db_name=db_name)
    try:
        filename = os.path.basename(filepath)
        content_type= 'image/' + filename.split('.')[-1]
        #content-type=content_type
        with fs.new_file(filename=filename, metadata=metadata) as fp:
            with open(filepath) as filedata:
                fp.write(filedata.read())
        return fp, db
    except AttributeError:
        print 'Failed ', filepath


def retrieve_last_instance_gridfs_file7(filepath=None, db_name=None):
    db, fs = connect_gridfs_mongodb(db_name=db_name)
    return fp


def find_record_gridfs(key=None, db_name=None, collection_name=None):
    import pymongo, bson, datetime
    from bson import Binary, Code
    from bson.json_util import dumps
    #client = .authenticate('user', 'password', mechanism='SCRAM-SHA-1')
    db, fs = connect_gridfs_mongodb(db_name=db_name)
    mongo_collection = db[collection_name]
    key = {'md5checksum': md5checksum}
    key_str = key.keys()[0]
    key_val = key.values()[0]
    check = mongo_collection.find({key_str: key_val}).count()
    return check


def main(filepath=None,metadata=None,db_name=None):
    print filepath
    if not db_name:
        db_name = 'gridfs_file7'
    insert_res = insert_file_gridfs_file7(filepath=filepath,metadata=metadata,db_name=db_name)
    try:
        return insert_res.items()
    except AttributeError:
        return insert_res 

if __name__ == '__main__':
    import sys
    try:
        filename = sys.argv[1]
        res = insert_file_gridfs_file7(filepath=filepath)[0]
        print res._id 
    except IndexError:
        print 'No File supplied for insert'