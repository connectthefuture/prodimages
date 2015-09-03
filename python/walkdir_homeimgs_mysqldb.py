#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
###
## Extract All Metadata from Image File as Dict using PIL
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
## Write Single Metadata Tag/Value to Imagefile using pyexiv2
def embed_exif_metadata(image_filepath, exiftag=None, exifvalue=None):
    from PIL import Image
    import pyexiv2
    # Read EXIF data to initialize
    image_metadata = pyexiv2.ImageMetadata(image_filepath)
    image_metadata.read()
    # Add and Write new Tag to File
    image_metadata[exiftag] = exifvalue
    image_metadata.write()
    return image_filepath


def get_exif_metadata_value(image_filepath, exiftag=None, exifvalue=None):
    from PIL import Image
    import pyexiv2
    if exifvalue:

        # Read EXIF data to initialize
        image_metadata = pyexiv2.ImageMetadata(image_filepath)
        metadata = image_metadata.read()
        # Add and Write new Tag to File
        exifvalue = metadata[exiftag]
        # image_metadata[exiftag] = exifvalue
        # image_metadata.write()
    else:
        print "Not Yet Built"
    return image_filepath

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
## Convert Walked Dir List To Lines with path,photo_date,stylenum,dimensions. Depends on above "get_exif" function
def walkeddir_parse_stylestrings_out(walkeddir_list):
    import re,os
    regex_Raw = re.compile(r'/.*?/ON_FIGURE/.+?/[0-9]{9}.+?\.CR2$')
    regex_zjpg = re.compile(r'^/.+?/[0-9]{9}_[1-9]_?[0-9]{1,4}?.+?\.[jpgJPGCR2]{3}$')
    regex_productionraw_Exports = re.compile(r'^/.+?/ON_FIGURE/.+?SELECTS/.*?[0-9]{9}_[1-9]\.[jpgJPG]{3}$')
    regex_date = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')
    regex_mediarepo_imgs  = re.compile(r'^.+?MEDIAREPO.+?\.[NnjpegJPEG]{3,4}$')
    stylestrings = []
    stylestringsdict = {}
    for line in walkeddir_list:
        stylestringsdict_tmp = {}
        if re.findall(regex_mediarepo_imgs, line):
            try:
                file_path = line
                filename = file_path.split('/')[-1]
                name = filename.split('_')[0]
                try:
                    dimensions = get_exif(file_path)['ImageSize']
                except:
                    dimensions = 'not_available'
                    print 'No ImageSize exif field'
                shot_number = file_path.split('_')[-1]
                shot_number = shot_number.split('.')[0]
                ext = filename.split('.')[-1]
                try:
                    ##path_date = file_path.split('/')[6][:6]
                    ##path_date = "20{2:.2}-{0:.2}-{1:.2}".format(path_date[:2], path_date[2:4], path_date[4:6])
                    ##if re.findall(regex_date, path_date):
                    ##    photo_date = path_date
                    try:
                        photo_date = get_exif(file_path)['FileModificationDate\/Time'][:10]
                    except KeyError:
                        try:
                            photo_date = get_exif(file_path)['DateTime'][:10]
                        except KeyError:
                            photo_date = '0000-00-00'
                    #try:
                    #    file_type = get_exif(file_path)['FileType'][:10]
                    #except KeyError:
                    #    photo_date = get_exif(file_path)['DateTime'][:10]
                    ##else:
#                        try:
#                            photo_date = get_exif(file_path)['DateTimeOriginal'][:10]
#                        except KeyError:
#                            try:
#                                photo_date = get_exif(file_path)['DateTime'][:10]
#                            except KeyError:
#                                photo_date = '0000-00-00'
#                            except IOError:
#                                photo_date = '0000-00-00'
#                                print "IOError on {0}".format(line)
                except AttributeError:
                    photo_date = '0000-00-00'
                except IOError:
                    print "IOError on {0}".format(line)
                    photo_date = '0000-00-00'
                photo_date = str(photo_date)
                photo_date = photo_date.replace(':','-')
                stylestringsdict_tmp['name'] = name
                stylestringsdict_tmp['photo_date'] = photo_date
                file_path = file_path.replace('/mnt/Production_Raw/.zImages_1/', '/studio_thumbs/')
                stylestringsdict_tmp['file_path'] = file_path
                stylestringsdict_tmp['dimensions'] = dimensions
                stylestringsdict_tmp['shot_number'] = shot_number
                stylestringsdict[file_path] = stylestringsdict_tmp
                file_path_reletive = file_path.replace('/mnt/Post_Ready/zImages_1/', '/zImages/')
                file_path_reletive = file_path.replace('JPG', 'jpg')
                ## Format CSV Rows Returning list instead of dict
                #row = "{0},{1},{2},{3},{4}".format(name,photo_date,file_path_reletive,dimensions,shot_number)
                #print row
                #stylestrings.append(row)
            except IOError:
                print "IOError on {0}".format(line)
            #except AttributeError:
            #    print "AttributeError on {0}".format(line)
    return stylestringsdict
    



############################ Run ######################################################## Run ############################
############################ Run ######################################################## Run ############################

from PIL import Image
import os,sys,re

try:
    rootdir = sys.argv[1]
except:
    rootdir = '/mnt/MEDIAREPO/'
walkedout = recursive_dirlist(rootdir)

