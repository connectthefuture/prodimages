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
    return walkedlist


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
## Write Rows to Dated CSV in Users Home Dir If Desired
def csv_write_datedOutfile(lines):
    import csv,datetime,os
    dt = str(datetime.datetime.now())
    today = dt.split(' ')[0]
    f = os.path.join(os.path.expanduser('~'), today + '_stylestrings.csv')
    for line in lines:
        with open(f, 'ab+') as csvwritefile:
            writer = csv.writer(csvwritefile, delimiter='\n')
            writer.writerows(lines)

############################ Run ######################################################## Run ############################
############################ Run ######################################################## Run ############################

from PIL import Image
import os,sys,re,shutil

rootdir = sys.argv[1]
walkedout = recursive_dirlist(rootdir)

regex = re.compile(r'^/.+?\.[a-zA-Z2]{3}$')
regex_india_ready = re.compile(r'^/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/1_Sending/.*?[0-9]{9}\.[pngPNG]{3}$')
regex_india_prezipdir = re.compile(r'^/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/1_Sending/batch_[0-9]{6}/.*?\.[pngPNG]{3}$')
regex_india_prezip = re.compile(r'^/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/1_Sending/batch_[0-9]{6}\.[zipZIP]{3}$')

regex_india_postzip = re.compile(r'^/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/2_Returned/batch_[0-9]{6}\.[zipZIP]{3}$')
regex_india_postzipdir = re.compile(r'^/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/2_Returned/batch_[0-9]{6}/.*?\.[pngPNG]{3}$')

regex_l_uploading = re.compile(r'^/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/3_ListPage_to_Load/.*?[0-9]{9}_l\.[jpgJPG]{3}$')

regex_arch_l_uploded = re.compile(r'^/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/4_Archive/JPG/[0-9]{9}_[LP]\.[jpgJPG]{3}$')
regex_arch_postzip = re.compile(r'^/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/4_Archive/ZIP/batch_[0-9]{6}\.[zipZIP]{3}$')
regex_india_postzipdir = re.compile(r'^/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/4_Archive/PNG/batch_[0-9]{6}/.*?_LP.[pngPNG]{3}$')
#regex = re.compile(r'.+?/.[jpgJPG]{3}$')
outsource_senddir1     = '/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/1_Sending'
outsource_returndir2   = '/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/2_Returned'
outsource_largejpgdir3 = '/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/3_ListPage_to_Load'
outsource_archdir4     = '/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/4_Archive'

stylestrings = []
stylestringsdict = {}
for line in walkedout:
    stylestringsdict_tmp = {}
    if re.findall(regex,line):
        try:
            file_path      = line
            filename       = file_path.split('/')[-1]
            directorypath  = os.path.dirname(file_path)
            zip_groupdir   = directorypath.split('/')[-2]
            colorstyle     = filename[:9]
            ext            = filename.split('.')[-1]
            archivedir     = ext.upper()
            archivehash4   = filename[:4]

            file_path_pre     = os.path.join(outsource_senddir1, archivedir, filename)
            file_path_post    = os.path.join(outsource_returndir2, zip_groupdir, filename)
            file_path_zip  = os.path.join(outsource_senddir1, zip_groupdir)
            file_path_prezip  = os.path.join(outsource_senddir1, zip_groupdir + ext)
            file_path_postzip  = os.path.join(outsource_archdir4, archivedir, zip_groupdir + ext)

#            try:
#                photo_date = get_exif(file_path)['DateTimeOriginal'][:10]
#            except KeyError:
#                try:
#                    photo_date = get_exif(file_path)['DateTime'][:10]
#                except KeyError:
#                    photo_date = 0000-00-00
#            photo_date = photo_date.replace(':','-')

            stylestringsdict_tmp['file_path_pre'] = file_path_pre
            stylestringsdict_tmp['file_path_post'] = file_path_post
            stylestringsdict_tmp['file_path_zip'] = file_path_zip
            stylestringsdict_tmp['file_path_prezip'] = file_path_prezip
            stylestringsdict_tmp['file_path_postzip'] = file_path_postzip
            stylestringsdict_tmp['colorstyle'] = colorstyle
            stylestringsdict_tmp['archivedir'] = archivedir
            stylestringsdict_tmp['zip_groupdir'] = zip_groupdir
            stylestringsdict_tmp['directorypath'] = directorypath
            stylestringsdict[file_path] = stylestringsdict_tmp
#file_path_reletive = file_path.replace('/mnt/Post_Ready/zImages_1/', '/zImages/')
            file_path_reletive = file_path.replace('JPG', 'jpg')
# Format CSV Rows
            row = "{0},{1},{2},{3},{4}".format(colorstyle,zip_groupdir,file_path_pre,file_path_post,file_path_zip)
            print row
            stylestrings.append(row)
        except IOError:
            print "IOError on {0}".format(line)
        except AttributeError:
            print "AttributeError on {0}".format(line)

## Write CSV List to dated file for Import to MySQL
#csv_write_datedOutfile(stylestrings)

#Iterate through Dict of Walked Directory, then Import to MySql DB
import sqlalchemy
## First compile the SQL Fields as key value pairs
fulldict = {}
for k,v in stylestringsdict.iteritems():
    dfill = {}
    dfill['colorstyle'] = v['colorstyle']
    #dfill['photo_date'] = v['photo_date']
    file_path = k
    if regex_india_ready.findall(file_path):
        file_path = file_path.replace('/mnt/Post_Complete/SendReceive_BGRemoval/1_Sending', '/Retouch_')
    elif 
        file_path = file_path.replace('/mnt/Post_Complete/SendReceive_BGRemoval/2_Returned', '/zImages/')
    dfill['file_path'] = file_path
    dfill['alt'] = v['alt']
    fulldict[k] = dfill


## Take the compiled k/v pairs and Format + Insert into MySQL DB
for k,v in fulldict.iteritems():
    try:

        mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
        connection = mysql_engine.connect()
        ## /mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/1_Sending
        ## Test File path String to Determine which Table needs to be Updated Then Insert SQL statement
        sqlinsert_choose_test = v['file_path']

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
        
