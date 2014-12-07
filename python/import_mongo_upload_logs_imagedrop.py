#!/usr/bin/env python
# -*- coding: utf-8 -*-

def parse_upload_log_files_indir(dirname=None):
    import re, datetime, glob, os
    #dirname =  '/Users/johnb/Dropbox/DEVROOT/mnt/Post_Complete/ImageDrop/bkup' ##'/Users/johnb/Dropbox/DEVROOT/mnt/Post_Complete/ImageDrop/bkup'
    regex_textfile = re.compile(r'^(/.+?/)(LSTransfer)(\d{12})(.txt)$')
    regex_datarow  = re.compile(r'^(/.+?/)(LSTransfer)(\d{12})(.txt)$')
    textfile_list  = glob.glob(os.path.join(dirname, 'LST*.txt'))
    data = {}
    page = 1
    for textfile in textfile_list:
        if regex_textfile.findall(textfile):
            matches = regex_textfile.match(textfile)
            datarows = open(textfile).readlines()
            insertbatch = []
            for datarow in datarows[1:]:
                datarow = datarow.strip('\n').strip('\r')
                insertrow = {}
                try:
                    ts = matches.groups()[2]
                    tsstr = "{0}-{1}-{2} {3}-{4}".format(ts[:4],ts[4:6],ts[6:8],ts[8:10],ts[10:12],ts[12:15])
                    timestamp = datetime.datetime.strptime(tsstr, '%Y-%m-%d %H-%M')
                    insertrow['batchid'] = ts
                    insertrow['colorstyle'] = datarow.split()[-1][:9]
                    insertrow['filename'] = datarow.split()[-1]
                    insertrow['format'] = datarow.split('.')[-1]
                    insertrow['timestamp'] = timestamp
                    alttest = datarow.split('.')[-2].split('_')[1][-1]
                    if alttest.isdigit():
                        insertrow['alt'] = int(alttest) + 1
                    elif alttest.islower():
                        insertrow['alt'] = int(0)
                    elif not alttest:
                        insertrow['alt'] = 'X'
                    insertbatch.append(insertrow)
                except IndexError:
                    insertrow['alt'] = 1
                    if insertrow['colorstyle']:
                        insertbatch.append(insertrow)
            data[page] = insertbatch
            yield data[page]
            page += 1


def insert_filerecord_pymongo(database_name=None, collection_name=None, batchid=None, colorstyle=None, alt=None, format=None, timestamp=None):
    # Insert a New Document
    import pymongo
    mongo = pymongo.Connection('127.0.0.1')
    mongo_db = mongo[database_name]
    mongo_collection = mongo_db[collection_name]

    # Returns the '_id' key associated with the newly created document
    new_insertobj_id = mongo_collection.insert({'colorstyle': colorstyle,'format': format,'batchid': batchid,'alt': alt,'timestamp': timestamp})
    #    new_insertobj_id = mongo_collection.insert({'colorstyle': colorstyle,'format': format,'batchid': batchid,'alt': alt,'timestamp': timestamp})
    #new_insertobj_id = mongo_collection.insert({'colorstyle': colorstyle,'format': format,'batchid': batchid,'alt': alt,'timestamp': timestamp}, continue_on_error=True, upsert=True)
    print "Inserted: {0}\nImageNumber: {1}\nFormat: {2}\nID: {3}".format(colorstyle,alt, format,new_insertobj_id)
    return new_insertobj_id


def update_filerecord_pymongo(database_name=None, collection_name=None, batchid=None, colorstyle=None, alt=None, format=None, timestamp=None):
    # Insert a New Document
    import pymongo, bson
    from bson import Binary, Code
    from bson.json_util import dumps
    mongo = pymongo.Connection('127.0.0.1')
    mongo_db = mongo[database_name]
    mongo_collection = mongo_db[collection_name]

    key = {'colorstyle': colorstyle}  #, 'alt': alt}
    #data = { "$set":{'format': format,'batchid': batchid,'alt': alt,'timestamp': timestamp}},
    datarow = {'colorstyle': colorstyle, 'format': format,'batchid': batchid,'alt': alt,'timestamp': timestamp}
     
    check = main_check(datarow=dumps(datarow))
    if check == True:
        print 'REFRESH IT ', check
    else:
        print 'NEW IT ', check

    data = { "$set":{'format': format,'batchid': batchid,'alt': alt,'timestamp': timestamp}}
    mongo_collection.create_index([("colorstyle", pymongo.ASCENDING)], background=True)
    #mongo_collection.create_index([("colorstyle", pymongo.ASCENDING),("alt", pymongo.DECENDING)], background=True)
    new_insertobj_id = mongo_collection.update(key, data, upsert=True, multi=True)
    print "Inserted: {0}\nImageNumber: {1}\nFormat: {2}\nID: {3}".format(colorstyle,alt, format,new_insertobj_id)
    return new_insertobj_id


