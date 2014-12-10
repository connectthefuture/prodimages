#!/usr/bin/env python
# -*- coding: utf-8 -*-

def parse_upload_log_files_indir(dirname=None):
    import re, datetime, glob, os
    #dirname =  '/Users/johnb/Dropbox/DEVROOT/mnt/Post_Complete/ImageDrop/bkup' ##'/Users/johnb/Dropbox/DEVROOT/mnt/Post_Complete/ImageDrop/bkup'
    regex_textfile = re.compile(r'^(/.+?/)(LSTransfer)(\d{12})(\.txt)$')
    regex_datarow  = re.compile(r'^(/.+?/)(LSTransfer)(\d{12})(\.txt)$')
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
            page += 1
    return data


def insert_filerecord_pymongo(database_name=None, collection_name=None, batchid=None, colorstyle=None, alt=None, format=None, timestamp=None):
    # Insert a New Document
    import pymongo
    mongo = pymongo.Connection('127.0.0.1')
    mongo_db = mongo[database_name]
    mongo_collection = mongo_db[collection_name]

    # Returns the '_id' key associated with the newly created document
    new_insertobj_id = mongo_collection.insert({'colorstyle': colorstyle,'format': format,'batchid': batchid,'alt': alt, 'upload_ct': 1,'timestamp': timestamp})
    #    new_insertobj_id = mongo_collection.insert({'colorstyle': colorstyle,'format': format,'batchid': batchid,'alt': alt, 'upload_ct': 1,'timestamp': timestamp})
    #new_insertobj_id = mongo_collection.insert({'colorstyle': colorstyle,'format': format,'batchid': batchid,'alt': alt, 'upload_ct': 1,'timestamp': timestamp}, continue_on_error=True, upsert=True)
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

    key = {'colorstyle': colorstyle}  #, 'alt': alt, 'upload_ct': 1}
    #data = { "$set":{'format': format,'batchid': batchid,'alt': alt, upload_ct: 1,'timestamp': timestamp}},
    datarow = {'colorstyle': colorstyle, 'format': format,'batchid': batchid,'alt': alt, 'upload_ct': 1,'timestamp': timestamp}
    key_str = key.keys()[0]
    check = mongo_collection.find({key_str: colorstyle}).count()
    if check == 1:
        print 'REFRESH IT ', check
        data = { "$set":{
                        'colorstyle': colorstyle,
                        'alt': {'$min': {'alt': alt}},
                        'format': format,
                        'batchid': batchid,
                        #'upload_ct':
                        '$inc': {'upload_ct': 1},
                        'timestamp': { '$max': {'timestamp': timestamp}}
                        }
                    }
        return check
    else:
        print 'NEW IT ', check
        data = { "$set":{'format': format,'batchid': batchid,'alt': alt, 'upload_ct': 1,'timestamp': timestamp}}
        #mongo_collection.create_index([("colorstyle", pymongo.ASCENDING)], unique=True, sparse=True, background=True)
    mongo_collection.create_index("colorstyle", unique=True, sparse=False, background=True)
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
    #data = { "$set":{'format': format,'batchid': batchid,'alt': alt, 'upload_ct': 1,'timestamp': timestamp}},
    data = {'colorstyle': colorstyle, 'format': format,'batchid': batchid,'alt': alt, 'upload_ct': 1,'timestamp': timestamp}
    results = mongo_collection.find({key: colorstyle}).count()
    #return count of styles with the number found
    return results