#regex = re.compile(r'.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')
#regex = re.compile(r'.+?\.[jpgJPG]{3}$')
#regex = re.compile(r'^/.+?/Production_Raw/PHOTO_STUDIO_OUTPUT/ON_FIGURE/.+?RAW_FILES.*?[0-9]{9}_[1-9]_[0-9]{1,4}\.[jpgJPGCR2]{3}$')
regex = re.compile(r'^/.+?/ON_FIGURE/.+?RAW_FILES.*?[0-9]{9}_[1-9]_[0-9]{1,4}\.[jpgJPGCR2]{3}$')
regex_productionraw_Exports = re.compile(r'^/.+?/ON_FIGURE/.+?SELECTS/.*?[0-9]{9}_[1-9]\.[jpgJPG]{3}$')
## Parse Walked Directory Paths Output stylestringssdict
stylestringsdict = walkeddir_parse_stylestrings_out(walkedout)

## Write CSV List to dated file for Impor t to MySQL
#csv_write_datedOutfile(stylestrings)



## Create Dir Struct under ZIMAGES_1 if dir doesnt Exist and make/copy Jpeg Thumbs files to it
#for k,v in stylestringsdict.iteritems():
#    import os,sys,shutil, re
#    pathname = k
#    make_and_move_zimages_lowres_thumbnails_dir_or_singlefile(pathname)

#Iterate through Dict of Walked Directory, then Import to MySql DB
import sqlalchemy
#from mtags_singlefile_RAW import sqlQueryMetatags
## First compile the SQL Fields as key value pairs
fulldict = {}
for k,v in stylestringsdict.iteritems():
    dfill = {}
    name = v['name']
    dimensions = v['dimensions']
    dfill['name'] = v['name']
    dfill['photo_date'] = v['photo_date']
    file_path = k
    file_path = file_path.replace('/mnt/Production_Raw/.zImages_1/', '/studio_thumbs/')
    file_path = file_path.replace('/mnt/Production_Raw/PHOTO_STUDIO_OUTPUT/ON_FIGURE/', '/studio_raw/')
#     regex_productionraw_Exports = re.compile(r'^/.+?/ON_FIGURE/.+?SELECTS/.*?[0-9]{9}_[1-9]\.[jpgJPG]{3}$')
#     if re.findall(regex_productionraw_Exports, file_path):
#         file_pathz = os.path.join('/mnt/Production_Raw/.zImages_1', name[:4], name, '_' + v['dimensions'], '.jpg')
#         if os.path.isfile(file_pathz):
#             file_path = file_pathz
    dfill['file_path'] = file_path
    dfill['dimensions'] = v['dimensions']
    try:
        dfill['shot_number'] = v['shot_number']
    except:
        pass
    fulldict[k] = dfill


## Take the compiled k/v pairs and Format + Insert into MySQL DB
for k,v in fulldict.iteritems():
    try:

        ##mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
        mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@127.0.0.1:3301/www_django')
        connection = mysql_engine.connect()
        ## Test File path String to Determine which Table needs to be Updated Then Insert SQL statement
        sqlinsert_choose_test = v['file_path']
        #regex_productionraw = re.compile(r'^/.+?/ON_FIGURE/.+?RAW_FILES.*?/[0-9]{9}_[1-9]_[0-9]{1,4}\.[jpgJPGCR2]{3}$')
        regex_mediarepo_imgs  = re.compile(r'^.+?MEDIAREPO.+?\.[NnjpegJPEG]{3,4}$')
        regex_mediarepo_vids  = re.compile(r'^.+?MEDIAREPO.+?\.[MmpPEe34KkVvOo]{3,4}$')
        regex_mediarepo_music = re.compile(r'^.+?MEDIAREPO.+?\.[MmPp34]{3,4}$')
        regex_productionraw = re.compile(r'.+?/[0-9]{9}_[1-9]_?[0-9]{1,4}?.+?\.[jpgJPGCR2]{3}$')
        regex_productionraw_zimages = re.compile(r'.*?studio_thumbs.*?[0-9]{4}/[0-9]{9}_[1-9]_?[0-9]{1,4}?.+?\.[jpgJPGCR2]{3}$')
        regex_productionraw_Exports = re.compile(r'^/.+?/studio_raw/.+?SELECTS/.*?[0-9]{9}_[1-9]\.[jpgJPG]{3}$')
        regex_photoselects = re.compile(r'^/.+?/Post_Ready/.+?Push/.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')
        regex_postreadyoriginal = re.compile(r'^/Retouch_.+?/.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')
        regex_zimages = re.compile(r'^/zImages.*?/[0-9]{4}/.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')

## ProdRaw Thumbs
        if re.findall(regex_mediarepo_imgs, sqlinsert_choose_test):
            connection.execute("""INSERT INTO home_mediarepo_imgs (id, name, photo_date, file_path, dimensions) VALUES (%s, %s, %s, %s, %s)""", v['name'], v['photo_date'], v['file_path'],  v['dimensions'], v['shot_number'])
            print "Successful Insert home_mediarepo_imgs --> {0}".format(k)

        if re.findall(regex_mediarepo_music, sqlinsert_choose_test):
            connection.execute("""INSERT INTO home_mediarepo_music (id, name, modify_date, file_path, duration) VALUES (%s, %s, %s, %s, %s)""", v['name'], v['photo_date'], v['file_path'],  v['dimensions'], v['shot_number'])
            print "Successful Insert home_mediarepo_music --> {0}".format

## ProdRaw RAW
#        elif re.findall(regex_productionraw, sqlinsert_choose_test):
#            connection.execute("""INSERT INTO production_raw_onfigure (name, photo_date, file_path, dimensions, shot_number) VALUES (%s, %s, %s, %s, %s)""", v['name'], v['photo_date'], v['file_path'],  v['dimensions'], v['shot_number'])
#            print "Successful Insert production_raw_onfigure --> {0}".format(k)

        else:
            print "Database Table not Found for Inserting {0}".format(k)
    #except OSError:
    except sqlalchemy.exc.IntegrityError:
        print "Duplicate Entry {0}".format(k)
        pass
