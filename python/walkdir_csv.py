#!/usr/bin/env python

##Walk Root Directory and Return List or all Files in all Subdirs too
def recursive_dirlist(rootdir):
    import os
    walkedlist = []
    for dirname, subdirnames, filenames in os.walk(rootdir):
        # append path of all filenames to walkedlist
        for filename in filenames:
            file_path = os.path.abspath(os.path.join(dirname, filename))
            if os.path.isfile(file_path):
                walkedlist.append(file_path)
    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    #if '.git' in dirnames:
    # don't go into any .git directories.
    #    dirnames.remove('.git')
    return walkedlist

def get_exif(filepath):
    from PIL import Image
    from PIL.ExifTags import TAGS
    exifdata = {}
    i = Image.open(filepath)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        exifdata[decoded] = value
    return exifdata

def csv_write_datedOutfile(lines):
    import csv,datetime,os
    dt = str(datetime.datetime.now())
    today = dt.split(' ')[0]
    f = os.path.join(os.path.expanduser('~'), today + '_stylestrings.csv')
    for line in lines:
        with open(f, 'ab+') as csvwritefile:
            writer = csv.writer(csvwritefile, delimiter='\n')
            writer.writerows([lines])

############################ Run ######################################################## Run ############################
############################ Run ######################################################## Run ############################

from PIL import Image
#import pyexiv2
import os,sys,re

rootdir = sys.argv[1]
walkedout = recursive_dirlist(rootdir)

regex = re.compile(r'.+?[.jpg|.JPG]$')

stylestrings = []
stylestringsdict = {}
for line in walkedout:
    stylestringsdict_tmp = {}
    if re.findall(regex,line):
        try:
            file_path = line
            filename = file_path.split('/')[-1]
            colorstyle = filename.split('_')[0]
            alt_ext = file_path.split('_')[-1]
            alt = alt_ext.split('.')[0]
            ext = alt_ext.split('.')[-1]
            photo_date = get_exif(file_path)['DateTimeOriginal'][:10]
            photo_date = photo_date.replace(':','-')

            stylestringsdict_tmp['colorstyle'] = colorstyle
            stylestringsdict_tmp['photo_date'] = photo_date
            stylestringsdict_tmp['file_path'] = file_path
            stylestringsdict_tmp['alt'] = alt
            stylestringsdict[file_path] = stylestringsdict_tmp
            
            ## Format CSV Rows
            row = "{0},{1},{2},{3}".format(colorstyle,photo_date,file_path,alt)
            print row
            stylestrings.append(row)
        except IOError:
            print "IOError on {0}".format(line)


## Write CSV List to dated file for Import to MySQL
#csv_write_datedOutfile(stylestrings)



## Create Dir Struct and copy files to it
for k,v in stylestringsdict.iteritems():
    import os,sys,shutil
    src = k
    destdir = os.path.join('/mnt/Post_Ready/zImages_1', v['colorstyle'][:4])
    destfilename = src.split('/')[-1]
    destpath = os.path.join(destdir,destfilename)
    try:
        os.mkdirs(destdir)
        shutil.copy2(src,destdir)
    except:
        #try:
        shutil.copy2(src,destdir)
        print "Success Copying {0} --> {1}".format(src,destpath)
        #except:
        #    print "Error on {0} --> {1}".format(src,destpath)
        #    pass
        #pass
    


#Import to MySql DB
import sqlalchemy #, oursql
from sqlalchemy import *
import _mysql

fulldict = {}
for k,v in stylestringsdict.iteritems():
    dfill = {}
    dfill['colorstyle'] = v['colorstyle']
    dfill['photo_date'] = v['photo_date']
    fpathstrip = k
    fpathstrip = fpathstrip.replace('/mnt/Post_Ready/zImages_1/', '/zImages/')
    dfill['file_path'] = fpathstrip
    dfill['alt'] = v['alt']
    fulldict[k] =  dfill
    #csv_datedOutFile(kvstring)
    #print kvstring
    #d = dict(colorstyle=colorstyle, photo_date=photo_date, file_path=file_path, alt=alt)
    print dfill
    print 'DebuggerLine'

#sql = "INSERT INTO data_imagepaths.push_photoselects (colorstyle, photo_date, file_path, alt) VALUES (%('" + colorstyle + "')s,%('" + photo_date + "')d,%('" + file_path + "')s,%(('" + alt + "'))s"
#print sql
for k,v in fulldict.iteritems():
    try:
        mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
        #push_photoselects = Table('push_photoselects', mysql_engine)
        #i = push_photoselects.insert()
        connection = mysql_engine.connect()
        #i.execute(dfill)
        connection.execute("""INSERT INTO push_photoselects (colorstyle, photo_date, file_path, alt) VALUES (%s, %s, %s, %s)""", v['colorstyle'], v['photo_date'], v['file_path'],  v['alt'])
    except sqlalchemy.exc.IntegrityError:
        print "Duplicate Entry {0}".format(fpathstrip)    

    #for vals in v:
    #    print v[vals]


#
#
#class PhotoMetaData(f):
#
#    def __init__(self, f):
#        #self.files_list = []
##        self.recursivefilelist = []
#        self.MetaDict = {}
#        self.f = f
##        self.__update(directory)
#
#
#    def get_exif(self,f):
#        from PIL import Image
#        from PIL.ExifTags import TAGS
#        i = Image.open(f)
#        info = i._getexif()
#        exifdict = {}
#        for tag, value in info.items():
#            decoded = TAGS.get(tag, tag)
#            exifdict[decoded] = value
#        return exifdict
#
#
#    def get_photodate_dict(self,f):
#        self.MetaDict = {}
#        for f in rcrsedir:
#            MetaDict = {}
#        try:
#            dtod = {}
#            dto = get_exif(f)['DateTimeOriginal'][0:10]
#            f.split('/')[-1]
#            #dtod['ext'] = fn.split('.')[0]
#            dtod['colorstyle'] = f.split('_')[0]
#            dtod['photo_Date'] = dto
#            dtod['file_path'] = f
#            dtod['alt'] = f.split('_')[-1]
#
#            self.MetaDict[f] = dtod
#
#        except AttributeError:
#            print 'End -- None Type'
#        except IOError:
#            print 'IO Identity Error'
#        except KeyError:
#            print "No Date Time Field"
