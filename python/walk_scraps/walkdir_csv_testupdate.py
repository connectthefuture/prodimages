#!/usr/bin/env python

###
## Walk Root Directory and Return List or all Files in all Subdirs too
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
    walkedset = list(set(sorted(walkedlist)))
    return walkedset


###
## Extract All Metadata from Image File as Dict
def get_exif(file_path):
    from PIL import Image
    from PIL.ExifTags import TAGS
    exifdata = {}
    im = Image.open(file_path)
    info = im._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        exifdata[decoded] = value
    return exifdata


###
## Make Lowres Thumnails from Image files or Directory Full of Image Files
def make_lowres_thumbnails_dir_or_singlefile(pathname):
    from PIL import Image
    import glob, os, re
    size = 600, 720
    regex_jpeg = re.compile(r'.+?\.[jpgJPG]{3}$')
#    regex_jpeg_colorstyle = re.compile(r'.+?[0-9]{9}_[1-6][.jpg|.JPG]$')

    if re.findall(regex_jpeg, pathname):
    ## If input variable is a single File Create 1 Thumb
        if os.path.isfile(pathname):
            try:
                infile = os.path.abspath(pathname)
                filename, ext = os.path.splitext(infile)
                im = Image.open(infile)
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(filename , "JPEG")
            except:
                print "Error Creating Single File Thumbnail for {0}".format(infile)
    ## If input variable is a Directory Decend into Dir and Crate Thumnails for all jpgs
        elif os.path.isdir(pathname):
            dirname = os.path.abspath(pathname)
            for infile in glob.glob(os.path.join(dirname, "*.jpg")):
                try:
                    filename, ext = os.path.splitext(infile)
                    im = Image.open(infile)
                    im.thumbnail(size, Image.ANTIALIAS)
                    im.save(filename, "JPEG")
                except:
                    print "Error Creating Thumbnail for {0}".format(infile)

###
## Write Rows to Dated CSV in Users Home Dir If Desired
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
import os,sys,re

rootdir = sys.argv[1]
walkedout = recursive_dirlist(rootdir)

regex = re.compile(r'.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')
#regex = re.compile(r'.+?\.[jpgJPG]{3}$')

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
            try:
                photo_date = get_exif(file_path)['DateTimeOriginal'][:10]
            except KeyError:
                try:
            	    photo_date = get_exif(file_path)['DateTime'][:10]
                except KeyError:
                    photo_date = NULL
            photo_date = photo_date.replace(':','-')
            stylestringsdict_tmp['colorstyle'] = colorstyle
            stylestringsdict_tmp['photo_date'] = photo_date
            stylestringsdict_tmp['file_path'] = file_path
            stylestringsdict_tmp['alt'] = alt
            stylestringsdict[file_path] = stylestringsdict_tmp
            file_path_reletive = file_path.replace('/mnt/Post_Ready/zImages_1/', '/zImages/')
            file_path_reletive = file_path.replace('JPG', 'jpg')
            ## Format CSV Rows
            row = "{0},{1},{2},{3}".format(colorstyle,photo_date,file_path_reletive,alt)
            print row
            stylestrings.append(row)
        except IOError:
            print "IOError on {0}".format(line)
        except AttributeError:
            print "AttributeError on {0}".format(line)

## Write CSV List to dated file for Import to MySQL
#csv_write_datedOutfile(stylestrings)



## Create Dir Struct under ZIMAGES_1 if dir doesnt Exist and copy files to it
for k,v in stylestringsdict.iteritems():
    import os,sys,shutil, re
    regex_zimages = re.compile(r'^.*?/zImages.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')
    src = k
