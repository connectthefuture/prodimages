#!/usr/bin/env python
# -*- coding: utf-8 -*-

def parse_upload_log_files_indir(dirname=None):
    import re, datetime, glob, os
    dirname =  '/Users/johnb/Dropbox/DEVROOT/mnt/Post_Complete/ImageDrop/bkup' ##'/Users/johnb/Dropbox/DEVROOT/mnt/Post_Complete/ImageDrop/bkup'
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
                    insertrow['batch_id'] = ts
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


def insert_filerecord_pymongo_uploads_datatrack(database_name=None, collection_name=None, batch_id=None, colorstyle=None, alt=None, format=None, timestamp=None):
    # Insert a New Document
    import pymongo
    mongo = pymongo.Connection('127.0.0.1')
    mongo_db = mongo[database_name]
    mongo_collection = mongo_db[collection_name]
    # Returns the '_id' key associated with the newly created document

    new_insertobj_id = mongo_collection.insert({'colorstyle': colorstyle,
                                                 'format': format,
                                                 'batch_id': batch_id,
                                                 'alt': alt,
                                                 'timestamp': timestamp
                                                })
    print "Inserted: {0}\nImageNumber: {1}\nFormat: {2}\nID: {3}".format(colorstyle,alt, format,new_insertobj_id)
    return new_insertobj_id


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

import pymongo
def save(data):
    coll.insert(data)

def fetch(id):
    return coll.find_one({"id": id } )

#conn = pymongo.Connection('mongodb://tutorial-test:u3ZYh136@ds029187.mongolab.com:29187/tutorial-test')
conn = pymongo.Connection('mongodb://127.0.0.1:27017/data_images')

db = conn['tutorial-test']
db.test_collection.insert({})
db.test_collection.find()
list(db.test_collection.find())


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
    transfer_batches = parse_upload_log_files_indir()
    for batch in transfer_batches:
        database_name = 'data_images'
        collection_name = 'uploads_imagedrop'
        for row in batch:
            print row
            for k,v in row.items():
                ## Build object of key/values for insert
                batch_id = row['batch_id']
                colorstyle = row['colorstyle']
                alt = row['alt']
                format = row['format']
                timestamp = row['timestamp']
                ## Perform the Insert to mongodb
                #uploads_imagedrop.find({'colorstyle': colorstyle, 'app_config_id':{'$in':app_config_ids}})
                expr = { "$or": [ {"uploads_imagedrop": { "$exists": False }}, {"colorstyle": colorstyle}]}

                for c in collection_name.find(expr):
                    print [ k.upper() for k in sorted(c.keys()) ]
                if regex_valid_colorstyle_file.findall(row['filename']):
                    insert_filerecord_pymongo_uploads_datatrack(database_name=database_name, collection_name=collection_name, batch_id=batch_id, colorstyle=colorstyle, alt=alt, format=format, timestamp=timestamp)
                    #print "Successful Insert to uploads_imagedrop {0} --> {1}".format(k,v)
                else:
                    pass


if __name__ == '__main__':
    main()