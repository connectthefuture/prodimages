#!/usr/bin/env python
import os, sys, re, csv


def subproc_pad_to_x480(file,destdir):
    import subprocess, os
    
    fname = file.split(".")[0]
    ext = file.split(".")[-1]
    outfile = os.path.join(destdir, fname + "_" + "l" + ".jpg")
    
    try:
            
        subprocess.call([
            "convert",
            file,
            "-format",
            "jpg",
            "-resize",
            "350x432",
            "-background",
            "white",
            "-gravity",
            "center",
            "-extent",
            "400x480",
            outfile,
        ])

    except:
        print "Failed: {0}".format(file)
    return outfile


######################
destdir = os.path.abspath(sys.argv[1])

######################

os.chdir(destdir)
for f in os.listdir(destdir):
    try:
        
        padded_file = subproc_pad_to_x480(f,destdir)
        print 'Success!! Nice one, you just padded this----->{}'.format(f)
    except:
        print 'Booo, this ----->{} failed'.format(f)
        pass