#!/usr/bin/env python
# -*- coding: utf-8 -*-


def connect_gridfs_mongodb(db_name='None'):
    import pymongo, gridfs, __builtin__
    conn = pymongo.Connection('127.0.0.1')
    db = conn.db_name
    fs = gridfs.GridFS(db)
    return db, fs


def insert_file_gridfs_file7(filename=None, db_name='gridfs_file7'):
    db, fs = connect_gridfs_mongodb(db_name=db_name)
    with fs.new_file() as fp:
        with open(filename) as filedata:
            fp.write(filedata.read())
    return fp, db


def retrieve_last_instance_gridfs_file7(filename=None, db_name='gridfs_file7'):
    db, fs = connect_gridfs_mongodb(db_name=db_name)
    return fp


def find_record_gridfs(key=None, database_name='gridfsFile7', collection_name=None):
    import pymongo, bson, datetime
    from bson import Binary, Code
    from bson.json_util import dumps
    mongo = pymongo.Connection('127.0.0.1')
    mongo_db = mongo[database_name]
    mongo_collection = mongo_db[collection_name]
    key = {'md5checksum': md5checksum}
    key_str = key.keys()[0]
    key_val = key.values()[0]
    check = mongo_collection.find({key_str: key_val}).count()
    return check


def main(filename=None):
    insert_res = insert_file_gridfs_file7(filename=filename)
    return insert_res.items()


if __name__ == '__main__':
    import sys
    try:
        filename = sys.argv[1]
        res = insert_file_gridfs_file7(filename=filename)[0]
        print res._id 
    except IndexError:
        print 'No File supplied for insert'