#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, re, csv

def update_pm_photodate(colorstyle):
    import subprocess
    update_url = 'http://dmzimage01.l3.bluefly.com:8080/photo/{0}'.format(colorstyle)

    subprocess.call([
    "curl",
    '-d',
    "sample_image=Y",
    '-d',
    "photographed_date=now",
    "-X",
    "PUT",
    "-format",
    update_url,
    ])


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


def splitswim_updatepm(file_path):
    import re
    regex_fullmultistyle = re.compile(r'^.+?/[1-9][0-9]{8}_[b-zB-Z][a-zA-Z]{1,10}[1-9][0-9]{8}_[1-6].+?\.CR2')
    #regex_multistyle = re.compile(r'^.+?/[1-9][0-9]{8}_[1-6]\.jpg')
    regex_split       = re.compile(r'[b-zB-Z][a-zA-Z]{1,10}')

    if re.findall(regex_fullmultistyle, file_path):
        print "Multistyle".format(file_path)
        try:
            fname                 = file_path.split('/')[-1]
            secondarycat          = re.split(regex_split, fname)
            primarystyle          = secondarycat[0][:9]
            secondarystyle        = secondarycat[1][:9]
            # m = re.match(r"(\d+)\.?(\d+)?", "24")
            #m = re.match(regex_fullmultistyle,file_path)
            # m.groups('0')   # Now, the second group defaults to '0'.
            # groupdict([m])
            #primarystyle = m.groups('0')[0]
            #secondarystyle = m.groups('0')[1]

#            try:
#                secondarycategory = fname.split('_')[2]
#                print secondarycategory,"SECOND"
#            except:
#                pass
#            print primarystyle,secondarystyle
            try:
                return primarystyle, secondarystyle
            except:
                pass
        except OSError:
            print "FailedSwimSplit {}".format(file_path)
            pass
##############################RUN###########################
from PIL import Image
import os, sys, re, glob, datetime

todaysdate = str(datetime.date.today())
todaysfolder = "{0}{1}{2}_".format(todaysdate[5:7],todaysdate[8:10],todaysdate[2:4])

eFashion_root = '/mnt/Post_Ready/eFashionPush'
aPhoto_root = '/mnt/Post_Ready/aPhotoPush'

#rootdir = sys.argv[1]
#walkedout = recursive_dirlist(rootdir)

regex = re.compile(r'.*?/[0-9]{9}_[1].*?\.[jpgJPGCR2]{3}$')
regex_raw = re.compile(r'.*?/RAW/.+?/[0-9]{9}_[1].*?\.[jpgJPGCR2]{3}$')
#regex = re.compile(r'.+?\.[jpgJPG]{3}$')
basedir = os.path.join('/mnt/Production_Raw/PHOTO_STUDIO_OUTPUT/ON_FIGURE/*/', todaysfolder + '*')
basedirstill = os.path.join(aPhoto_root, todaysfolder + '*')

flagged = ''
try:
    args = sys.argv
except:
    args = ''

if args and len(args) == 1:
    globalldirs = os.path.abspath(sys.argv[1])
    #globexportdir = os.path.abspath(sys.argv[1])#glob.glob(os.path.join(basedir, "EXPORT/*/*.jpg"))
    #globstilldir = os.path.abspath(sys.argv[1])#'.' 
    flagged = 'SET'# glob.glob(os.path.join(basedirstill, "*/*.jpg"))
elif args and len(args) > 1: 
    globalldirs = args[1:]
    flagged = 'SET'
else:
    #globrawdir = glob.glob(os.path.join(basedir, "*/*/*.CR2"))
    #globexportdir = glob.glob(os.path.join(basedir, "EXPORT/*/*.jpg"))
    globstilldir = glob.glob(os.path.join(basedirstill, "*/*.jpg"))
    #curl -d sample_image=Y -d photographed_date=now -X PUT http://dmzimage01.l3.bluefly.com:8080/photo/"$outName"

    globalldirs = globstilldir


