# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os, sys, re, csv



def csv2dict(csvfile):
    import csv
    with open(csvfile, mode='rbU') as infile:
        reader = csv.reader(infile)
        with open(csvfile.replace('.csv','_dict.csv'), mode='w') as outfile:
            writer = csv.writer(outfile)
            mydict = {rows[0]:rows[1] for rows in reader}
    return mydict
    
####################################################################################################
########################################   RUN   ###################################################
####################################################################################################

try:
    if sys.argv[1]:
        csvdata = sys.argv[1]
except:
    pass

    
if __name__ == '__main__':
    
    try:
        csv2dict(csvdata)
        print "{} has now been converted to a Dict".format(csvdata.split('/')[-1])
    except:
        print "{0} Failed during conversion. Check the input file:\n\t{1} for formatting errors".format(csvdata.split('/')[-1], csvdata)
