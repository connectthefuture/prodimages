#!/usr/bin/env python
# -*- coding: utf-8 -*-


def connect_gridfs_mongodb(db_name='None'):
    import pymongo, gridfs, __builtin__
    mongo = pymongo.MongoClient('127.0.0.1')
    mongo_db = mongo[db_name].authenticate('mongo', 'mongo')
    #mongo_db = mongo[db_name]
    db = mongo.db_name
    fs = gridfs.GridFS(db)
    return db, fs


def insert_file_gridfs_file7(filepath=None, metadata=None, db_name='gridfs_file7'):
    db, fs = connect_gridfs_mongodb(db_name=db_name)
    filename=filepath.spilt('/')[-1]
    content_type= 'image/' + filename.split('.')[-1]
    #content-type=content_type
    with fs.new_file(filename=filename, metadata=metadata) as fp:
        with open(filepath) as filedata:
            fp.write(filedata.read())
    return fp, db


def retrieve_last_instance_gridfs_file7(filepath=None, db_name='gridfs_file7'):
    db, fs = connect_gridfs_mongodb(db_name=db_name)
    return fp


def find_record_gridfs(key=None, db_name='gridfsFile7', collection_name=None):
    import pymongo, bson, datetime
    from bson import Binary, Code
    from bson.json_util import dumps
    #client = .authenticate('user', 'password', mechanism='SCRAM-SHA-1')
    db, fs = connect_gridfs_mongodb(db_name=db_name)
    mongo_collection = db.[collection_name]
    key = {'md5checksum': md5checksum}
    key_str = key.keys()[0]
    key_val = key.values()[0]
    check = mongo_collection.find({key_str: key_val}).count()
    return check


def main(filepath=None,metadata=None):
    insert_res = insert_file_gridfs_file7(filepath=filepath)
    return insert_res.items()


if __name__ == '__main__':
    import sys
    try:
        filename = sys.argv[1]
        res = insert_file_gridfs_file7(filepath=filepath)[0]
        print res._id 
    except IndexError:
        print 'No File supplied for insert'