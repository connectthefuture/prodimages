#!/usr/bin/python
def csv_write_datedOutfile(lines):
    import csv,datetime,os
    dt = str(datetime.datetime.now())
    today = dt.split(' ')[0]
    f = os.path.join(os.path.expanduser('~'), today + '_write.csv')
    for line in lines:
        with open(f, 'ab+') as csvwritefile:
            writer = csv.writer(csvwritefile, delimiter=',')
            writer.writerows([lines])


def readxl_outputdict(workbk=None):         
    import csv,xlrd,sys
#    workbk = sys.argv[1]
    book = xlrd.open_workbook(workbk)##sys.argv[1])
    sh = book.sheet_by_index(0)

    #convWriter = csv.writer(sys.stdout,delimiter=',', dialect='excel')
    numcols=sh.ncols
    outdict = {}
    for rx in xrange(sh.nrows):
        rowdict = {}    
        for cx in xrange(sh.ncols):
            rowhead = sh.cell_value(rowx=0,colx=cx)
            rowval = sh.cell_value(rowx=rx,colx=cx)
            rowdict[rowhead] = rowval
            outdict[rx] = rowdict
    return outdict


def compile_outdict_by_rowkeys(outdict):
    from collections import defaultdict
    d = defaultdict(list)
    for r in outdict.items():
        dd = defaultdict(dict)
        for val in r[1].items():
            try:
                print r[0],val[0],val[1]
                dd[val[0]]=val[1]
                d[r[0]] = dd
                #csv_write_datedOutfile(lines.encode('ascii', 'replace'))
            except AttributeError:
                pass
    return d

############################################

import sys,os
xlfile=sys.argv[1]

workbk = xlfile

outdict = readxl_outputdict(workbk)
compiled_rows = compile_outdict_by_rowkeys(outdict)

for k,v in compiled_rows.iteritems():
    for val in v:
        print k,val,v[val]


import os, urllib
for row in compiled_rows.items():
    rootdir = os.path.abspath('.')
    bfly = row['bfly']
    vendor = row['SKU']
    main = row['MainImageURL']
    alt1 = row['OtherImageURL1']
    alt2= row['OtherImageURL2']
    try:
        error_check = urllib.urlopen(main)
        urlcode_value = error_check.getcode()
        print urlcode_value
        
        ### PRIMARY URL, AKA /Z/
        if urlcode_value == 200:
            urllib.urlretrieve(main, os.path.join(rootdir,bfly+"_1"+".jpg"))
    except:
        pass
    try:
        error_check = urllib.urlopen(alt1)
        urlcode_value = error_check.getcode()
        print urlcode_value
        
        ### PRIMARY URL, AKA /Z/
        if urlcode_value == 200:
            urllib.urlretrieve(alt1, os.path.join(rootdir,bfly+"_2"+".jpg"))
    except:
        pass
    try:
        error_check = urllib.urlopen(alt12)
        urlcode_value = error_check.getcode()
        print urlcode_value
        
        ### PRIMARY URL, AKA /Z/
        if urlcode_value == 200:
            urllib.urlretrieve(alt12, os.path.join(rootdir,bfly+"_3"+".jpg"))
    except:
        pass
        
