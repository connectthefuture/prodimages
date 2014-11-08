#!/usr/bin/env python
import os, sys, re, csv


def url_download_file(url,filepath):
    import urllib, subprocess
    #error_check = urllib.urlopen(url)
    #urlcode_value = error_check.getcode()
    #print urlcode_value
    
    #if urlcode_value == 200:
    try:
        urllib.urlretrieve(url, filepath)
        print "Retrieved: " + url + " ---> " + filepath
    except:
        print  'FAILED ', url, filepath
        pass
    #    return urlcode_value
    #elif urlcode_value == 404:
    #    return urlcode_value


#### Run ###
def main(styleslist=None, root_dir=None):
    import os,sys, urllib, datetime
    todaysdate = '{:%Y%m%d}'.format(datetime.datetime.now())
    username = os.path.expanduser('~').split('/')[-1].split('.')[0].lower()
    if not root_dir:
        root_dir = os.path.join(os.path.abspath(os.path.expanduser('~')), 'Pictures', todaysdate + '_files_for_' + username )
        if not os.path.isdir(root_dir):
            os.makedirs(root_dir)
    if not styleslist:
        styleslist = sys.argv[1:]
    else:
        pass
    # print 'Args ', sys.argv[0]
    regex_r = re.compile(r'.*?\r.*?')
    regex_n = re.compile(r'.*?\n.*?')
    regex_Space = re.compile(r'.*?\s.*?')
    print styleslist

    # styleslist1 = styleslist[0].split('\n')   #(','.join(str(arg) for arg in styleslist)).split('\n')
    # try:
    #     styleslist1 = styleslist[0].split(' ')   #(','.join(str(arg) for arg in styleslist)).split('\n')
    # except KeyError:
    #     pass
    # print styleslist1

    for style in styleslist:

        netsrv101_url = 'ftp://imagedrop:imagedrop0@netsrv101.l3.bluefly.com//mnt/images/images/'
        colorstyle = str(style)
        ext_PNG     = '.png'
        ext_JPG     = '.jpg'

        netsrv101_url_file = os.path.join(netsrv101_url, colorstyle[:4], colorstyle + ext_PNG)
    #try:
        #error_check = urllib.urlopen(netsrv101_url_file)
        #urlcode_value = error_check.getcode()
        #print urlcode_value
        #try: #if urlcode_value == 200:
        colorstyle_file = os.path.join(root_dir, colorstyle + ext_PNG)
        print netsrv101_url_file, colorstyle_file
        try:
            url_download_file(netsrv101_url_file, colorstyle_file)
        
            alt = 0   
            for x in range(1,6):
                try:
                    alt = x   
                    ext_ALT = '_alt0{0}{1}'.format(str(alt),ext_PNG)
                    colorstylealt = colorstyle + ext_ALT
                    colorstyle_filealt = (root_dir, colorstylealt)
                    
                    netsrv101_url_filealt = os.path.join(netsrv101_url, colorstyle[:4], colorstylealt)
                    
                    #error_check = urllib.urlopen(netsrv101_url_filealt)
                    #urlcode_value = error_check.getcode()
                    #if urlcode_value == 200:
                    if url_download_file(netsrv101_url_filealt, colorstyle_filealt):
                        url_download_file(netsrv101_url_filealt, colorstyle_filealt)
                except IOError:
                    pass        
        except IOError:
            pass   


if __name__ == '__main__':
    main()