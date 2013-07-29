#!/usr/bin/env python

def url_download_file(url,filepath):
    import urllib
    error_check = urllib.urlopen(url)
    urlcode_value = error_check.getcode()
    print urlcode_value
    if urlcode_value == 200:
        urllib.urlretrieve(url, filepath)
        print "Retrieved: " + url + " ---> " + filepath
    elif urlcode_value == 404:
        url_split = url.split('/')[-1]
        url_split = url_split.split('-')[1:]
        url_split = '-'.join(url_split)       
        url_parent = url.split('/')[:-1]
        url_parent = '/'.join(url_parent)
        url = os.path.join(url_parent, url_split)
        try:
            urllib.urlretrieve(url, filepath)
            print "Retrieved: " + url + " ---> " + filepath
        except:
            print "Failed {0} on 2nd Try".format(url)
    else:
        print "{0} Error:\v {1} is not a valid URL".format(urlcode_value,url)
        


def build_url_colorstyle_dict(file):
    import csv
    filedict = {}
    with open(file, 'rb') as f:
        reader = csv.reader(f, dialect=csv)
        for row in reader:
            localdict = {}
            localdict['url'] = row[2]
            localdict['style'] = row[1]
            filedict[row[1]] = localdict
    return filedict


########### RUN ########

import csv,datetime,os,sys
dt = str(datetime.datetime.now())
today = dt.split(' ')[0]

## Should be run after Imap get attachments so that todays swi file is used
try:
    file = sys.argv[1]
except:
    file = os.path.join('/mnt/Post_Complete/.Vendor_to_Load/feeds', today + '_sku-luxury-conv.csv')

## Completed Downloads
upload_drop = '/mnt/Post_Complete/.Vendor_to_Load/upload_drop'
daily_dir = os.path.join(upload_drop, today + '_jpgs')
try:
    os.mkdir(daily_dir, 16877)
except OSError:
    pass


filedict = build_url_colorstyle_dict(file)


for k,v in filedict.iteritems():
    os.chdir(daily_dir)
    vendor_url = v['url']
    colorstyle = k + ".jpg"
    colorstyle_file = os.path.join(os.path.abspath(os.curdir), colorstyle)
    #print vendor_url, colorstyle_file
    url_download_file(vendor_url,colorstyle_file)
#print swiurl
        
        
#for k,v in stylesDict.iteritems():
#    for val in v:
#        vendor_url = 'http://admin.swisswatchintl.com/Z/'
#        vendor_style = k + ".jpg"
#        colorstyle = str(v[val]) + ".jpg"
#        #vendor_stripped = k
#        vendor_file = vendor_url + vendor_style
#
#        colorstyle_file = os.path.join(os.path.abspath(os.curdir), colorstyle)
#        # 
#        #print vendor_file, colorstyle_file
#        #try:
#        url_download_file(vendor_file,colorstyle_file)