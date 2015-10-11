#!/usr/bin/env python
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
    book = xlrd.open_workbook(workbk)
    sh = book.sheet_by_index(0)
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
            except AttributeError:
                pass
    return d

############################################

import sys,os

workbk = xlfile

outdict = readxl_outputdict(workbk)
compiled_rows = compile_outdict_by_rowkeys(outdict)

#for k,v in compiled_rows.iteritems():
#    for val in v:
#        print k,val,v[val]
#

import os, urllib2, urllib
for k,v in compiled_rows.items():
    rootdir = os.path.abspath('.')
    if v['MainImageURL'] == 'MainImageURL':
        pass
    else:
            
        bfly = v['bfly']
        bfly = int(float(bfly))
        bfly = str(bfly)
        vendor = v['SKU']
        main = v['MainImageURL']
        alt1 = v['OtherImageURL1']
        alt2= v['OtherImageURL2']
        try:
            error_check = urllib.urlopen(main)
            urlcode_value = error_check.getcode()
            dest = os.path.join(rootdir,bfly+"_1"+".jpg")
            
            if urlcode_value == 200:
                r = urllib2.urlopen(main)
                f = open(dest,'wb')
                f.write(r.read())
                f.close()
                print "wget -O {1} {0}".format(main, dest)
        except IOError:
            pass
        try:
            error_check = urllib.urlopen(alt1)
            urlcode_value = error_check.getcode()
            dest = os.path.join(rootdir,bfly+"_2"+".jpg")
            
            if urlcode_value == 200:
                r = urllib2.urlopen(alt1)
                f = open(dest,'wb')
                f.write(r.read())
                f.close()
                print "wget -O {1} {0}".format(alt1, dest)
        except IOError:
            pass
        try:
            error_check = urllib.urlopen(alt2)
            urlcode_value = error_check.getcode()
            dest = os.path.join(rootdir,bfly+"_2"+".jpg")
            
            if urlcode_value == 200:
                r = urllib2.urlopen(alt2)
                f = open(dest,'wb')
                f.write(r.read())
                f.close()
                print "wget -O {1} {0}".format(alt2, dest)
        except IOError:
            pass
        
