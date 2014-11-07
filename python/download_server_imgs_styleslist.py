#!/usr/bin/env python
import os, sys, re, csv


def url_download_file(url,filepath):
    import urllib
    #error_check = urllib.urlopen(url)
    #urlcode_value = error_check.getcode()
    #print urlcode_value
    
    #if urlcode_value == 200:
    urllib.urlretrieve(url, filepath)
    print "Retrieved: " + url + " ---> " + filepath
    #    return urlcode_value
    #elif urlcode_value == 404:
    #    return urlcode_value


#### Run ###
main(styleslist=None, root_dir=None):
    import os,sys, urllib, datetime
    todaysdate = '{:%Y,%m,%d}'.format(datetime.datetime.now())
    if not root_dir:
        root_dir = os.path.join(os.path.abspath(os.path.expanduser('~')), 'Pictures', todaysdate + '_downloads')
        if not os.path.isdir(root_dir):
            os.makedirs(root_dir)
    if not styleslist:
        args = sys.argv[1:]
    else:
        args = styleslist

    regex_r = re.compile(r'.*?\r.*?')
    regex_n = re.compile(r'.*?\n.*?')
    regex_Space = re.compile(r'.*?\n.*?')


    #args1 = args[0].split('\n')   #(','.join(str(arg) for arg in args)).split('\n')
    try:
        args1 = args[0].split(' ')   #(','.join(str(arg) for arg in args)).split('\n')
    except KeyError:
        pass
    try:
        if len(args1) >= 2:
            styleslist = args1
            print "HELLO Greater 2"
            print len(styleslist)
            
        elif len(args1) == 1:
            ponum = args[0] #sys.argv[1]#ys.argv[1]#args_split #sys.argv[1]
            print ponum
            styleslist = sqlQuery_GetStyleVendor_ByPO(ponum)
            #print stylesDict
    #        #ponum = '119071'
    except OSError:
        print "Enter at least PO Number as 1st Arg or Nothing will Happen"
#


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
        colorstyle_file = os.path.join(os.path.abspath(os.curdir), colorstyle + ext_PNG)
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