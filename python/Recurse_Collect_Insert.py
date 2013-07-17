import threading, zipfile, os, re, sys

class ExifPhotoData:
    def __init__(self, f, **kargs):
        self.f = f
        self.exifdict = {}
    #self.dtodict = {}
    #self.directory = directory
    #self.allfoundlist = allfoundlist
    #@staticmethod
    def get_exif(self):
        from PIL import Image
        from PIL.ExifTags import TAGS
        try:
            i = Image.open(self.f)
            info = i._getexif()
            self.exifdict = {}
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                self.exifdict[decoded] = value
        except IOError:
            print 'IO No File Exists: {0}'.format(self)
        
        return self.exifdict

class RecurseDir:
    def __init__(self, directory, **kargs):
        self.directory = directory
        self.exifdict = {}
        self.allfound = []
        self.listingdict = {}
    
    
    def recurse_dir_list(self):
        import os,sys,re
        __filepaths = {}
        for dirpath,subdir,files in os.walk(self.directory):
            for f in files:
                __filepaths[dirpath] = files[:]
        #print filepaths
        recursivefilelist = []
        for path,files in __filepaths.items():
            for f in files:
                __filepath = "{0}/{1}".format(path,f)
                #print file,path
                
                recursivefilelist.append(__filepath)
                sorted(recursivefilelist)
        #print recursivefilelist
        #print recursivefilelist
        regex = re.compile(r'^.+?[/][0-9]{9}_?[1-6]?.jpg$')
        #regex = re.compile(r'^.+?[.]jpg$')
        self.allfound = []
        for f in recursivefilelist:
            foundjpgs = re.findall(regex,f)
            if foundjpgs:
                self.allfound.append(f)
        return self.allfound
    
    def photodatedict(self):
        self.listingdict = {}
        for f in self.allfound:
            ldict = {}
            __exif = ExifPhotoData(f)
            file_path = os.path.abspath(f)
            colorstyle = file_path.split('/')[-1]
            colorstyle = colorstyle.strip('.jpg')
            colorstyle = colorstyle.split('_')[0]
            alt = file_path.split('_')[-1]
            alt = alt.strip('.jpg')
            photodate = __exif.get_exif()['DateTime'][0:10]
            
            ldict['colorstyle'] = colorstyle
            ldict['photo_date'] = photodate.replace(':','-')
            ldict['file_path'] = file_path
            ldict['alt'] = alt
            self.listingdict[file_path] = ldict
        return self.listingdict


def superDicter(allrecinstlistpush):
    superdicts = {}
    for inst in allrecinstlistpush:
        print inst
        inst.recurse_dir_list()
        instdirdatedict = inst.photodatedict()
        for k,v in instdirdatedict.iteritems():
            superdict = {}
            #print v['colorstyle'],v['photodate'],v['file_path'],v['alt']
            superdict['colorstyle'] = v['colorstyle']
            superdict['photo_date'] = v['photo_date']
            superdict['file_path'] = v['file_path']
            superdict['alt'] = v['alt']
            superdicts[v['file_path']] = superdict
    #print len(superdicts)
    return superdicts


def file7_archdir_pushdir_list():
    from Recurse_Collect_Insert import RecurseDir
    
#    recursedirpushstill = '/mnt/Post_Ready/aPhotoPush'
#    recursedirpushfashion = '/mnt/Post_Ready/eFashionPush'
    recursedirarchstill = '/mnt/Post_Ready/Retouch_Still'
    recursedirarchfashion = '/mnt/Post_Ready/Retouch_Fashion'
    
#    allrecinstlistpush = []
    allrecinstlistarch = []
#    recurselistingpushstillinst = RecurseDir(recursedirpushstill)
#    recurselistingpushfashioninst = RecurseDir(recursedirpushfashion)
    recurselistingstillinst = RecurseDir(recursedirarchstill)
    recurselistingfashioninst = RecurseDir(recursedirarchfashion)
    

#    allrecinstlistpush.append(recurselistingpushstillinst)
#    allrecinstlistpush.append(recurselistingpushfashioninst)
    allrecinstlistarch.append(recurselistingstillinst)
    allrecinstlistarch.append(recurselistingfashioninst)
    
    #print allrecinstlistpush
    return allrecinstlistarch
