#!/usr/bin/env python
#from pythonstartup import csv_read_file
import csv,os,sys



csvfile='/Users/johnb/Documents/118491.csv'
procdir = '/Users/johnb/Downloads/118491'

#procdir = sys.argv[1]
#csvfile = sys.argv[2]

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

os.chdir(procdir)


missingdict = {}
with open(csvfile,'rbU') as f:
    reader = csv.reader(f,dialect=csv)
    
    for row in reader:
        #try:
        colorstyle = row[1]
        vendorstyle = row[0]
        os.chdir(procdir)
        for fn in os.listdir(os.path.abspath(os.curdir)):
            count = 1
            fname = fn.split('.')[0] + ".jpg"
            fname = fname.replace(':S',':S')
            print fn.split('_')[0].replace(':',':'), vendorstyle
            if fn.split('_')[0].replace(':',':') == vendorstyle:
                colorstylefile = os.path.join(os.path.abspath(os.curdir), colorstyle + "_" + str(count) + ".jpg")   
                while False:
                    colorstylefile = os.path.join(os.path.abspath(os.curdir), colorstyle + "_" + str(count) + ".jpg") 
                    os.path.isfile(vendorfile)
                    count += 1
                vendorfile = os.path.join(os.path.abspath(os.curdir), vendorstyle + "_" + str(count) + ".jpg") 
                colorstylefile = os.path.join(os.path.abspath(os.curdir), colorstyle + "_" + str(count) + ".jpg") 
                #print (fname,colorstylefile)
                os.rename(fn,colorstylefile)
                #os.system('mv' + " " + vendorfile + " " + colorstylefile)
                #print "Success: {0}".format(colorstyle)
        #except OSError:
            #print "Not Found: {0}".format(row[0])