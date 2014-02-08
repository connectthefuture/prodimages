#!/usr/bin/python
def csv_write_datedOutfile(lines):
    import csv,datetime,os
    dt = str(datetime.datetime.now())
    today = dt.split(' ')[0]
    f = os.path.join(os.path.expanduser('~'), today + '_write.csv')
    for line in lines:
        with open(f, 'ab+') as csvwritefile:
            writer = csv.writer(csvwritefile, delimiter=',')
            writer.writerows([lines])


def readxl_outputdict(workbk=None):         
    import csv,xlrd,sys
#    workbk = sys.argv[1]
book = xlrd.open_workbook(workbk)##sys.argv[1])
sh = book.sheet_by_index(0)

#convWriter = csv.writer(sys.stdout,delimiter=',', dialect='excel')
numcols=sh.ncols
outdict = {}
for rx in range(sh.nrows):
    rowdict = {}    
    for cx in range(sh.ncols):
        rowhead = sh.cell_value(rowx=0,colx=cx)
        rowval = sh.cell_value(rowx=rx,colx=cx)
        rowdict[rowhead] = rowval
        outdict[rx] = rowdict
return outdict

###########
import sys,os

workbk = sys.argv[1]

outdict = readxl_outputdict(workbk)


for rowout in outdict.items():
    #print k,
    for val in rowout:
        try:
            for valn,valv in val.items()[:]:
                lines = rowout[0],valn,valv,
                print lines,
                #csv_write_datedOutfile(lines.encode('ascii', 'replace'))
        except AttributeError:
            pass

