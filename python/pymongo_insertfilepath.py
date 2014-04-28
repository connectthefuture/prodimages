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


def imagepath_dbprep(recursed_output):
    import re,os
    #regex = re.compile(r'.*?[0-9]{9}_?[1-6]?_?.*?\.[jpngJPNG]{3}$')    
    regex = re.compile(r'.*?\.[jpngJPNG]{3}$')
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
                        try:
                            photo_date = get_exif(file_path)['EXIF:DateTimeOriginal'][:10]
                        except KeyError:
                            try:
                                photo_date = get_exif(file_path)['File:FileModifyDate'][:10]
                            except KeyError:
                                pass
                                
                except AttributeError:
                    photo_date = '0000-00-00'
                except IOError:
                    print "IOError on {0}".format(line)
                    photo_date = '0000-00-00'
                photo_date = str(photo_date)
                photo_date = photo_date.replace(':','-')
                stylestringsdict_tmp['colorstyle'] = colorstyle
                stylestringsdict_tmp['photo_date'] = photo_date
                
                # Change db entry to use Relative path from server
                file_path = file_path.replace('/Volumes/', '/mnt/')
                file_path = file_path.replace('/mnt/Production_Raw/.zImages_1/', '/studio_thumbs/')
                file_path = file_path.replace('/mnt/Post_Ready/Retouch_Fashion/', '/Retouch_Fashion/')
                file_path = file_path.replace('/mnt/Post_Ready/Retouch_Still/', '/Retouch_Still/')
                file_path = file_path.replace('/mnt/Post_Ready/zImages_1/', '/zImages/')
                file_path = file_path.replace('JPG', 'jpg')
                
                stylestringsdict_tmp['file_path'] = file_path
                stylestringsdict_tmp['alt'] = alt
                stylestringsdict_tmp['shot_number'] = shot_number
                stylestringsdict[file_path] = stylestringsdict_tmp

                #row = "[{0},{1},{2},{3},{4}]".format(colorstyle,photo_date,file_path,alt,shot_number)
                #print row
                #stylestringslist.append([row])
            except IOError:
                print "IOError on {0}".format(line)
    #return stylestringslist
    # return colorstyle,photo_date,file_path,alt,shot_number
    return stylestringsdict   
    ######################


#def insert_pymongo(**kwargs):
def insert_filerecord_pymongo(colorstyle=None, photo_date=None, file_path=None, alt=None, shot_number=None):
    # Insert a New Document
    import pymongo
    mongo = pymongo.Connection('127.0.0.1')
    mongo_db = mongo['images']
    mongo_collection = mongo_db['imagecollection']
    # Returns the '_id' key associated with the newly created document
    new_insertobj_id = mongo_collection.insert({'colorstyle': colorstyle,
                                                 'photo_date': photo_date,
                                                 'file_path': file_path,
                                                 'alt': alt,
                                                 'shot_number': shot_number
                                                })
    print "Inserted {}".format(file_path)
    return new_insertobj_id

############# RUN ##############
def main(rootdir):
    import os,sys,re
    recursedout = recursive_dirlist(rootdir)                   
    mongo_insertdict = imagepath_dbprep(recursedout)
    for k,v in mongo_insertdict.iteritems():        
        # Insert/Create a New Document
        print k,v
        colorstyle  = v['colorstyle']
        photo_date  = v['photo_date']
        file_path   = v['file_path']
        alt         = v['alt']
        shot_number = v['shot_number']
        insert_filerecord_pymongo(colorstyle=colorstyle, photo_date=photo_date, file_path=file_path, alt=alt, shot_number=shot_number)
        print "Inserted {}".format(file_path)

#######################
#######################
if __name__ == '__main__': 
    import sys
    rootdir = ''
    try:
        if sys.argv[1]:
            rootdir = sys.argv[1]
    except IndexError:
        pass
    
    main(rootdir)
