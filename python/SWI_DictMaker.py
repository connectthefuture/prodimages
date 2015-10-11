#!/usr/bin/env python
#from pythonstartup import csv_read_file

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
        tmpdict['BO_VARIANCE_ID'] = line['BO_VARIANCE_ID']
        tmpdict['STYLE'] = line['STYLE']
        tmpdict['STORE'] = line['STORE']
        tmpdict['CATEGORY'] = line['CATEGORY']
        tmpdict['SUBCATEGORY'] = line['SUBCATEGORY']
        tmpdict['BRAND_NAME'] = line['BRAND_NAME']
        tmpdict['TITLE'] = line['TITLE']
        tmpdict['QOH'] = line['QOH']
        tmpdict['WEIGHT'] = line['WEIGHT']
        tmpdict['PRODUCT_DESCRIPTION'] = line['PRODUCT_DESCRIPTION']
        tmpdict['MSRP'] = line['MSRP']
        tmpdict['SELL_PRICE'] = line['SELL_PRICE']
        tmpdict['YOUR_COST'] = line['YOUR_COST']
        tmpdict['IMAGE'] = line['IMAGE']
        pipelist = line['FEATURES_PIPED']
        pipelist = pipelist.split('|')

        while len(pipelist) > 0:
            try:
                #print len(pipelist)
                value = pipelist.pop()
                key = pipelist.pop()
                pipedict[key] = value
            except IndexError:
                len(pipelist)

        tmpdict['FEATURES_PIPED'] = pipedict
        completedict[dkey] = tmpdict
    csvfile.close()
    return completedict
    
def url_download_file_http(url):
    from time import time
    import os, urllib
    try:
        downloaddir = os.path.join(os.path.expanduser('~'), 'script_downloads')
        #downloaddir = os.path.join('/Users/johnb', 'script_dowloads')
        if not downloaddir:
            os.mkdir(downloaddir)
        filename = url.split('/')[-1]
        filepath =  os.path.join(downloaddir, filename)
        url_start = time()
        downloadfile = urllib.urlretrieve(url, filepath)
        url_end = time()
        #filepath.close()
        print "File: %s\vDownload Time -> %s"  % (filename,url_end - url_start)
    except OSError:
        print "OS Error {0}".format(filepath)
    except IOError:
        print "IO Error {0}".format(filepath)
    except AttributeError:
        print "Attribute Error - Type doesnt have a property requested {0}".format(filepath)    


def url_download_file_requests(url):
    r = requests.get(url)
    
    
    
import os,sys
en = os.environ
print en['PYTHONSTARTUP']
#csvfile = os.path.join(os.path.abspath(os.curdir),'BlueFly.csv')
csvfile = '/Users/johnb/Dropbox/Apps/PythonistaAppOnly/BlueFly.csv'
missingcsv = '/Users/johnb/Dropbox/Apps/PythonistaAppOnly/mistswis/missingswiwatch.csv'
#csvfile = os.path.join(os.path.abspath(os.curdir),'datafeedSAMPLE2.csv')
fieldnamelist = ["SWI_SKU","BO_VARIANCE_ID","STYLE","STORE","CATEGORY","SUBCATEGORY","BRAND_NAME","TITLE","QOH","WEIGHT","PRODUCT_DESCRIPTION","MSRP","SELL_PRICE","YOUR_COST","IMAGE","FEATURES_PIPED"]

## Make Dict of Csvfile
swidict = swi_product_dict(csvfile,fieldnamelist)

## IterItems Pulling Image + Download
#from PYTHON_FUNCTION_MASTER import url_download_file_http
count = len(swidict)
for k,v in swidict.iteritems():
    import urllib,csv
    #print found[1]['IMAGE']
    swi_image = v['IMAGE']
    swi_sku = v['SWI_SKU']
#    with open(missingcsv, 'rbU') as f:
    reader = csv.reader(open(missingcsv, 'rbU'),dialect=csv)
    for row in reader:
        print row[1]
        
        
    url_download_file_http(swi_image)
    count -= 1
    print "Downloads Remaining: {0}".format(count)    
#print swidict