def get_filerecord_pymongo(database_name=None, collection_name=None, batchid=None, colorstyle=None, alt=None, format=None, timestamp=None):
    import pymongo
    mongo = pymongo.Connection('127.0.0.1')
    mongo_db = mongo[database_name]
    mongo_collection = mongo_db[collection_name]
    key = 'colorstyle'
    #data = { "$set":{'format': format,'batchid': batchid,'alt': alt,'timestamp': timestamp}},
    data = {'colorstyle': colorstyle, 'format': format,'batchid': batchid,'alt': alt,'timestamp': timestamp}
    results = mongo_collection.find({key: colorstyle}).count()
    #return count of styles with the number found
    return results


def normalize_json_tounicode(input_data):
    from kitchen.text.converters import getwriter, to_unicode
    import json
    from collections import defaultdict
    from os import path
    data = []
    if type(input_data) == 'str':
        if path.isfile(input_data):
            jsondata = json.load(open(input_data))
            print 'FILE'
            for row in jsondata:
                datarow = {}
                for k,v in row.items():
                    if type(v) == unicode:
                        v = to_unicode(v)
                    if type(k) == unicode:
                        k = to_unicode(k)
                    if type(v) == int:
                        v = str(v)
                        v = to_unicode(v)
                    if type(k) == int:
                        k = str(k)
                        k = to_unicode(k)
                    #print type(v), type(k)
                    datarow[k] = v
                #data[to_unicode(row[k])] = datarow
                data.append(datarow)
        else:
            jsondata = json.dumps(input_data)
            print 'STR'
    else:
        jsondata = input_data
        datarow =  {} ##defaultdict(list)
        for k,v in jsondata.iteritems():
            if type(v) == unicode:
                v = to_unicode(v)
            if type(k) == unicode:
                k = to_unicode(k)
            if type(v) == int:
                v = str(v)
                v = to_unicode(v)
            if type(k) == int:
                k = str(k)
                k = to_unicode(k)
            #print type(v), type(k)
            #datarow[k].append(v)
            datarow[k] = v
        #data[to_unicode(row[k])] = datarow
        data.append(datarow)
        print 'ELSE', type(input_data)
    return data


class MongodbClient:
    import pymongo
    #conn = pymongo.Connection('mongodb://tutorial-test:u3ZYh136@ds029187.mongolab.com:29187/tutorial-test')
    def __init__(self):
        #super(SuperClass, self).__init__()
        self.hostname           = ''
        self.database_name      = ''
        self.db                 = ''
        self.conn               = ''
        self.collection_name    = ''
        self.defaultHost        = True
        self.alt_host_port      = ''
        self.item               = ''

        # Set Global Style number variable if available in env
        try:
            self.objects = data
        except:
            self.objects = ''
            pass

    def connect_to_mongodb(self):
        if defaultHost:
            self.conn = pymongo.Connection('mongodb://127.0.0.1:27017/' + database_name)
        else:
            self.conn = pymongo.Connection('mongodb://' + alt_host_port + '/' + database_name)
        db = self.conn[database_name]
        return self.db

    def find_in_collection(self):
        #db.collection_name.insert({})
        db.collection_name.find()
        return list(db.collection_name.find())

    def save(self):
        self.collection_name.insert(self.objects)

    def fetch(self):
        return self.collection_name.find_one({"id": self.item })


class ImageDropMongodbClient(MongodbClient):
    import pymongo
    #conn = pymongo.Connection('mongodb://tutorial-test:u3ZYh136@ds029187.mongolab.com:29187/tutorial-test')
    def __init__(self, **kargs): ##  data,
        #super(ImageDropMongodbClient, self).__init__()
        self.batchid   = self.item['batchid']
        self.colorstyle = self.item['colorstyle']
        self.alt        = self.item['alt']
        self.format     = self.item['format']
        self.timestamp  = self.item['timestamp']


def main_check(datarow=None):
    import sys,os,re, sqlalchemy, json
    regex_uploadlogs = re.compile(r'^.*?/Post_Complete/ImageDrop/bkup/LSTransfer.+?\.[txtTXT]{3}$')
    regex_valid_colorstyle_file = re.compile(r'^(.*?/?)?.*?([0-9]{9})(_alt0[1-6])?(\.[jpngJPNG]{3})?$')
    database_name = 'images'
    collection_name = 'uploads_imagedrop'
    ## Build object of key/values for insert
    batchid = datarow[0]['batchid']
    colorstyle = datarow[0]['colorstyle']
    alt = datarow[0]['alt']
    format = datarow[0]['format']
    timestamp = datarow[0]['timestamp']
    #print locals()
    ## Perform the Insert to mongodb
    #uploads_imagedrop.find({'colorstyle': colorstyle, 'app_config_id':{'$in':app_config_ids}})
    #expr = { "$or": [ {"uploads_imagedrop": { "$exists": False }}, {"colorstyle": colorstyle}]}

    #for c in collection_name.find(expr):
    #    print [ k.upper() for k in sorted(c.keys()) ]
    if regex_valid_colorstyle_file.findall(datarow[0]['filename']):
        ## inserts only, not updates, will create multiple records if exists already
        check = get_filerecord_pymongo(database_name=database_name, collection_name=collection_name, batchid=batchid, colorstyle=colorstyle, alt=alt, format=format, timestamp=timestamp)
        if check >= 1:
            print "Successful Insert to uploads_imagedrop {0} --> {1}".format(datarow[0])
            return True, check
        else:
            return False, check


