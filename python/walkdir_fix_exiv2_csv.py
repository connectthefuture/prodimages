#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

def get_PNG_datecreate(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        datecreated = et.get_metadata(image_filepath)['PNG:datecreate'][:10]
    return datecreated

def get_exif_all_data(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(image_filepath)#['XMP:DateCreated'][:10].replace(':','-')
    return metadata


###
## Convert Walked Dir List To Lines with path,photo_date,stylenum,alt. Depends on above "get_exif_all_data" function
def walkeddir_parse_stylestrings_out(walkeddir_list):
    import re,os
    regex = re.compile(r'.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')
    stylestrings = []
    stylestringsdict = {}
    for line in walkeddir_list:
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
                    photo_date = get_exif_all_data(file_path)['File:FileModifyDate'][:10]
                except KeyError:
                    try:
                        photo_date = get_exif(file_path)['DateTime'][:10]
                    except KeyError:
                        try:
                            photo_date = get_exif(file_path)['DateTimeOriginal'][:10]
                        except KeyError:
                            photo_date = '0000-00-00'
                except AttributeError:
                        try:
                            photo_date = get_exif_all_data(file_path)['File:FileModifyDate'][:10]
                        except:
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
            #except AttributeError:
            #    print "AttributeError on {0}".format(line)
    return stylestringsdict


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



###
## Make Lowres Thumnails from Image files or Directory Full of Image Files. Copy Metadata after creating Thumbnail
def make_and_move_zimages_lowres_thumbnails_dir_or_singlefile(pathname):
    import os, sys, re, csv
    from PIL import Image
    import pyexiv2
    import glob, os, re
    size = 600, 720
    regex_jpeg = re.compile(r'.+?\.[jpgJPG]{3}$')
    zimages_root = '/mnt/Post_Ready/zImages_1'
    test_zimages = '/'.join(pathname.split('/')[:4])
    if test_zimages == zimages_root:
        pass
    elif re.findall(regex_jpeg, pathname):
        zimages_root = '/mnt/Post_Ready/zImages_1'
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
                #print "File Exists: {0}".format(zimages_filepath)
                os.remove(zimages_filepath)
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
                        os.remove(zimages1_photoselects)
                    else:
                        pass

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

def main():
    from PIL import Image
    import os,sys,re

    rootdir = sys.argv[1]
    walkedout = recursive_dirlist(rootdir)

    regex = re.compile(r'.*?[0-9]{9}_[1-6x]\.[jpgJPG]{3}$')
    #regex = re.compile(r'.+?\.[jpgJPG]{3}$')


    ## Parse Walked Directory Paths Output stylestringssdict
    stylestringsdict = walkeddir_parse_stylestrings_out(walkedout)

    ## Write CSV List to dated file for Impor t to MySQL
    #csv_write_datedOutfile(stylestrings)



    ## Create Dir Struct under ZIMAGES_1 if dir doesnt Exist and make/copy Jpeg Thumbs files to it
    import datetime
    tm = datetime.datetime.now().time()
    char1 = int(str(tm)[0])
    if char1 > 0: pass
    else:
        for k,v in stylestringsdict.iteritems():
            import os,sys,shutil, re
            pathname = k
            make_and_move_zimages_lowres_thumbnails_dir_or_singlefile(pathname)

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

            mysql_engine_data = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
            mysql_engine_www  = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
            connection_data = mysql_engine_data.connect()
            connection_www = mysql_engine_www.connect()

            ## Test File path String to Determine which Table needs to be Updated Then Insert SQL statement
            sqlinsert_choose_test = v['file_path']
            regex_photoselects = re.compile(r'^/.+?/Post_Ready/.+?Push/.*?[0-9]{9}_[1-6x]\.[jpgJPG]{3}$')
            regex_postreadyoriginal = re.compile(r'^.*?/Retouch_.+?/.*?[0-9]{9}_[1-6x]\.[jpgJPG]{3}$')
            regex_zimages = re.compile(r'^/zImages.*?/[0-9]{4}/.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')

            if re.findall(regex_photoselects, sqlinsert_choose_test):
                connection_data.execute("""INSERT INTO push_photoselects (colorstyle, photo_date, file_path, alt) VALUES (%s, %s, %s, %s)""", v['colorstyle'], v['photo_date'], v['file_path'],  v['alt'])
                connection_www.execute("""INSERT INTO push_photoselects (colorstyle, photo_date, file_path, alt) VALUES (%s, %s, %s, %s)""", v['colorstyle'], v['photo_date'], v['file_path'],  v['alt'])
                print "Successful Insert Push_Photoselecs --> {0}".format(k)

            elif re.findall(regex_postreadyoriginal, sqlinsert_choose_test):
                connection_data.execute("""INSERT INTO post_ready_original (colorstyle, photo_date, file_path, alt) VALUES (%s, %s, %s, %s)""", v['colorstyle'], v['photo_date'], v['file_path'],  v['alt'])
                connection_www.execute("""INSERT INTO post_ready_original (colorstyle, photo_date, file_path, alt) VALUES (%s, %s, %s, %s)""", v['colorstyle'], v['photo_date'], v['file_path'],  v['alt'])
                print "Successful Insert to Post_Ready_Originals --> {0}".format(k)

            elif re.findall(regex_zimages, sqlinsert_choose_test):
                connection_data.execute("""INSERT INTO zimages1_photoselects (colorstyle, photo_date, file_path, alt) VALUES (%s, %s, %s, %s)""", v['colorstyle'], v['photo_date'], v['file_path'],  v['alt'])
                connection_www.execute("""INSERT INTO zimages1_photoselects (colorstyle, photo_date, file_path, alt) VALUES (%s, %s, %s, %s)""", v['colorstyle'], v['photo_date'], v['file_path'],  v['alt'])
                print "Successful Insert to Zimages --> {0}".format(k)

            else:
                print "Database Table not Found for Inserting {0}".format(k)

        except sqlalchemy.exc.IntegrityError:
            print "Duplicate Entry {0}".format(k)



if __name__ == '__main__':
    main()
