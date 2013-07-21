#!/usr/bin/env python

def find_regex_list(regex,filelist):
    import re,os
    dig3tlist = []
    try:

        for f in filelist:
            found = re.findall(regex, f)
            if found:
                dig3tlist.append(f)
                dig3tlist = sorted(dig3tlist)
            else:
                continue
    except TypeError:
        print "Error"
    return dig3tlist


def found3digit_rename(filename):
    import os
    #print filename
    fdir = os.path.dirname(filename)
    destdir = fdir #.strip("['")
    #print destdir
    fname = os.path.basename(filename)
    style = fname.split('_')[0]
    ext = fname.split('.')[-1]
    oldname = filename
    incr = 1
    newstyle = str(style + "_" + str(incr) + "." + ext)
    newname = os.path.join(destdir, newstyle)
    while os.path.isfile(newname) == True:
        newstyle = str(style + "_" + str(incr) + "." + ext)
        newname = os.path.join(destdir, newstyle)
        print newname
        incr += 1
        os.path.isfile(newname)
    else:
        #print newname
        os.rename(oldname,newname)
        return

##################  RUN  ########################

import re,os,glob,sys

dir_archstill = '/mnt/Post_Ready/Retouch_Still'
dir_archfashion = '/mnt/Post_Ready/Retouch_Fashion'
dir_zimages = '/mnt/Post_Ready/zImages_1'


regex_3 = re.compile(r'.+?/[2-9][0-9]{8}_[0-9]{3}\.[jpgJPG]{3}$')


if sys.argv[1] == dir_archstill:
    fileslist = glob.glob(os.path.join(dir_archstill, '*/*/*.jpg'))
elif sys.argv[1] == dir_archfashion:
    fileslist = glob.glob(os.path.join(dir_archfashion, '*/*.jpg'))
elif sys.argv[1] == dir_zimages:
    fileslist = glob.glob(os.path.join(dir_zimages, '*/*.jpg'))
else:
    globdir = sys.argv[1]
    fileslist = glob.glob(os.path.join(globdir, '*.jpg'))

foundlist = find_regex_list(regex_3,fileslist)

for f in foundlist:
    print f
    found3digit_rename(f)
