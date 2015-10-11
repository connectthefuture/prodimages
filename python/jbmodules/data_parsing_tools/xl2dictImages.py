#!/usr/bin/env python
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
    for rx in xrange(sh.nrows):
        rowdict = {}    
        for cx in xrange(sh.ncols):
            rowhead = sh.cell_value(rowx=0,colx=cx)
            rowval = sh.cell_value(rowx=rx,colx=cx)
            rowdict[rowhead] = rowval
            outdict[rx] = rowdict
    return outdict


def compile_outdict_by_rowkeys(outdict):
    from collections import defaultdict
    d = defaultdict(list)
    for r in outdict.items():
        dd = defaultdict(dict)
        for val in r[1].items():
            try:
                if type(val[1]) == float:
                    value = str(int(val[1]))#"{0:.0}".format(val[1])
#                    if len(value) == 9:
#                        print "Style {0}".format(value)
#                    else:
#                        print "PO# {0}".format(value)
                        
                else:
                    value = val[1]
                #print type(val[1])
                #print r[0],val[0],value
                dd[val[0]]=value
                d[r[0]] = dd
                #print dd
                #csv_write_datedOutfile(lines.encode('ascii', 'replace'))
            except AttributeError:
                pass
    return d

def output_imgurl_dict(dictinclurls):
    from collections import defaultdict
    import re
    colorstyles_vendorimgs = defaultdict(list)
    regex_url = re.compile(r'.*?[.][jJpPnNgG]{3}$')
    regex_colorstyle = re.compile(r'^[1-9][0-9]{8}$')
    for k,v in dictinclurls.iteritems():
        imageurls = []
        for val in v:
            if re.findall(regex_url,v[val]):
                imgurl =  v[val]#, k,val
                imageurls.append(imgurl)
            if re.findall(regex_colorstyle,v[val]):
                style = v[val]
                colorstyles_vendorimgs[style] = imageurls
    return colorstyles_vendorimgs

############################################
############################################

def main():
    import sys

    try:
        workbk = sys.argv[1]

    except:
        workbk = xlfile
    outdict = readxl_outputdict(workbk)
    compiled_rows = compile_outdict_by_rowkeys(outdict)
    colorstyle_vendorimages = output_imgurl_dict(compiled_rows)
    for k,v in colorstyle_vendorimages.iteritems():
        
        print k, sorted(v)

if __name__ == '__main__': 
    main()
    x = main()
    #print x