# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os, sys, re, csv



def csv2dict(csvfile):
    import csv
    count = 0
    with open(csvfile, mode='rbU') as infile:
        reader = csv.reader(infile)
        with open(csvfile.replace('.csv','_dict.csv'), mode='w') as outfile:
            writer = csv.writer(outfile)
            count += 1
#            try:
#                col2 = rows[1]
#            except IndexError:
#                col2 = ''
#            col1 = rows[0]
#            if not col2:
#                col2 = col1
#                col1 = count
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
    except OSError:
        print "{0} Failed during conversion. Check the input file:\n\t{1} for formatting errors".format(csvdata.split('/')[-1], csvdata)
