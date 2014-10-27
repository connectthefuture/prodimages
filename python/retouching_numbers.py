#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
## Convert Walked Dir List To Lines with path,photo_date,stylenum,alt. Depends on above "get_exif" function
def walkeddir_parse_stylestrings_out(walkeddir_list):
    import re,os
    ########  Regex only finds _1.jpg files
    regex = re.compile(r'^/mnt/Post_Complete/Complete_Archive/Uploaded/dateloaded_\d+?/uploaded_\d+?/JPG_RETOUCHED_ORIG/[0-9]{9}\.[jpgJPG]{3}$')
    regex_alt = re.compile(r'^/mnt/Post_Complete/Complete_Archive/Uploaded/dateloaded_\d+?/uploaded_\d+?/JPG_RETOUCHED_ORIG/[0-9]{9}_alt0[1-7]\.[jpgJPG]{3}$')
    regex_date = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')
    stylestrings = []
    stylestringsdict = {}
    for line in walkeddir_list:
        stylestringsdict_tmp = {}
        if re.findall(regex,line):
            try:
                file_path = line
                fileext = '.' + file_path.split('.')[-1]
                filename = file_path.split('/')[-1]
                colorstyle = filename[:9]
                alt_ext = ''
                try:
                    alt_ext = file_path.split('_')[-1][:]
                except:
                    pass
                
                if not alt_ext:
                    alt_ext = '_1' + fileext
                else:
                    alt_int = int(alt_ext.split('.')[0][-1]) + 1
                
                    alt_ext = str("_" + str(alt_int) + fileext)
                ext = alt_ext.split('.')[-1]
                try:
                    path_date = file_path.split('/dateloaded_')[2:8]
                    path_date = "20{2:.2}-{0:.2}-{1:.2}".format(path_date[:2], path_date[2:4], path_date[4:6])
                    if re.findall(regex_date, path_date):
                        photo_date = path_date
                    else:
                        try:
                            photo_date = get_exif(file_path)['DateTimeCreated'][:10]
                        except KeyError:
                            try:
                                photo_date = get_exif(file_path)['DateTime'][:10]
                            except KeyError:
                                photo_date = '0000-00-00'
                except AttributeError:
                    photo_date = '0000-00-00'
                photo_date = str(photo_date)
                photo_date = photo_date.replace(':','-')
                stylestringsdict_tmp['colorstyle'] = colorstyle
                stylestringsdict_tmp['photo_date'] = photo_date
                stylestringsdict_tmp['file_path'] = file_path
                stylestringsdict_tmp['alt'] = str(alt_int)
                stylestringsdict[file_path] = stylestringsdict_tmp
                file_path_reletive = file_path.replace('/mnt/Post_Ready/zImages_1/', '/zImages/')
                file_path_reletive = file_path.replace('JPG', 'jpg')
                ## Format CSV Rows
                row = "{0},{1},{2},{3}".format(colorstyle,photo_date,file_path_reletive,str(alt_int))
                #print row
                stylestrings.append(row)
            except IOError:
                print "IOError on {0}".format(line)
                #except AttributeError:
                #    print "AttributeError on {0}".format(line)
    return stylestringsdict



def retouching_numbers():
    import datetime
    from collections import defaultdict
    ######  Recursively search Photo Folders and get counts of shots by date
    ## rootdir_still = '/mnt/Post_Ready/Retouch_Still'
    rootdir_still = '/mnt/Post_Complete/Complete_Archive/Uploaded/'
    #####  Walk rootdir tree compile dict of Walked Directory
    walkedout_still = recursive_dirlist(rootdir_still)
    #### Parse Walked Still Directory Paths Output stylestringssdict
    stylestringsdict_still = walkeddir_parse_stylestrings_out(walkedout_still)
    ### Now the still sets counts by date
    stilld = defaultdict(list)
    for row in stylestringsdict_still.itervalues():
        try:
            file_path = row['file_path']
            photo_date = row['photo_date']
            dt = photo_date
            dt = "{} 00:00:00".format(dt)
            dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            #### 5 digit date
            if type(dt) == datetime.datetime:
                photo_date = dt
                stilld[photo_date].append(file_path)
                #        else:
                #            dt = ''
                #            dt = "2000-01-01 00:00:00".format(dt)
                #            dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
                #            photo_date = dt
                #            stilld[photo_date].append(file_path)
        except:
            pass

    ## Count the Grouped Files
    stillcomplete_dict = {}
    for k,v in stilld.iteritems():
        tmp_dict = {}
        tmp_dict['role'] = 'Retouching'
        tmp_dict['total'] = len(v)
        stillcomplete_dict[k] = tmp_dict
        #    stillcomplete_dict['Role'] = 'Still_Photo'
        #    fashioncomplete_dict['shot_count'] = len(v)
    return stillcomplete_dict


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