## Dont Move or Resize Files found in zImages copy everything else to zImages
    if re.findall(regex_zimages, src):
        pass
    else:
		destdir = os.path.join('/mnt/Post_Ready/zImages_1', v['colorstyle'][:4])
		destfilename = src.split('/')[-1]
		destpath = os.path.join(destdir,destfilename)
		## Test if File Exists in zimage Directory else copy it and resize
		if os.path.isfile(destpath):
			#print "Not Copying Over File {0}".format(destpath)
			pass
		else:
	## Mkdir if not there
			try:
				os.mkdirs(destdir)
			except:
				pass
	## Mk Thumbs Then move thumbs to Destdir
			try:
				make_lowres_thumbnails_dir_or_singlefile(src)
				successthumb = "Created Thumbnail --> {0}".format(src)
				csv_write_datedOutfile(successthumb)
	## Success on Thumb Creation Now Move to Dest Dir
				try:
					src = os.replace('.jpg', '.jpeg')
					os.rename(src,destpath)
					success = "Success Moving {0} --> {1}".format(src,destpath)
					#print success
					csv_write_datedOutfile(success)
				except:
					errthumb = "Error Moving {0} --> {0}".format(src,destpath)
					print errthumb
					csv_write_datedOutfile(errthumb)
			except:
				errthumb = "Error Creating Thumbnail for {0}".format(src)
				print errthumb
				csv_write_datedOutfile(errthumb)


#Iterate through Dict of Walked Directory, then Import to MySql DB
import sqlalchemy

## First compile the SQL Fields as key value pairs
fulldict = {}
for k,v in stylestringsdict.iteritems():
    dfill = {}
    dfill['colorstyle'] = v['colorstyle']
    dfill['photo_date'] = v['photo_date']
    file_path = k
    file_path = file_path.replace('/mnt/Post_Ready/zImages_1/', '/zImages/')
    file_path = file_path.replace('/mnt/Post_Ready/Retouch_', '/Retouch_')
    dfill['file_path'] = file_path
    dfill['alt'] = v['alt']
    fulldict[k] = dfill


## Take the compiled k/v pairs and Format + Insert into MySQL DB
for k,v in fulldict.iteritems():
    try:

        mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
        #connection = mysql_engine.connect()
        
        mysql_engine.echo = False  # Try changing this to True and see what happens
        metadata = BoundMetaData(mysql_engine)
        
        push_photoselects = Table('push_photoselects', metadata, autoload=True)

        i = push_photoselects.insert()
        i.execute(colorstyle=colorstyle, photo_date=photo_date, file_path=file_path, alt=alt)
        
        
        ## Test File path String to Determine which Table needs to be Updated Then Insert SQL statement
        sqlinsert_choose_test = v['file_path']
        regex_photoselects = re.compile(r'^/mnt/Post_Ready/.+?Push/.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')
        regex_postreadyoriginal = re.compile(r'^/Retouch_.+?/.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')
        regex_zimages = re.compile(r'^/zImages.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')

        if re.findall(regex_photoselects, sqlinsert_choose_test):
            connection.execute("""INSERT INTO push_photoselects (colorstyle, photo_date, file_path, alt) VALUES (%s, %s, %s, %s)""", v['colorstyle'], v['photo_date'], v['file_path'],  v['alt'])
            print "Successful Insert Push_Photoselecs --> {0}".format(k)

        elif re.findall(regex_postreadyoriginal, sqlinsert_choose_test):
            connection.execute("""INSERT INTO post_ready_original (colorstyle, photo_date, file_path, alt) VALUES (%s, %s, %s, %s)""", v['colorstyle'], v['photo_date'], v['file_path'],  v['alt'])
            print "Successful Insert to Post_Ready_Originals --> {0}".format(k)

        elif re.findall(regex_zimages, sqlinsert_choose_test):
            connection.execute("""INSERT INTO zimages1_photoselects (colorstyle, photo_date, file_path, alt) VALUES (%s, %s, %s, %s)""", v['colorstyle'], v['photo_date'], v['file_path'],  v['alt'])
            print "Successful Insert to Zimages --> {0}".format(k)

        else:
            print "Database Table not Found for Inserting {0}".format(k)

    except sqlalchemy.exc.IntegrityError:
        print "Duplicate Entry {0}".format(k)

    #for vals in v:
    #    print v[vals]

        #push_photoselects = Table('push_photoselects', mysql_engine)
        #i = push_photoselects.insert()
#sql = "INSERT INTO data_imagepaths.push_photoselects (colorstyle, photo_date, file_path, alt) VALUES (%('" + colorstyle + "')s,%('" + photo_date + "')d,%('" + file_path + "')s,%(('" + alt + "'))s"
#print sql
#
#
#class PhotoMetaData(f):
#
#    def __init__(self, f):
#        #self.files_list = []
##       self.recursivefilelist = []
#        self.MetaDict = {}
#        self.f = f
##       self.__update(directory)
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
