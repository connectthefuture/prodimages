#!/usr/bin/env python
# -*- coding: utf-8 -*-


def connect_gridfs_mongodb(hostname=None,db_name=None):
    import pymongo, gridfs, __builtin__
    if not hostname:
        hostname='127.0.0.1'
    mongo = pymongo.MongoClient(hostname, max_pool_size=50, waitQueueMultiple=10)
    mongo_db = mongo[db_name]
    #mongo_db = mongo[db_name]
    mongo_db.authenticate('mongo', 'mongo')
    fs = ''
    fs = gridfs.GridFS(mongo_db)
    return mongo_db, fs


def get_gridfs_obj(destdir=None,hostname=None,db_name=None,query=None):
    from os import path
    mongo_db, fs = connect_gridfs_mongodb(hostname=hostname,db_name=db_name)
    if not query:
        fileobjs=fs.find()
        fileobj=fileobjs.next()
    else:
        fileobj=fs.find(query)
    outfile=path.join(destdir,fileobj.name)
    with open(outfile , 'wb') as f:
        f.write(fileobj.readchunk())
    return outfile



def main():
    import sys
    ret = get_gridfs_obj(hostname='127.0.0.1',db_name=sys.argv[1],destdir=sys.arv[2],query=syss.arv[3])
    return ret



if __name__ == '__main__':
    main()
