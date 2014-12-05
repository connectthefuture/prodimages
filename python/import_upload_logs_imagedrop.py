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

def main(dirname=None):
    import sys,os,re, sqlalchemy, json
    regex_uploadlogs = re.compile(r'^.*?/Post_Complete/ImageDrop/bkup/LSTransfer.+?\.[txtTXT]{3}$')
    regex_valid_colorstyle_file = re.compile(r'^(.*?/?)?.*?([0-9]{9})(_alt0[1-6])?(\.[jpngJPNG]{3})?$')
    if not dirname:
        try:
            dirname = sys.argv[1]
        except:
            dirname = '/mnt/Post_Complete/ImageDrop/bkup'
    ## Take the compiled k/v pairs and Format + Insert into MySQL DB
    transfer_batches = parse_upload_log_files_indir(dirname=dirname)
    #transfer_batches = [ r for r in transfer_batches if r  ]
    try:
        for batch in transfer_batches:
            database_name = 'images'
            collection_name = 'uploads_imagedrop'
            for row in batch:
                print row
                for k,v in row.items():
                    batchid = row['batchid']
                    colorstyle = row['colorstyle']
                    alt = row['alt']
                    format = row['format']
                    timestamp = row['timestamp']
                    query_insert =   """INSERT INTO imagesimagedrop (batchid, colorstyle, alt, format, timestamp) VALUES (%s, %s, %i, %s, %d)""", batchid, colorstyle, alt, format, timestamp
                    print query_insert
                    try:
                        ##mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
                        mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
                        connection = mysql_engine.connect()
                        if regex_valid_colorstyle_file.findall(row['filename']):
                            connection.execute(query_insert)
                            print "Successful Insert to uploads_imagedrop {0} --> {1}".format(k,v)
                        else:
                            print "Database Table not Found for Inserting {0} --> {1}".format(k,v)
                    except sqlalchemy.exc.IntegrityError:
                        print "Duplicate Entry {0} --> {1}".format(k,v)
                        pass
    except AttributeError:
        pass

if __name__ == '__main__':
    main()
