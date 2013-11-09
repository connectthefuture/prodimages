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
        

import re,os,glob
dir_pushstill = '/mnt/Post_Ready/aPhotoPush'
dir_pushfashion = '/mnt/Post_Ready/aFashionPush'

pushstillfiles = glob.glob(os.path.join(dir_pushstill, '*/*/*.jpg'))
pushfashionfiles = glob.glob(os.path.join(dir_pushfashion, '*/*/*.jpg'))

regex_3 = re.compile(r'.+?/[2-9][0-9]{8}_[0-9]{3}.jpg')

foundliststill = find_regex_list(regex_3,pushstillfiles)

for f in foundliststill:
    print f
    found3digit_rename(f)
    
foundlistfashion = find_regex_list(regex_3,pushfashionfiles)

for f in foundlistfashion:
    print f
    found3digit_rename(f)
