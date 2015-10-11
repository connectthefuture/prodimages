#!/usr/bin/env python
import os, sys, re, csv

def sqlquery_getvendornum_fromstylenum(colorstyle):
    import sqlalchemy
#    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()    
    
    querymake_consig_stylefix="SELECT POMGR.PRODUCT_COLOR.ID AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR.PO_LINE.PO_HDR_ID AS po_hdr_id FROM POMGR.PRODUCT_COLOR INNER JOIN POMGR.PO_LINE ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.PRODUCT_COLOR.ID LIKE '" + colorstyle + "%'"
    
    result = connection.execute(querymake_consig_stylefix)
    consigstyles = {}
    for row in result:
        consigstyle = {}        
        consigstyle['colorstyle'] = row['colorstyle']
        #consigstyle['vendor_style'] = row['vendor_style']
        consigstyles[row['vendor_style']] = consigstyle
        
    #print consigstyles
    connection.close()
    return consigstyles


def swi_product_dict(csvfile,fieldnames):
    import csv
    
    csvfile = open(csvfile,'rbU')
    reader = csv.DictReader(csvfile,fieldnames,delimiter=',')
    
    completedict = {}
    for line in reader:
        tmpdict = {}
        pipedict = {}
        dkey = line['SWI_SKU']
        tmpdict['SWI_SKU'] = line['SWI_SKU']
        tmpdict['COLORSTYLE'] = line['COLORSTYLE']
        tmpdict['IMAGE'] = line['IMAGE']
##        try:    
##            pipelist = line['FEATURES_PIPED']
##            pipelist = pipelist.split('|')
##
##            while len(pipelist) > 0:
##                try:
##                    #print len(pipelist)
##                    value = pipelist.pop()
##                    key = pipelist.pop()
##                    pipedict[key] = value
##                except IndexError:
##                    len(pipelist)
##            tmpdict['FEATURES_PIPED'] = pipedict
#        except AttributeError:
#            ##print "Attrib Error {}".format(line)
#            pass

        completedict[dkey] = tmpdict
    csvfile.close()
    return completedict

########################### RUN ###############################################
fieldnamelist = ["SWI_SKU","COLORSTYLE","IMAGE"]

feed_swi = '/Volumes/Post_Complete/.Vendor_to_Load/feeds/sku-conv.csv'

## Make Dict of Csvfile to search by SWI_SKU
swidict = swi_product_dict(feed_swi,fieldnamelist)


vendornums_to_check = {}

try:
    search_list = sys.argv[1:]
    print search_list
    for style in search_list:
        res = sqlquery_getvendornum_fromstylenum(style)
        colorstyle =  res.values()[-1]['colorstyle']
        vnum = res.items()[0][0]
        #vendornums_to_check.append(vnum)
        #print vnum, colorstyle
        vendornums_to_check[vnum] = colorstyle    
except OSError:
    print "Please submit a list to search"
    pass
    
    
print vendornums_to_check

for k,v in vendornums_to_check.iteritems():
    if swidict.get(k):
        imgurl = swidict.get(k)['IMAGE']
        colorstyle = swidict.get(k)['COLORSTYLE']
        renamed = imgurl.replace(imgurl.split('/')[-1].split('.')[0], colorstyle)
        filepath = os.path.abspath(os.path.join('/Users/johnb/Pictures', colorstyle + ".jpg"))
        #### Now try and download to Pictures dir
        import urllib
        error_check = urllib.urlopen(imgurl)
        urlcode_value = error_check.getcode()
        print urlcode_value
        if urlcode_value == 200:
            urllib.urlretrieve(imgurl, filepath)
        else:
            print "File not Found {0} Error:{1}".format(url, urlcode_value)
        
    