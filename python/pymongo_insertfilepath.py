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


def get_exif(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(image_filepath)
        #['XMP:DateCreated'][:10].replace(':','-')
    return metadata


def imagepath_dbprep(recursed_output=None):
    import re,os
    regex = re.compile(r'.*?[0-9]{9}_[1-6]_?.*?\.[jpngJPNG]{3}$')    
    stylestringslist = []
    stylestringsdict = {}
    for line in recursed_output:
        stylestringsdict_tmp = {}
        if re.findall(regex,line):
            try:
                file_path = line
                filename = file_path.split('/')[-1]
                colorstyle = filename[:9]
                alt = ''
                alt = filename.split('_')[1]
                shot_number = ''
                shot_number = filename.split('_')[2]
                ext = filename.split('.')[-1]
                photo_date = ''
                try:
                    ##path_date = file_path.split('/')[6][:6]
                    ##path_date = "20{2:.2}-{0:.2}-{1:.2}".format(path_date[:2], path_date[2:4], path_date[4:6])
                    ##if re.findall(regex_date, path_date):
                    ##    photo_date = path_date
                    try:
                        photo_date = get_exif(file_path)['DateTimeOriginal'][:10]
                    except KeyError:
                        photo_date = get_exif(file_path)['DateTime'][:10]
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
                stylestringsdict_tmp['colorstyle'] = colorstyle
                stylestringsdict_tmp['photo_date'] = photo_date
                # file_path = file_path.replace('/mnt/Production_Raw/.zImages_1/', '/studio_thumbs/')
                stylestringsdict_tmp['file_path'] = file_path
                stylestringsdict_tmp['alt'] = alt
                stylestringsdict_tmp['shot_number'] = shot_number
                stylestringsdict[file_path] = stylestringsdict_tmp
                #file_path_reletive = file_path.replace('/mnt/Post_Ready/zImages_1/', '/zImages/')
                #file_path_reletive = file_path.replace('JPG', 'jpg')
                ## Format CSV Rows
                row = "{0},{1},{2},{3},{4}".format(colorstyle,photo_date,file_path,alt,shot_number)
                print row
                stylestringslist.append([row])
            except IOError:
                print "IOError on {0}".format(line)
            #except AttributeError:
            #    print "AttributeError on {0}".format(line)
    
    return stylestringslist
    #return colorstyle,photo_date,file_path,alt,shot_number
    #return stylestringsdict   
    
    
######################

def insert_pymongo(**kwargs):
#def insert_filerecord_pymongo(colorstyle = colorstyle, photo_date = photo_date, file_path = file_path, alt = alt, shot_number = shot_number):
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
def main():
    import os,sys,re
    rootdir = ''
    try:
        if sys.argv[1]:
            rootdir = sys.argv[1]
    except IndexError:
        pass

    recursedout = recursive_dirlist(rootdir)                   
    mongo_insertlist = imagepath_dbprep(recursedout)

    # Insert list
    for insrt in mongo_insertlist:        
        insert_pymongo(insrt)


if __name__ == 'main': 
    main()

