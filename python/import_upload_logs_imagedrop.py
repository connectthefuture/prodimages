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


def main(dirname=None):
    import sys,os,re, sqlalchemy
    if not dirname:
        try:
            dirname = sys.argv[1]
        except:
            dirname = '/mnt/Post_Complete/ImageDrop/bkup'
    ## Take the compiled k/v pairs and Format + Insert into MySQL DB
    transfer_batches = parse_upload_log_files_indir()
    #[ r for r in transfer_batches.items() if r  ] 
    for batch in transfer_batches:
        for row in batch:
            print row
            for k,v in row.items():
                batch_id = row['batch_id']
                colorstyle = row['colorstyle']
                alt = row['alt']
                format = row['format']
                timestamp = row['timestamp']
                x =   """INSERT INTO uploads_imagedrop (batch_id, colorstyle, alt, format, timestamp) VALUES (%s, %s, %i, %s, %d)""", batch_id, colorstyle, alt, format, timestamp
                print x

                try:
                    ##mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
                    mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
                    connection = mysql_engine.connect()
                    regex_uploadlogs = re.compile(r'^.*?/Post_Complete/ImageDrop/bkup/LSTransfer.+?\.[txtTXT]{3}$')
                    regex_valid_colorstyle_file = re.compile(r'^(.*?)/.*?([0-9]{9})(_alt0[1-6])?(\.[jpngJPNG]{3})?$')

                    if re.findall(regex_consigConvertedPNG, sqlinsert_choose_test):
                        connection.execute("""INSERT INTO uploads_imagedrop (batch_id, colorstyle, alt, format, timestamp) VALUES (%s, %s, %i, %s, %d)""", batch_id, colorstyle, alt, format, timestamp)
                        print "Successful Insert uploads_imagedrop --> {0}".format(k)

                    else:
                        print "Database Table not Found for Inserting {0}".format(k)
                #except OSError:
                except sqlalchemy.exc.IntegrityError:
                    print "Duplicate Entry {0}".format(k)
                    pass


if __name__ == '__main__':
    main()