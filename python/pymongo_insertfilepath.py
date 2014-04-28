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
    return walkedlist


def get_exif(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(image_filepath)
        #['XMP:DateCreated'][:10].replace(':','-')
    return metadata


def imagepath_dbprep(recursed_output=None):
    import re,os
    regex = re.compile(r'.*?[0-9]{9}_?[1-6]?_?.*?\.[jpngJPNG]{3}$')    
    stylestringslist = []
    stylestringsdict = {}
    for line in recursed_output:
        stylestringsdict_tmp = {}
        alt = ''
        shot_number = ''
        photo_date = ''
        if re.findall(regex,line):
            try:
                file_path = line
                filename = file_path.split('/')[-1]
                colorstyle = filename[:9]
                ext = filename.split('.')[-1]
                # alt
                try:
                    alt = filename.split('_')[1]
                except IndexError:
                    alt = ''
                # shot_number
                try:
                    shot_number = filename.split('_')[2]
                except IndexError:
                    shot_number = ''
                # photo_date
                try:
                    try:
                        photo_date = get_exif(file_path)['XMP:DateCreated'][:10].replace(':','-')
                    except KeyError:
                        photo_date = get_exif(file_path)['DateTime'][:10]
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
                #row = "{0},{1},{2},{3},{4}".format(colorstyle,photo_date,file_path,alt,shot_number)
                #print row
                #stylestringslist.append([row])
            except IOError:
                print "IOError on {0}".format(line)
    #return stylestringslist
    # return colorstyle,photo_date,file_path,alt,shot_number
    return stylestringsdict   
    ######################


def insert_pymongo(**kwargs):
    # def insert_filerecord_pymongo(colorstyle = colorstyle, photo_date = photo_date, file_path = file_path, alt = alt, shot_number = shot_number):
    # Insert a New Document
    # colorstyle = colorstyle, 
    # photo_date = photo_date, 
    # file_path = file_path, 
    # alt = alt, 
    # shot_number = shot_number
    import pymongo
    mongo = pymongo.Connection('127.0.0.1')
    mongo_db = mongo['testimages']
    mongo_collection = mongo_db['imagecollection']
    # Returns the '_id' key associated with the newly created document
    insert_id = mongo_collection.insert({'colorstyle': colorstyle,
                                         'photo_date': photo_date,
                                         'file_path': file_path,
                                         'alt': alt,
                                         'shot_number': shot_number
                                        })

############# RUN ##############
def main(rootdir):
    import os,sys,re
    recursedout = recursive_dirlist(rootdir)                   
    mongo_insertlist = imagepath_dbprep(recursedout)
    # Insert list
    for insrt in mongo_insertlist:        
        # Insert a New Document
        colorstyle  = insrt['colorstyle']
        photo_date  = insrt['photo_date']
        file_path   = insrt['file_path']
        alt         = insrt['alt']
        shot_number = insrt['shot_number']
        insert_pymongo(colorstyle=colorstyle, photo_date=photo_date, file_path=file_path, alt=alt, shot_number=shot_number)
        print "Inserted {}".format(file_path)

if __name__ == 'main': 
    import sys
    rootdir = ''
    try:
        if sys.argv[1]:
            rootdir = sys.argv[1]
    except IndexError:
        pass
    
    main(rootdir)
