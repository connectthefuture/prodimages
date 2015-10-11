#!/usr/bin/env python

###
## Walk Root Directory and Return List of all Files in all Subdirs too
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
                	photo_date = 0000-00-00

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
        connection = mysql_engine.connect()

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
        
