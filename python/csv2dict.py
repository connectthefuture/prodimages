# -*- coding: utf-8 -*-
#!/usr/bin/env python

def csv2dict(csvfile):
    import csv
    count = 0
    with open(csvfile, mode='rbU') as infile:
        reader = csv.reader(infile)
        with open(csvfile.replace('.csv','_dict.csv'), mode='w') as outfile:
            writer = csv.writer(outfile)
            count += 1
            mydict = {rows[0]:rows[1] for rows in reader}
            writer.write(mydict.items())
    return mydict

####################################################################################################
########################################   RUN   ###################################################
####################################################################################################
def main(csvdata=None):
    import os, sys, re, csv

    try:
        if not csvdata:
            csvdata = sys.argv[1]
        else: pass

    except:
        pass

    try:
        csv2dict(csvdata)
        print "{} has now been converted to a Dict".format(csvdata.split('/')[-1])
    except:
        print "{0} Failed during conversion. Check the input file:\n\t{1} for formatting errors".format(
            csvdata.split('/')[-1], csvdata)


if __name__ == '__main__':
    main()