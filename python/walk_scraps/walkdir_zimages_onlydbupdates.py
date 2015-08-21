#!/usr/bin/env python
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
## Convert Walked Dir List To Lines with path,photo_date,stylenum,alt. Depends on above "get_exif" function
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
                file_path_reletive = file_path.replace('/Volumes/Post_Ready/zImages_1/', '/zImages/')
                file_path_reletive = file_path.replace('JPG', 'jpg')
                ## Format CSV Rows
                row = "{0},{1},{2},{3}".format(colorstyle,photo_date,file_path_reletive,alt)
                print row
                stylestrings.append(row)
            except IOError:
                print "IOError on {0}".format(line)
            except AttributeError:
                print "AttributeError on {0}".format(line)
    return stylestringsdict