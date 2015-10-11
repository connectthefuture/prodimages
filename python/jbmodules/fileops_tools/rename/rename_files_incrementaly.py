#!/usr/bin/env python
import os, sys, re, csv
import glob
import sqlalchemy
glbdir = sys.argv[1]
   
#glbdir = '/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/117147'
#globtoconvert = os.path.join('/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/117147', '*.jpg')
globtoconvert = glob.glob(os.path.join(os.path.realpath(glbdir), '*.jpg'))
globtoconvert = sorted(globtoconvert)
#print globtoconvert
for f in globtoconvert:
    
    #print globtoconvert
    try:
        altnum = 1
        fname = os.path.abspath(f).split('/')[-1].split('_')[0]

        pdirname = os.path.dirname(f)

        ext = f.split('.')[-1]
        
        renamed = os.path.join(pdirname, fname + '_' + str(altnum) + '.' + ext)
        
        while os.path.isfile(renamed):
            renamed = os.path.join(pdirname, fname + '_' + str(altnum) + '.' + ext)
            altnum += 1
            print "{} exists".format(renamed)    
            
        
        os.rename(f, renamed)
        print renamed
    except OSError:
        print "Ugh"