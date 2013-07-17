#!/usr/bin/env python
#from pythonstartup import csv_read_file
import csv,os,sys



csvfile='/Users/johnb/nne/bell617.csv'

#####
#csvfile=sys.argv[1]
#####
#
#####
#if sys.argv[2]:
#    procdir = sys.argv[2]
#    os.chdir(procdir)
#else:
#    procdir = '.'
#####

procdir = '/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/vendor_dropoff/vintage_bella_bags/118110'
os.chdir(procdir)


missingdict = {}
with open(csvfile,'rbU') as f:
    reader = csv.reader(f,dialect=csv)

    for row in reader:
        try:
            colorstyle = row[0]
            colorstylefile = colorstyle + ".jpg"
            vendorstyle = row[1]
            vendorfile = vendorstyle + ".jpg"
            os.chdir(procdir)
            os.rename(vendorfile,colorstyle)
            print "Success: {0}".format(colorstyle)
        except OSError:
            print "Not Found: {0}".format(row[0])