def check_running_process(check_process_name=None, kill_found_procs=False):
    import psutil, re, os
    regex_pyfile = re.compile(r'^.+?\.py[c]?.*?$')
    if check_process_name:
        pass
    else:
        check_process_name = os.path.abspath(__file__).split('/')[-1]
    procnames=[]
    for p in list(psutil.process_iter()):
        try:
            if p.exe():
                procnames.append(p.cmdline())
            else:
                pass
        except:
            pass

    #procnames = sorted(procnames)
    found_conflicts_bypid = []
    for proc in procnames:
        if len(proc) > 1:
            script_name = [ p for p in proc if regex_pyfile.findall(p) ] #.split('/')[-1]
            print script_name
            try:
                if script_name:
                    if os.path.abspath(script_name[0]) ==  os.path.abspath(__file__):
                        found_conflicts_bypid.append(script_name[0])
                else:
                    pass
            except IndexError:
                pass
        else:
            pass

    # if not kill_found_procs:
    #     return found_conflicts_bypid
    # else:
    #     ## kill them
    #return found_conflicts_bypid
    return found_conflicts_bypid


        # regex_proc_check = re.compile(check_process_name)
        # try:
        #     pdict      = p.as_dict()
        #     procname   = pdict['name']
        #     procuser   = pdict['username']
        #     procstatus = pdict['status']
        #     if regex_proc_check.findall(procname) and procuser == 'root':
        #         print procname,  procuser, procstatus
        #         found_conflicts_bypid.append(pdict['pid'])
        #     else:
        #         pass
        # except:
        #     pass
    


## Perform the Insert to mongodb
#uploads_imagedrop.find({'colorstyle': colorstyle, 'app_config_id':{'$in':app_config_ids}})
#expr = { "$or": [ {"uploads_imagedrop": { "$exists": False }}, {"colorstyle": colorstyle}]}

#for c in collection_name.find(expr):
#    print [ k.upper() for k in sorted(c.keys()) ]


def main_check(datarow=None):
    import sys,os,re, sqlalchemy, json
    regex_uploadlogs = re.compile(r'^.*?/Post_Complete/ImageDrop/bkup/LSTransfer.+?\.[txtTXT]{3}$')
    regex_valid_colorstyle_file = re.compile(r'^(.*?/?)?.*?([0-9]{9})(_alt0[1-6])?(\.[jpngJPNG]{3})?$')
    database_name = 'images'
    collection_name = 'uploads_imagedrop'
    if regex_valid_colorstyle_file.findall(datarow['filename']):
        ## inserts only, not updates, will create multiple records if exists already
        check = get_filerecord_pymongo(datarow)  #database_name=database_name, collection_name=collection_name, batchid=batchid, colorstyle=colorstyle, alt=alt, format=format, timestamp=timestamp)
        if check >= 1:
            #print "Successful Insert to uploads_imagedrop {0} --> {1}".format(k,v)
            return True, check
        else:
            return False, check


def main_update(dirname=None):
    import sys,os,re, sqlalchemy, json, pymongo
    regex_uploadlogs = re.compile(r'^.*?/Post_Complete/ImageDrop/bkup/LSTransfer.+?\.[txtTXT]{3}$')
    regex_valid_colorstyle_file = re.compile(r'^(.*?/?)?.*?([0-9]{9})(_alt0[1-6])?(\.[jpngJPNG]{3})?$')
    if not dirname:
        try:
            dirname = sys.argv[1]
        except:
            dirname = '/mnt/Post_Complete/ImageDrop/bkup'
    ## Take the compiled k/v pairs and Format + Insert into Mongo DB
    transfer_batches = parse_upload_log_files_indir(dirname=dirname)
    #try:sorted(data, reverse=True)
    
    for batch in sorted(transfer_batches.values(), reverse=True):
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
                    try:
                        update_filerecord_pymongo(database_name=database_name, collection_name=collection_name, batchid=batchid, colorstyle=colorstyle, alt=alt, format=format, timestamp=timestamp)
                        print "Successful Insert to uploads_imagedrop {0} --> {1}".format(k,v)
                    except pymongo.errors.ConnectionFailure:
                        import time
                        time.sleep(5)
                        pass


                else:
                    pass
    #except StopIteration:
        #print "Successful Batch Update Completed uploads_imagedrop..."


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