def main_update(dirname=None):
    import sys,os,re, sqlalchemy, json
    regex_uploadlogs = re.compile(r'^.*?/Post_Complete/ImageDrop/bkup/LSTransfer.+?\.[txtTXT]{3}$')
    regex_valid_colorstyle_file = re.compile(r'^(.*?/?)?.*?([0-9]{9})(_alt0[1-6])?(\.[jpngJPNG]{3})?$')
    if not dirname:
        try:
            dirname = sys.argv[1]
        except:
            dirname = '/mnt/Post_Complete/ImageDrop/bkup'
    ## Take the compiled k/v pairs and Format + Insert into Mongo DB
    transfer_batches = parse_upload_log_files_indir(dirname=dirname)
    for batch in transfer_batches:
        database_name = 'images'
        collection_name = 'uploads_imagedrop'
        for row in batch:
            #print row
            for k,v in row.items():
                ## Build object of key/values for insert
                batchid = row['batchid']
                colorstyle = row['colorstyle']
                alt = row['alt']
                format = row['format']
                timestamp = row['timestamp']
                #print locals()
                ## Perform the Insert to mongodb
                #uploads_imagedrop.find({'colorstyle': colorstyle, 'app_config_id':{'$in':app_config_ids}})
                #expr = { "$or": [ {"uploads_imagedrop": { "$exists": False }}, {"colorstyle": colorstyle}]}

                #for c in collection_name.find(expr):
                #    print [ k.upper() for k in sorted(c.keys()) ]
                if regex_valid_colorstyle_file.findall(row['filename']):
                    ## inserts only, not updates, will create multiple records if exists already
                    update_filerecord_pymongo(database_name=database_name, collection_name=collection_name, batchid=batchid, colorstyle=colorstyle, alt=alt, format=format, timestamp=timestamp)
                    print "Successful Insert to uploads_imagedrop {0} --> {1}".format(k,v)
                else:
                    pass


def main(dirname=None):
    import sys,os,re, sqlalchemy, json
    regex_uploadlogs = re.compile(r'^.*?/Post_Complete/ImageDrop/bkup/LSTransfer.+?\.[txtTXT]{3}$')
    regex_valid_colorstyle_file = re.compile(r'^(.*?/?)?.*?([0-9]{9})(_alt0[1-6])?(\.[jpngJPNG]{3})?$')
    if not dirname:
        try:
            dirname = sys.argv[1]
        except:
            dirname = '/mnt/Post_Complete/ImageDrop/bkup'
    ## Take the compiled k/v pairs and Format + Insert into Mongo DB
    transfer_batches = parse_upload_log_files_indir(dirname=dirname)
    for batch in transfer_batches:
        database_name = 'images'
        collection_name = 'uploads_imagedrop'
        for row in batch:
            print row
            for k,v in row.items():
                ## Build object of key/values for insert
                batchid = row['batchid']
                colorstyle = row['colorstyle']
                alt = row['alt']
                format = row['format']
                timestamp = row['timestamp']
                print locals()
                ## Perform the Insert to mongodb
                #uploads_imagedrop.find({'colorstyle': colorstyle, 'app_config_id':{'$in':app_config_ids}})
                #expr = { "$or": [ {"uploads_imagedrop": { "$exists": False }}, {"colorstyle": colorstyle}]}

                #for c in collection_name.find(expr):
                #    print [ k.upper() for k in sorted(c.keys()) ]
                if regex_valid_colorstyle_file.findall(row['filename']):
                    ## inserts only, not updates, will create multiple records if exists already
                    insert_filerecord_pymongo(database_name=database_name, collection_name=collection_name, batchid=batchid, colorstyle=colorstyle, alt=alt, format=format, timestamp=timestamp)
                    print "Successful Insert to uploads_imagedrop {0} --> {1}".format(k,v)
                else:
                    pass


if __name__ == '__main__':
    import os,sys
    dirname = ''
    function = ''
    try:
        dirname = sys.argv[1]
    except IndexError:
        pass
    try:
        function = sys.argv[2]
    except IndexError:
        pass
    if function == 'update':
        main_update(dirname=dirname)
    elif function == 'insert':
        main(dirname=dirname)
    else:
        main(dirname=dirname)