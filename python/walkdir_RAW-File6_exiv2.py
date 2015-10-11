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
## Convert Walked Dir List To Lines with path,photo_date,stylenum,alt. Depends on above "get_exif" function
def walkeddir_parse_stylestrings_out(walkeddir_list):
    import re,os
    regex_Raw = re.compile(r'/.*?/ON_FIGURE/.+?/[0-9]{9}.+?\.CR2$')
    regex_productionraw_Exports = re.compile(r'^/.+?/ON_FIGURE/.+?SELECTS/.*?[0-9]{9}_[1-9]\.[jpgJPG]{3}$')
    regex_date = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')
    stylestrings = []
    stylestringsdict = {}
    for line in walkeddir_list:
        stylestringsdict_tmp = {}
        if re.findall(regex_productionraw_Exports,line):
            try:

                file_path = line
                filename = file_path.split('/')[-1]
                colorstyle = filename.split('_')[0]
                alt = file_path.split('_')[-1]
                ext = filename.split('.')[-1]
                try:
                    path_date = file_path.split('/')[6][:6]
                    path_date = "20{2:.2}-{0:.2}-{1:.2}".format(path_date[:2], path_date[2:4], path_date[4:6])
                    if re.findall(regex_date, path_date):
                        photo_date = path_date
                    else:
                        try:
                            photo_date = get_exif(file_path)['DateTimeOriginal'][:10]
                        except KeyError:
                            try:
                                photo_date = get_exif(file_path)['DateTime'][:10]
                            except KeyError:
                                photo_date = '0000-00-00'
                        except IOError:
                            photo_date = '0000-00-00'
                            print "IOError on {0}".format(line)
                except AttributeError:
                    photo_date = '0000-00-00'
                except IOError:
                    print "IOError on {0}".format(line)
                    photo_date = '0000-00-00'
                photo_date = str(photo_date)
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

        elif re.findall(regex_Raw,line):
            try:
                file_path = line
                filename = file_path.split('/')[-1]
                colorstyle = filename.split('_')[0]
                alt = file_path.split('_')[-2]
                shot_number = file_path.split('_')[-1]
                shot_number = shot_number.split('.')[0]
                ext = filename.split('.')[-1]
                try:
                    path_date = file_path.split('/')[6][:6]
                    path_date = "20{2:.2}-{0:.2}-{1:.2}".format(path_date[:2], path_date[2:4], path_date[4:6])
                    if re.findall(regex_date, path_date):
                        photo_date = path_date
                    else:
                        try:
                            photo_date = get_exif(file_path)['DateTimeOriginal'][:10]
                        except KeyError:
                            try:
                                photo_date = get_exif(file_path)['DateTime'][:10]
                            except KeyError:
                                photo_date = '0000-00-00'
                            except IOError:
                                photo_date = '0000-00-00'
                                print "IOError on {0}".format(line)
                except AttributeError:
                    photo_date = '0000-00-00'
                except IOError:
                    print "IOError on {0}".format(line)
                    photo_date = '0000-00-00'
                photo_date = str(photo_date)
                photo_date = photo_date.replace(':','-')
                stylestringsdict_tmp['colorstyle'] = colorstyle
                stylestringsdict_tmp['photo_date'] = photo_date
                stylestringsdict_tmp['file_path'] = file_path
                stylestringsdict_tmp['alt'] = alt
                stylestringsdict_tmp['shot_number'] = shot_number
                stylestringsdict[file_path] = stylestringsdict_tmp
                file_path_reletive = file_path.replace('/mnt/Post_Ready/zImages_1/', '/zImages/')
                file_path_reletive = file_path.replace('JPG', 'jpg')
                ## Format CSV Rows
                row = "{0},{1},{2},{3},{4}".format(colorstyle,photo_date,file_path_reletive,alt,shot_number)
                print row
                stylestrings.append(row)
            except IOError:
                print "IOError on {0}".format(line)
            #except AttributeError:
            #    print "AttributeError on {0}".format(line)
    return stylestringsdict



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
## Resize/Copy Image as Copy All Metadata from Source Image File to Resized Thumb
def resize_image(infile, dest_file, size):
    from PIL import Image
    import pyexiv2
    zimages_filepath = dest_file
