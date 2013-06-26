# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 21:36:12 2013

@author: JCut
"""

#from sys import * 
#from os import * 
import os
import sys
import readline 
import rlcompleter
import atexit
import csv
import glob
import collections
readline.parse_and_bind("tab: complete")
import sqlalchemy
#import MySQLdb

"""
Initial Directory Variables to Set at Start
"""
dir_homedir 	        = os.path.expanduser('~') 
dir_zimages 	        = os.path.abspath("/mnt/Post_Ready/zImages_1")
dir_pushfashion 	    = os.path.abspath("/mnt/Post_Ready/eFashionPush")
dir_pushstill 	        = os.path.abspath("/mnt/Post_Ready/aPhotoPush")
dir_sites 	            = os.path.abspath("/mnt/Post_Ready/zProd_Server/imageServer7/sites") 
dir_apps 	            = os.path.abspath("/mnt/Dropbox/Apps") 
dir_consig 	            = os.path.abspath("/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment")
dir_datacsv             = os.path.abspath("/mnt/Post_Ready/zProd_Server/imageServer7/data/csv")
dir_dboxapps 		    = os.path.abspath('/Users/johnb/Dropbox/Apps')
wild_csvI7files         = os.path.join(dir_datacsv, "*.csv")
wild_jpgZImgfiles       = os.path.join(dir_zimages, "*/*.jpg")
glob_csvI7files         = glob.glob(wild_csvI7files)
glob_jpgZImgfiles       = glob.glob(wild_jpgZImgfiles)


# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 22:38:40 2013

@author: JCut

FUNCTION DEFINITIONS
"""

"""
Return Date Formatted for Inserting to MySQL db
"""
def dateMysql(date):
    date = {}
    import datetime
    from string import Formatter    
    dt = unicode(datetime.datetime.today())
    ##print dt
    Formatter()
    date = '{:.10}'.format(dt)
    return date



"""
Return Exif info to KeyValue Array
"""
def get_exif(fn):
    
    ret = {}
    from PIL import Image
    from PIL.ExifTags import TAGS
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret
    


"""
Write a Text file of input -- File Named as Today Date to Pictures folder on Linux And OSX
"""    
def writeFile(fn,outfilename):
    #ret = {}
    from datetime import datetime
    from string import Formatter    
    from os import path
    dt = unicode(datetime.today())
    print dt
    Formatter()
    date = '{:.10}'.format(dt)
    print date    
    dir_homedir = path.expanduser('~')
    
    myfile = unicode(path.join(dir_homedir, 'Pictures/' + outfilename + '-' + date + '.txt'))   
    #frd  = file()
    print myfile    
    #fwrt = file(myfile, 'w+')     
    wrt = open(myfile, 'w+')
    for line in fn:
        sline = str(line)
        print sline
        wrt.write(sline + '\n')
    wrt.close
    
    
    
"""
Glob or Reg Search Dir for CSV output as:
    filename(ie.style),photo_date(ie.createdate),file_location(url or filepath)

"""

def outputExifCsvGlob(listDirGlob):
    ret = {}
    from PIL import Image
    from PIL.ExifTags import TAGS
    for fn in listDirGlob:
        i = Image.open(fn)
        info = i._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
    return ret

def dateCreateFix(fndir):
    import datetime, os
    ret = {}
    for fn in fndir:
        info = os.stat(fn)
        ctime = info[9]
        d = datetime.date.fromtimestamp(ctime)
        d = d.isocalendar(datetime.date.fromtimestamp(d))
        d = d.strftime("%Y-%m-%d")
    return ret

"""
Query Mysql DB using 2 attribs. Filed(ie. 'colorstyle', param(ie.'302332901'))
"""
def sqlQueryStyles(searchField,searchParam):
    import sqlalchemy
    #import os
    #import sys
    #import csv
    #ret = {}
    ##  Create Sql Engine and Connection Obj -- Connected  --- 
    ##  Includes local replicated server & remote connections
    #engine = sqlalchemy.create_engine('mysql://root:root@192.168.21.111:3301/data_imagepaths')
    
    engine = sqlalchemy.create_engine('mysql://root:root@localhost/data_imagepaths')
    connection = engine.connect()

    ## Create Query
    #querymake = "select * from product_snapshot where " + searchField + " like %" + searchParam + "%"
    querymake = "select * from product_snapshot where " + searchField + " = " + searchParam
    
    engine = sqlalchemy.create_engine('mysql://root:root@192.168.21.111:3301/data_imagepaths')
    #querymake = "select * from " + searchtable + " where " + searchField + " = " + searchParam
    #result = connection.execute("select * from product_snapshot where brand = 'Gucci'")
    result = connection.execute(querymake)

    ### Print Results of Query
    for row in result:
        print "colorstyle:",        row['colorstyle']
        print "production status:", row['production_status']
        print "brand:",             row['brand']
        print "sample status:",     row['sample_status']
        print "sample date:",       row['status_dt']
    connection.close()
    #return ret