#    return (allrecinstlistpush, allrecinstlistarch)

######    BEGIN COMMANDS FOR EXECUTION    #######################################################


try:
    
    if sys.argv[1]:
        recursedir = sys.argv[1]
        print recursedir
#recurselistinginst = RecurseDir(recursedir)

except IndexError:
    try:
        ## Test whether sys.argv contains Directory to Recurse and list, Else use file7 Img Dirs
        if sys.argv[1]:
            
            ### Call Class Instance
            recurselistinginst = RecurseDir(recursedir)
            
            ## Call recurse func on Class Instance
            recursedirlist = recurselistinginst.recurse_dir_list()
            
            ## Collect Output as Dict
            recursedirdatedict = recurselistinginst.photodatedict()
            
            for k,v in recursedirdatedict.iteritems():
                print v['colorstyle'],v['photo_date'],v['file_path'],v['alt']
    
    except IndexError:
        ## If Dir to Recurse variable NOT set for sys.argv
        ## ## Then run script using file7 Image folders creating/outputting separate lists for Arch vs Push
        allrecinstlistpush = file7_archdir_pushdir_list()
        superDictFinPush = superDicter(allrecinstlistpush)



    for k,v in superDictFinPush.iteritems():
        #from jcbfunx import csv_datedOutFile
        import sqlalchemy #, oursql
        from sqlalchemy import *
        import _mysql
        #kvstring = k,v
        d = {}
        dfill = {}
        dfill['colorstyle'] = v['colorstyle']
        dfill['photo_date'] = v['photo_date']
        fpathstrip = k
        fpathstrip = fpathstrip.replace('/mnt/Post_Ready/', '/')
        dfill['file_path'] = fpathstrip
        dfill['alt'] = v['alt']
        d[k] =  dfill
        #csv_datedOutFile(kvstring)
        #print kvstring
        #d = dict(colorstyle=colorstyle, photo_date=photo_date, file_path=file_path, alt=alt)
        print dfill
        print 'DebuggerLine'
        
        #sql = "INSERT INTO data_imagepaths.push_photoselects (colorstyle, photo_date, file_path, alt) VALUES (%('" + colorstyle + "')s,%('" + photo_date + "')d,%('" + file_path + "')s,%(('" + alt + "'))s"
        #print sql
        try:
            
            mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:root@localhost:3301/data_imagepaths')
            #oursql_engine_connection = oursql.connect(host='127.0.0.1', user='root', passwd='root', db='data_imagepaths', port=3301)
            #push_photoselects = Table('push_photoselects', mysql_engine)
            
            #i = push_photoselects.insert()
            connection = mysql_engine.connect()
            
            #i.execute(dfill)
            
            
            connection.execute("""INSERT INTO push_photoselects (colorstyle, photo_date, file_path, alt) VALUES (%s, %s, %s, %s)""", dfill['colorstyle'], dfill['photo_date'], dfill['file_path'],  dfill['alt'])
        except sqlalchemy.exc.IntegrityError:
            print "Duplicate Entry {0}".format(fpathstrip)
#table_addresses = 'push_photoselects'
#address = Address(colorstyle,photo_date,file_path,alt)
#ins = table.insert()
#connection.execute("INSERT INTO push_photoselects (colorstyle, photo_date, file_path, alt) VALUES (?, ?, ?, ?)", d)

#itwrap = oursql.IterWrapper([colorstyle, photo_date, file_path, alt])
#connection.execute("INSERT INTO 'some_table' VALUES (?, ?, ?, ?)", (itwrap))


#connection.execute(d[colorstyle], d[photo_date], d[file_path], d[alt])
#session.add(address)
#querymake_consig_stylefix="SELECT Distinct POMGR_SNP.SKU.PRODUCT_COLOR_ID AS colorstyle, POMGR_SNP.SKU.SKU_CODE AS sku FROM POMGR_SNP.SKU WHERE POMGR_SNP.SKU.SKU_CODE LIKE '" + sku + "' ORDER by POMGR_SNP.SKU.PRODUCT_COLOR_ID ASC"
#result = connection.execute(querymake_consig_stylefix)