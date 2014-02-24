#!/usr/bin/env python
import os, sys, re, csv

def update_pm_photodate(colorstyle):
    import subprocess
    update_url = 'http://ccapp101.l3.bluefly.com:8080/photo/{0}'.format(colorstyle)

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


globrawdir = glob.glob(os.path.join(basedir, "*/*/*.CR2"))
globexportdir = glob.glob(os.path.join(basedir, "EXPORT/*/*.jpg"))

globstilldir = glob.glob(os.path.join(basedirstill, "*/*.jpg"))
#curl -d sample_image=Y -d photographed_date=now -X PUT http://ccapp101.l3.bluefly.com:8080/photo/"$outName"

globalldirs = globrawdir + globstilldir

colorstyles_unique = []
#stylestringsdict = {}

for line in globalldirs:
    #stylestringsdict_tmp = {}
    if re.findall(regex_raw,line):

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



############ Send Shots to PM API to update photodate

for colorstyle in colorstyles_unique:
    try:
        update_pm_photodate(colorstyle)
    except:
        print "FAILED UPDATE for {0}".format(colorstyle)

########### Check for Exports Remove Shot Number & and Move to eFashionPush ##########
import shutil

if globexportdir:
    for f in globexportdir:
        found3digit_rename(f)


### Get ShootDir Name from last "f" in previous glob and rename ops, then create if not exist
## eFashionPush Dir to Create for Exports used below 
try:
    eFashion_name = f.split('/')[6]
    eFashion_dir = os.path.join(eFashion_root, eFashion_name)
    if not os.path.isdir(eFashion_dir):
        os.makedirs(eFashion_dir, 16877)

except IndexError:
    pass
## Refresh and Get Renamed files then copy to eFashion Dir
globexportdir = glob.glob(os.path.join(basedir, "EXPORT/*/*.jpg"))

if globexportdir:

    for f in globexportdir:
        try:
            shutil.copy2(f, eFashion_dir)    
        except IndexError:
            pass
