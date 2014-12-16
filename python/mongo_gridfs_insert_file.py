#!/usr/bin/env python
# -*- coding: utf-8 -*-



def insert_file_gridfs_a(filename=None,):
    import pymongo, gridfs, __builtin__
    conn = pymongo.Connection()
    db = conn.gridfs_a
    fs = gridfs.GridFS(db)
    with fs.new_file() as fp:
        with __builtin__.open(filename) as filedata:
            fp.write(filedata.read())
    return fp

def main(filename=None):
    insert_res = insert_file_gridfs_a(filename=filename)
    return insert_res.items()

if __name__ == '__main__':
    import sys
    try:
        filename = sys.argv[1]
        res = insert_file_gridfs_a(filename=filename)
        print res._id 
    except IndexError:
        print 'No File supplied for insert'