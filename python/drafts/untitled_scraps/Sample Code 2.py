import threading, zipfile, os, re, sys, oursql, sqlalchemy

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
            print 'IO No File Exists: {0}'.format(f)
            
        return self.exifdict

class RecurseDir:
    def __init__(self, directory, **kargs):
        self.directory = directory
        self.exifdict = {}
        self.allfound = []
        self.listingdict = {}
        
        
    def recurse_dir_list(self):
        import os,sys,re
        filepaths = {}
        for dirpath,subdir,files in os.walk(self.directory):
            for f in files:
                filepaths[dirpath] = files[:]
        #print filepaths
        recursivefilelist = []
        for path,files in filepaths.items():
            for f in files:
                filepath = "{0}/{1}".format(path,f)
            #print file,path
            
                recursivefilelist.append(filepath)
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
            import string
            ldict = {}
            exif = ExifPhotoData(f)
            file_path = os.path.abspath(f)
            colorstyle = file_path.split('/')[-1]
            colorstyle = colorstyle.strip('.jpg')
            colorstyle = colorstyle.split('_')[0]
            alt = file_path.split('_')[-1]
            alt = alt.strip('.jpg')
            photodate = exif.get_exif()['DateTime'][0:10]
            
            ldict['colorstyle'] = colorstyle
            ldict['photo_date'] = photodate.replace(':','-')
            ldict['file_path'] = file_path
            ldict['alt'] = alt
            self.listingdict[file_path] = ldict
        return self.listingdict



#from sqlalchemy import Column, Integer, String, Date
#class Address():
#    __tablename__ = 'addresses'
#
#    id = Column(Integer, primary_key=True)
#    colorstyle = Column(String)
#    photo_date = Column(Date)
#    file_path = Column(String)
#    alt = Column(String)
#
#    def __init__(self,colorstyle, photo_date, file_path, alt):
#        self.colorstyle = colorstyle
#        self.photo_date = photo_date
#        self.file_path = file_path
#        self.alt = alt

def superDicter(allrecinstlist):
    superdicts = {}
    for inst in allrecinstlist:
        print inst
        instdirlist = inst.recurse_dir_list()
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
    import RecurseDir

    recursedirpushstill = '/mnt/Post_Ready/aPhotoPush'
    recursedirpushfashion = '/mnt/Post_Ready/aFashionPush'
    recursedirarchstill = '/mnt/Post_Ready/Retouch_Still'
    recursedirarchfashion = '/mnt/Post_Ready/Retouch_Fashion'
    
    allrecinstlistpush = []
    allrecinstlistarch = []
    recurselistingpushstillinst = RecurseDir(recursedirpushstill)
    recurselistingpushfashioninst = RecurseDir(recursedirpushfashion)
    #recurselistingstillinst = RecurseDir(recursedirarchstill)
    #recurselistingfashioninst = RecurseDir(recursedirarchfashion)
    
    #allrecinstlistarch.append(recurselistingstillinst)
    #allrecinstlistarch.append(recurselistingfashioninst)
    allrecinstlistpush.append(recurselistingpushstillinst)
    allrecinstlistpush.append(recurselistingpushfashioninst)
        

    #print allrecinstlistpush
    return allrecinstlistpush
#    return (allrecinstlistpush, allrecinstlistarch)
##################################    BEGIN COMMANDS FOR EXECUTION    ###########################
#testdir='/Users/johnb/Public/Drop_FinalFilesOnly'

try:
    
    if sys.argv[1]:
        recursedir = sys.argv[1]
        print recursedir
        #recurselistinginst = RecurseDir(recursedir)
except IndexError:
    pushDict = file7_archdir_pushdir_list()
    
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
        superDictFinPush = superDicter(allrecinstpush)



    for k,v in superDictFinPush.iteritems():
        #from jcbfunx import csv_datedOutFile
        import sqlalchemy
        #kvstring = k,v
        colorstyle = v['colorstyle']
        photo_date = v['photo_date']
        file_path = k #v['file_path']
        alt = v['alt']
        #csv_datedOutFile(kvstring)
        #print kvstring
        d = dict(colorstyle=colorstyle, photo_date=photo_date, file_path=file_path, alt=alt)
        print d
        #sql = "INSERT INTO data_imagepaths.push_photoselects (colorstyle, photo_date, file_path, alt) VALUES (%('" + colorstyle + "')s,%('" + photo_date + "')d,%('" + file_path + "')s,%(('" + alt + "'))s"
        #print sql
        mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:root@localhost:3301/data_imagepaths')
        oursql_engine_connection = oursql.connect(host='127.0.0.1', user='root', passwd='root',
            db='data_imagepaths', port=3301)
        
        connection = mysql_engine.connect()
        #table_addresses = 'push_photoselects'
        #address = Address(colorstyle,photo_date,file_path,alt)
        #ins = table.insert()
        connection.execute("insert into push_selects(colorstyle, photo_date, file_path, alt) values (?, ?, ?, ?)", d)
        
        itwrap = oursql.IterWrapper([colorstyle, photo_date, file_path, alt])
        curs.execute(
            "INSERT INTO 'some_table' VALUES (?, ?, ?, ?)",
            (itwrap))
        #connection.execute(d[colorstyle], d[photo_date], d[file_path], d[alt])
        #session.add(address)
        #querymake_consig_stylefix="SELECT Distinct POMGR_SNP.SKU.PRODUCT_COLOR_ID AS colorstyle, POMGR_SNP.SKU.SKU_CODE AS sku FROM POMGR_SNP.SKU WHERE POMGR_SNP.SKU.SKU_CODE LIKE '" + sku + "' ORDER by POMGR_SNP.SKU.PRODUCT_COLOR_ID ASC"
        #result = connection.execute(querymake_consig_stylefix)