## Extract Originals Metadata prior to Resizing
    source_metadata = pyexiv2.ImageMetadata(infile)
    source_metadata.read()
# Resize and Save Thumb copy to Zimages
    im = Image.open(infile)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(zimages_filepath , "JPEG")
    print infile, zimages_filepath
# Copy EXIF data from Source to Resized Image
    dest_metadata = pyexiv2.ImageMetadata(zimages_filepath)
    dest_metadata.read()
    source_metadata.copy(dest_metadata, exif=True, iptc=True, xmp=True, comment=True)
# set EXIF image size info to resized size
#    dest_metadata.read()
#    dest_metadata["Exif.Photo.PixelXDimension"] = im.size[0]
#    dest_metadata["Exif.Photo.PixelYDimension"] = im.size[1]
    dest_metadata.write()
    return zimages_filepath

def subproc_magick_thumbs_600720(file,destdir):
    import subprocess, os, re
    outsize = '600x720'
    insize = '3744x5616'
    fname = file.split(".")[0]
    ext = file.split(".")[-1]
    outfile = os.path.join(destdir, fname + ".jpg")
    regex_CR2 = re.compile(r'.+?\.[CR2cr2]')
    regex_jpg = re.compile(r'.+?\.[JPGjpg]')
    if re.findall(regex_CR2, file):

        try:
            subprocess.call([
                "convert",
                "-format",
                "jpg",
                file,
                "-define",
                "jpeg:size=3744x5616",
                "-size",
                "600x720",
                "-colorspace",
                "rgb",
                "-adaptive-sharpen",
                "100",
                "-unsharp",
                "40",
                "-format",
                "jpg",
                "-colorspace",
                "srgb",
                "-quality",
                "75",
                "-thumbnail",
                outsize,
                outfile
            ])
            print "Made Thumb from RAW with Magick"
        except:
            print "Failed: {0}".format(file)

    elif re.findall(regex_jpg, file):
        try:
            subprocess.call([
                "convert",
                file,
                "-format",
                "jpg",
                "-adaptive-sharpen",
                "70",
                "-unsharp",
                "50",
                "-quality",
                "80",
                "-thumbnail",
                outsize,
                outfile
            ])
            print "Made Jpg-Thumb with Magick"
        except:
            print "Failed: {0}".format(file)
    return outfile

