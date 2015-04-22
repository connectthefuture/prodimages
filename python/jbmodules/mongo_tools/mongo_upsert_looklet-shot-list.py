#!/usr/bin/env python
# coding: utf-8

import sys, os.path
mongotoolsdir = os.path.dirname('__file__')
sys.path.append(mongotoolsdir)

def connect_gridfs_mongodb(hostname=None,db_name=None):
    import pymongo, gridfs, __builtin__
    if not hostname:
        hostname='127.0.0.1'
    mongo = pymongo.MongoClient(hostname, maxPoolSize=50, waitQueueMultiple=10)
    mongo_db = mongo[db_name]
    #mongo_db = mongo[db_name]
    mongo_db.authenticate('mongo', 'mongo')
    fs = ''
    #fs = gridfs.GridFS(mongo_db)
    return mongo_db, fs



def update_filerecord_pymongo(database_name=None, collection_name=None, username=None, colorstyle=None, photodate=None, reshoot=None, timestamp=None):
    # Insert a New Document
    import pymongo, bson
    from bson import Binary, Code
    from bson.json_util import dumps
    mongo_db, fs = connect_gridfs_mongodb(db_name=database_name)
    if fs:
        collection_name = 'fs.files'
    mongo_collection = mongo_db[collection_name]

    key = {'timestamp': timestamp}  #, 'photodate': photodate, 'shoot_ct': 1}
    #data = { "$set":{'reshoot': reshoot,'username': username,'photodate': photodate, shoot_ct: 1,'timestamp': timestamp}},
    #datarow = {'colorstyle': colorstyle, 'reshoot': reshoot,'username': username,'photodate': photodate, 'shoot_ct': 1,'timestamp': timestamp}
    key_str = key.keys()[0]
    check = mongo_collection.find({key_str: colorstyle}).count()
    if check == 1:
        print 'REFRESH IT ', check
        data = { "$set":{
                        'colorstyle': colorstyle,
                        'photodate': {'$min': {'photodate': photodate}},
                        'reshoot': reshoot,
                        'username': username,
                        #'shoot_ct':
                        '$inc': {'shoot_ct': 1},
                        'timestamp': { '$max': {'timestamp': timestamp}}
                        }
                    }
        return check
    else:
        print 'NEW IT ', check
        data = { "$set":{'reshoot': reshoot,'username': username, 'photodate': photodate, 'shoot_ct': 1,'timestamp': timestamp}}
        #mongo_collection.create_index([("colorstyle", pymongo.ASCENDING)], unique=True, sparse=True, background=True)
    mongo_collection.ensure_index("timestamp", unique=True, sparse=True, background=True)
    #mongo_collection.create_index([("colorstyle", pymongo.ASCENDING),("photodate", pymongo.DECENDING)], background=True)
    new_insertobj_id = mongo_collection.update(key, data, upsert=True, multi=True)
    print "Inserted: {0}\nPhotodate: {1}\nReshoot: {2}\nID: {3}".format(colorstyle,photodate, reshoot,new_insertobj_id)
    return new_insertobj_id


def main(filename=None):
    import sys,os,re, sqlalchemy, json, datetime, requests
    from os import path
    today = datetime.date.strftime(datetime.date.today(), '%Y-%m-%d')
    if not filename:
        try:
            filename = sys.argv[1]
            if path.isfile(filename):
                pass
            else:
                filename='/var/www/srv/media/feeds/{0}_LookletShotListImportJSON.json'.format(today)
        except IndexError:
            filename='/var/www/srv/media/feeds/{0}_LookletShotListImportJSON.json'.format(today)
    data_insert = json.load(open(filename,'rb'))
    #print data_insert
    for d in data_insert:
        try:
            database_name = 'images'
            collection_name = 'looklet_shot_list'
            #print d
            # Build object of key/values for insert
            colorstyle = d['colorstyle']
            photodate = d['photodate']
            reshoot = d['reshoot']
            timestamp = d['timestamp']
            username = d['username']
            #print locals()
            ## Perform the Insert to mongodb
            #uploads_imagedrop.find({'colorstyle': colorstyle, 'app_config_id':{'$in':app_config_ids}})
            #expr = { "$or": [ {"uploads_imagedrop": { "$exists": False }}, {"colorstyle": colorstyle}]}
            #for c in collection_name.find(expr):
            #    print [ k.upper() for k in sorted(c.keys()) ]
            #if regex_valid_colorstyle.findall(d['colorstyle']):
            ##updates/upserts, will not create multiple records if timesramp exists already
            update_filerecord_pymongo(database_name=database_name, collection_name=collection_name, photodate=photodate, colorstyle=colorstyle, username=username, reshoot=reshoot, timestamp=timestamp)
            print "Successful Insert to {0} --> {1}".format(database_name + collection_name, colorstyle)
        except OSError:
            print 'OSKEY ERROR'
            pass



if __name__ == '__main__':
    import sys
    try:
        jsonfile=sys.argv[1]
    except IndexError:
        jsonfile = None
    main(filename=jsonfile)