colorstyles_unique = []
#stylestringsdict = {}
for line in globalldirs:
    #stylestringsdict_tmp = {}
    regex_fullmultistyle = re.compile(r'^.+?/[1-9][0-9]{8}_[b-zB-Z][a-zA-Z]{1,10}[1-9][0-9]{8}_[1-6].+?\.CR2')
    
    try:
        if re.findall(regex_fullmultistyle, line):
            
            swimpair = splitswim_updatepm(line)
            primarystyle     = swimpair[0]
            secondarystyle   = swimpair[1]
            #if primarystyle not in colorstyles_unique:
            print "YAY_SWIMTOP-->{0}".format(primarystyle)
            colorstyles_unique.append(primarystyle)
            colorstyles_unique = sorted(colorstyles_unique)
            #if secondarystyle not in colorstyles_unique:
            print "YAY_SWIMBOTTOM-->{0}".format(secondarystyle)
            colorstyles_unique.append(secondarystyle)
            colorstyles_unique = sorted(colorstyles_unique)

        elif re.findall(regex_raw,line):
            try:
                file_path = line
                filename = file_path.split('/')[-1]
                colorstyle = filename.split('_')[0]
                alt = filename.split('_')[1]
                shot_ext = file_path.split('_')[-1]
                shot_number = shot_ext.split('.')[0]
                ext = shot_ext.split('.')[-1]
                
                
                ## Unique Styles Only
                if colorstyle not in colorstyles_unique:
                    print colorstyle
                    colorstyles_unique.append(colorstyle)
                    colorstyles_unique = sorted(colorstyles_unique)
                else:
                    print "Already Accounted {0}".format(colorstyle)

            except IOError:
                print "IOError on {0}".format(line)
            except AttributeError:
                print "AttributeError on {0}".format(line)
        ## If file_path doesnt match the Regular 9digit_# format, checks for 2 styles in 1 shot             
        elif len(line) == 9 and line.isdigit():
            colorstyle = line
            colorstyles_unique.append(colorstyle)
            colorstyles_unique = sorted(colorstyles_unique)
        

        else:
            try:
                file_path = line
                filename = file_path.split('/')[-1]
                colorstyle = filename.split('_')[0]
                alt = filename.split('_')[1]
                #shot_ext = file_path.split('_')[-1]
                #shot_number = shot_ext.split('.')[0]
                #ext = shot_ext.split('.')[-1]
                
                
                ## Unique Styles Only
                if colorstyle not in colorstyles_unique:
                    print colorstyle
                    colorstyles_unique.append(colorstyle)
                    colorstyles_unique = sorted(colorstyles_unique)
                else:
                    print "Already Accounted {0}".format(colorstyle)
            except IOError:
                print "IOError on {0}".format(line)
            except AttributeError:
                print "AttributeError on {0}".format(line)
    except:
        print "Error appending {}".format(line)
        pass
        

        ############ Send Shots to PM API to update photodate
colorstyles_unique = set(sorted(colorstyles_unique))
for colorstyle in colorstyles_unique:
    try:
        update_pm_photodate(colorstyle)
    except:
        print "FAILED UPDATE for {0}".format(colorstyle)

########### Check for Exports Remove Shot Number & and Move to eFashionPush ##########
if not flagged:
    try:
        
        import shutil

        if globexportdir:
            try:
                for f in globexportdir:
                    found3digit_rename(f)
            except:
                print 'Faild'

    ### Get ShootDir Name from last "f" in previous glob and rename ops, then create if not exist
    ## eFashionPush Dir to Create for Exports used below 

        eFashion_name = file_path.split('/')[6]

    #eFashion_name = '121913'

        eFashion_dir = os.path.join(eFashion_root, eFashion_name)
    # if not os.path.isdir(eFashion_dir):
    #     os.makedirs(eFashion_dir, 16877)


    ## Refresh and Get Renamed files then copy to eFashion Dir
        globexportdir = glob.glob(os.path.join(basedir, "EXPORT/*/*.jpg"))

        if globexportdir:
            for f in globexportdir:
                shutil.copy2(f, eFashion_dir)
    except:
        pass