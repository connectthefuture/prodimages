#!/usr/bin/env python
import os, sys, re, csv, glob, subprocess, shutil

filesdir = '/Users/johnb/GitHub-Primary'
testdir  = '/Users/johnb/Dropbox/testimgs'
tjpg = glob.glob(os.path.join(testdir,'*.jpg'))
gjpg = glob.glob(os.path.join(filesdir,'*.jpg'))
gpng = glob.glob(os.path.join(filesdir,'*.png'))

pngout=os.path.join(filesdir,'pngout')
jpgout=os.path.join(filesdir,'jpgout')

try:
    os.makedirs(pngout, 16877)
except:
    pass

try:
    os.makedirs(jpgout, 16877)
except:
    pass

ongrey = []
for f in gjpg:
    try:
        # newf = f.replace('_l','_n')
        cmd=['convert', f, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '2%', '-bordercolor', 'white', '-border', '2x2', '-trim','-format', '%@', 'info:-']
        ret = subprocess.check_output(cmd, stdin=None, stderr=subprocess.STDOUT, shell=False)
        not_white = "400x480+0+0"
        oldimg = '{}'.format(ret.split('__')[-1])

        if str(oldimg) == str(not_white):
            ongrey.append(f)
            try:
                shutil.move(f,jpgout)
            except:
                pass
    except:
        pass
        
print ongrey

ongreypng = []
for f in gpng:
    try:
        # newf = f.replace('_l','_n')
        cmd=['convert', f, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '2%', '-bordercolor', 'white', '-border', '2x2', '-trim','-format', '%@', 'info:-']
        ret = subprocess.check_output(cmd, stdin=None, stderr=subprocess.STDOUT, shell=False)
        not_white = "400x480+0+0"
        oldimg = '{}'.format(ret.split('__')[-1])

        if str(oldimg) == str(not_white):
            ongreypng.append(f)
            try:
                shutil.move(f,pngout)
            except:
                pass
    except:
         pass
print ongreypng