###
## Make Lowres Thumnails from Image files or Directory Full of Image Files. Copy Metadata after creating Thumbnail
def make_and_move_zimages_lowres_thumbnails_dir_or_singlefile(pathname):
    import os, sys, re, csv
    from PIL import Image
    import pyexiv2
    import glob, os, re
    size = 600, 720
    size = 3744, 5616
    regex_jpeg = re.compile(r'.+?\.[jpgJPG]{3}$')
    regex_productionraw_Exports = re.compile(r'^/.+?/ON_FIGURE/.+?SELECTS/.*?[0-9]{9}_[1-9]\.[jpgJPG]{3}$')
    regex_productionraw_Raw = re.compile(r'^/.+?/ON_FIGURE/.+?RAW_FILES.*?[0-9]{9}_[1-9]_[0-9]{1,4}\.[CR2]{3}$')
    zimages_root = '/mnt/Production_Raw/.zImages_1'
    test_zimages = '/'.join(pathname.split('/')[:4])
    if test_zimages == zimages_root:
        pass
    elif re.findall(regex_productionraw_Raw, pathname):
        pass
    elif re.findall(regex_productionraw_Exports, pathname):
        zimages_root = '/mnt/Production_Raw/.zImages_1'
    ## If input variable is a single File Create 1 Thumb
        if os.path.isfile(pathname):
            #try:
            infile = os.path.abspath(pathname)
            filename, ext = os.path.splitext(infile)
            zimages_name = os.path.split(infile)[-1]
            zimages_dir = zimages_name[:4]
            zimages_dir = os.path.join(zimages_root, zimages_dir)
            zimages_filepath = os.path.join(zimages_dir, zimages_name)
            #print infile, zimages_filepath

            ## Try to make 4 digit directory or pass if already present
            try:
                os.mkdir(zimages_dir, 16877)
            except OSError:
                pass

            ## Test if this file has already been copied to Zimages Dir -- If not Make 600x720 jpg in zimagesdir
            if os.path.isfile(zimages_filepath):
                print "File Exists: {0}".format(zimages_filepath)
                pass
            else:
                try:

                ## Extract Originals Metadata prior to Resizing
                    source_metadata = pyexiv2.ImageMetadata(infile)
                    source_metadata.read()
                # Resize and Save Thumb copy to Zimages
                    im = Image.open(infile)
                    im.thumbnail(size, Image.ANTIALIAS)
                    im.save(zimages_filepath , "JPEG")
                    print infile, zimages_filepath
                # Copy EXIF data from Source to Resized Image
                    dest_metadata = pyexiv2.ImageMetadata(zimages_filepath)
                    dest_metadata.read()
                    source_metadata.copy(dest_metadata, exif=True, iptc=True, xmp=True, comment=True)
                # set EXIF image size info to resized size
                #    dest_metadata.read()
                #    dest_metadata["Exif.Photo.PixelXDimension"] = im.size[0]
                #    dest_metadata["Exif.Photo.PixelYDimension"] = im.size[1]
                    dest_metadata.write()
                except IOError:
                    print "Bad Image File {}".format(zimages_filepath)
                    pass
            return zimages_filepath



            #except:
             #   print "Error Creating Single File Thumbnail for {0}".format(infile)
    ## If input variable is a Directory Decend into Dir and Crate Thumnails for all jpgs
    elif os.path.isdir(pathname):
        dirname = os.path.abspath(pathname)
        print dirname
        for infile in glob.glob(os.path.join(dirname, "*.jpg")):
            try:
                infile = os.path.abspath(infile)
                filename, ext = os.path.splitext(infile)
                zimages_name = os.path.split(infile)[-1]
                zimages_dir = zimages_name[:4]
                zimages_dir = os.path.join(zimages_root, zimages_dir)
                zimages_filepath = os.path.join(zimages_dir, zimages_name)
                print infile, zimages_filepath

                ## Try to make 4 digit directory or pass if already present
                try:
                    os.mkdir(zimages_dir, 16877)
                except OSError:
                    pass

                ## Test if this file has already been copied to Zimages Dir -- If not Make 600x720 jpg in zimagesdir
                if os.path.isfile(zimages_filepath):
                    pass
                    print "File Exists: {0}".format(zimages_filepath)
                else:
                    ## Extract Originals Metadata prior to Resizing
                        source_metadata = pyexiv2.ImageMetadata(infile)
                        source_metadata.read()
                    # Resize and Save Thumb copy to Zimages
                        im = Image.open(infile)
                        im.thumbnail(size, Image.ANTIALIAS)
                        im.save(zimages_filepath , "JPEG")
                        print infile, zimages_filepath
                    # Copy EXIF data from Source to Resized Image
                        dest_metadata = pyexiv2.ImageMetadata(zimages_filepath)
                        dest_metadata.read()
                        source_metadata.copy(dest_metadata, exif=True, iptc=True, xmp=True, comment=True)
                    # set EXIF image size info to resized size
                    #    dest_metadata.read()
                    #    dest_metadata["Exif.Photo.PixelXDimension"] = im.size[0]
                    #    dest_metadata["Exif.Photo.PixelYDimension"] = im.size[1]
                        dest_metadata.write()
                return zimages_filepath
            except:
                print "Error Creating Thumbnail for {0}".format(infile)

    else:
        print "File: {0} is not a jpg".format(pathname)

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
    colorstyle = v['colorstyle']
    alt = v['alt']
    dfill['colorstyle'] = v['colorstyle']
    dfill['photo_date'] = v['photo_date']
    file_path = k
    file_path = file_path.replace('/mnt/Production_Raw/.zImages_1/', '/studio_thumbs/')
    file_path = file_path.replace('/mnt/Production_Raw/PHOTO_STUDIO_OUTPUT/ON_FIGURE/', '/studio_raw/')