"""
Query EVENTS Mysql DB using 2 attribs. Filed(ie. 'colorstyle', param(ie.'302332901'))
"""
def sqlQueryEvents(searchtable,searchField,searchParam):
    import sqlalchemy
    #import os
    #import sys
    #import csv
    #ret = {}
    ##  Create Sql Engine and Connection Obj -- Connected  --- 
    ##  Includes local replicated server & remote connections
    #engine = sqlalchemy.create_engine('mysql://root:root@192.168.21.111:3301/data_imagepaths')
    engine = sqlalchemy.create_engine('mysql://root:root@192.168.21.111:3301/data_imports')
    connection = engine.connect()

    ## Create Query
    #querymake = "select * from product_snapshot where " + searchField + " like %" + searchParam + "%"
  
    querymake = "select * from " + searchtable + " where " + searchField + " = " + searchParam
    #result = connection.execute("select * from product_snapshot where brand = 'Gucci'")
    result = connection.execute(querymake)
    rowsss = {}
    ### Print Results of Query
    for row in result:
        print "colorstyle:",        row['colorstyle']
        print "event group:",       row['event_group']        
        print "event id:",          row['event_id']
        print "event title:",       row['event_title']        
        print "event start:",       row['ev_start']
        #print "production status:", row['production_status']        
        
    connection.close()
    return rowsss
    
    
    

def sqlQueryEventsUpcoming():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_eventscal = "select atg_snp.event.id, atg_snp.event.start_date, atg_snp.event.event_description from atg_snp.event where atg_snp.event.start_date >= trunc(sysdate) order by start_date desc"
    result = connection.execute(querymake_eventscal)
    events = {}
    for row in result:
        event = {}        
        event['ID'] = row['ID']
        event['START_DATE'] = row['START_DATE']
        event['EVENT_DESCRIPTION'] = row['EVENT_DESCRIPTION']
        events[row['ID']] = event
        
    print events
    connection.close()
    return events
    
    
def csv_read_file(filename, delim):
    with open(filename, 'rb') as f:
            dialect = csv.Sniffer().sniff(f.read(1024))
            reader = csv.reader(f, delimiter=delim, dialect=dialect)
            for lines in reader:
                for col in lines:
                    print col[1]
                    #source = l[1]
                    #dest   = l[2]
                #os.rename(source, dest)
                    



import csv
import os
import sys


homedir = os.path.expanduser("~")
csvfile = os.path.join(homedir, "2013-03-25_write.csv")

print csvfile

#pathtocsv = os.path.join(os.path.expanduser('~'), csvfile)

def csv_readfile(csvfile):
    with open(csvfile, 'rb') as f:
        readfile = csv.reader(f, delimiter=",")
        rows = []
        for row in readfile: 
            rows.append(row)
        return list(rows)

regex_url = '/^(((http|https|ftp):\/\/)?([[a-zA-Z0-9]\-\.])+(\.)([[a-zA-Z0-9]]){2,4}([[a-zA-Z0-9]\/+=%&_\.~?\-]*))*$/'




pattern = re.compile(r'___REGEX&?+*___')
for f in listdir(dir_homedir):
     fpath = os.path.abspath(f)
     re.findall(pattern, fpath)


for f in globcsvfiles:
    print f
    #test_file = f
    #csv_file = csv.DictReader(open(f, 'rb'), delimiter=',', quotechar='"')
    #it = iter(f)
    d = dict()
    with open(f, 'rb') as ff:
        for lines in enumerate(ff):
            string.Formatter()
            print '{:1.9}'.format(lines)
            print lines
#   reader = csv.DictReader(open(csv_file, 'rt'), delimiter=',', quotechar='"')
#        ret = {}
#        #print lines
#        print '\n'.join(it)
#        print ret
        #print line
 #!/usr/bin/python