#     regex_productionraw_Exports = re.compile(r'^/.+?/ON_FIGURE/.+?SELECTS/.*?[0-9]{9}_[1-9]\.[jpgJPG]{3}$')
#     if re.findall(regex_productionraw_Exports, file_path):
#         file_pathz = os.path.join('/mnt/Production_Raw/.zImages_1', colorstyle[:4], colorstyle, '_' + v['alt'], '.jpg')
#         if os.path.isfile(file_pathz):
#             file_path = file_pathz
    dfill['file_path'] = file_path
    dfill['alt'] = v['alt']
    try:
        dfill['shot_number'] = v['shot_number']
    except:
        pass
    fulldict[k] = dfill


## Take the compiled k/v pairs and Format + Insert into MySQL DB
for k,v in fulldict.iteritems():
    try:

        mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
        connection = mysql_engine.connect()
        ## Test File path String to Determine which Table needs to be Updated Then Insert SQL statement
        sqlinsert_choose_test = v['file_path']
        #regex_productionraw = re.compile(r'^/.+?/ON_FIGURE/.+?RAW_FILES.*?/[0-9]{9}_[1-9]_[0-9]{1,4}\.[jpgJPGCR2]{3}$')
        regex_productionraw = re.compile(r'.+?/[0-9]{9}_[1-9]_?[0-9]{1,4}?.+?\.[jpgJPGCR2]{3}$')
        regex_productionraw_zimages = re.compile(r'^/.+?Raw/\.zImages_1/.*?[0-9]{9}_[1-9]\.[jpgJPG]{3}$')
        regex_productionraw_Exports = re.compile(r'^/.+?/studio_raw/.+?SELECTS/.*?[0-9]{9}_[1-9]\.[jpgJPG]{3}$')
        regex_photoselects = re.compile(r'^/.+?/Post_Ready/.+?Push/.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')
        regex_postreadyoriginal = re.compile(r'^/Retouch_.+?/.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')
        regex_zimages = re.compile(r'^/zImages.*?/[0-9]{4}/.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')

## ProdRaw RAW
        if re.findall(regex_productionraw, sqlinsert_choose_test):
            connection.execute("""INSERT INTO production_raw_onfigure (colorstyle, photo_date, file_path, alt, shot_number) VALUES (%s, %s, %s, %s, %s)""", v['colorstyle'], v['photo_date'], v['file_path'],  v['alt'], v['shot_number'])
            print "Successful Insert production_raw_onfigure --> {0}".format(k)
## ProdRaw Thumbs
        elif re.findall(regex_productionraw_zimages, sqlinsert_choose_test):
            connection.execute("""INSERT INTO production_raw_zimages (colorstyle, photo_date, file_path, alt) VALUES (%s, %s, %s, %s)""", v['colorstyle'], v['photo_date'], v['file_path'],  v['alt'])
            print "Successful Insert production_raw_onfigure --> {0}".format(k)
## PostReady Daily Selects To get images for Retouching
        elif re.findall(regex_photoselects, sqlinsert_choose_test):
            connection.execute("""INSERT INTO push_photoselects (colorstyle, photo_date, file_path, alt) VALUES (%s, %s, %s, %s)""", v['colorstyle'], v['photo_date'], v['file_path'],  v['alt'])
            print "Successful Insert Push_Photoselecs --> {0}".format(k)
## PostReady Archived HiRez Selects
        elif re.findall(regex_postreadyoriginal, sqlinsert_choose_test):
            connection.execute("""INSERT INTO post_ready_original (colorstyle, photo_date, file_path, alt) VALUES (%s, %s, %s, %s)""", v['colorstyle'], v['photo_date'], v['file_path'],  v['alt'])
            print "Successful Insert to Post_Ready_Originals --> {0}".format(k)
## Post_Ready zImages Thumbs
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
