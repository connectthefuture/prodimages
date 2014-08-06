#!/usr/bin/env python
# -*- coding: utf-8 -*-

def sqlQuery_GetStyleVendor_ByPO(ponum=None):
    import sqlalchemy, sys
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()
    if ponum:
        querymake_StylesByPO="SELECT POMGR.PRODUCT_COLOR.ID AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR.PO_LINE.PO_HDR_ID AS ponumber FROM POMGR.PRODUCT_COLOR INNER JOIN POMGR.PO_LINE ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.PO_LINE.PO_HDR_ID = '" + ponum + "' AND PRODUCT_COLOR.IMAGE_READY_DT is null"
    else:
        ## Get all missing Styles vs above which takes a PO list
        querymake_StylesByPO="SELECT POMGR.PRODUCT_COLOR.ID AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR.PO_LINE.PO_HDR_ID AS ponumber FROM POMGR.PRODUCT_COLOR INNER JOIN POMGR.PO_LINE ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE PRODUCT_COLOR.IMAGE_READY_DT is null"

    result = connection.execute(querymake_StylesByPO)
    styles = {}
    for row in result:
        style = {}        
        style['colorstyle'] = row['colorstyle']
        style['ponumber'] = row['ponumber']
        styles[row['vendor_style']] = style
        
    connection.close()
    return styles


def define_variables_mkdirs():
    import os,sys
    maclinux_prefix=os.path.abspath(os.path.expanduser('~')).split('/')[1]
    if maclinux_prefix == 'Users':
        destdir=os.path.join('/Volumes','Post_Complete/Complete_Archive/MARKETPLACE/SWI/images')
    elif maclinux_prefix == 'home' or maclinux_prefix == 'root':
        destdir=os.path.join('/mnt','Post_Complete/Complete_Archive/MARKETPLACE/SWI/images')
    else:
        destdir=os.path.join(os.path.abspath(os.path.expanduser('~')),'MARKETPLACE/SWI/images')

    try:
        os.makedirs(destdir, 16877)
    except OSError:
        pass
    except:
        destdir=os.path.join(os.path.abspath(os.path.expanduser('~')),'MARKETPLACE/SWI/images')
        try:
            os.makedirs(destdir, 16877)
        except OSError:
            pass
    return destdir

     
def url_download_file(url,filepath):
    import urllib
    
    ## Split Vendor # to try again on fail of full VENDOR_STYLE_NO
    url_split = url.split('/')[-1]
    url_split = url_split.split('-')[1:]
    url_split = '-'.join(url_split)       
    url_parent = url.split('/')[:-1]
    url_parent = '/'.join(url_parent)
    backupurl = url.replace('admin.swisswatchintl.com/Z/', 'admin.swisswatchintl.com/H/')
    backup_spliturl = os.path.join(url_parent, url_split).replace('admin.swisswatchintl.com/Z/', 'admin.swisswatchintl.com/H/')
    
    
    error_check = urllib.urlopen(url)
    urlcode_value = error_check.getcode()
    print urlcode_value
    
    ### PRIMARY URL, AKA /Z/
    if urlcode_value == 200:
        urllib.urlretrieve(url, filepath)
        print "Retrieved: " + url + " ---> " + filepath
    
    elif urlcode_value == 404:
        
        ### Split URL, /Z/
        urlsplit = os.path.join(url_parent, url_split)
        error_check = urllib.urlopen(urlsplit)
        split_urlcode_value = error_check.getcode()        
        
        ### Backup URL, AKA /H/
        error_check = urllib.urlopen(backupurl)
        backup_urlcode_value = error_check.getcode()

        ### BackupSplit
        error_check = urllib.urlopen(backup_spliturl)
        backup_spliturlcode_value = error_check.getcode()
        
            
        if split_urlcode_value == 200:
            urllib.urlretrieve(urlsplit, filepath)
            print "On 2nd Attempt, Retrieved: " + urlsplit + " ---> " + filepath
            
        elif backup_urlcode_value == 200: 
            # urllib.urlretrieve(backupurl, filepath.replace('.jpg', '_H.jpg'))
            urllib.urlretrieve(backupurl, filepath)
            print "Downloaded URL {0} Finally on 3rd and Final Attempt with Error Code {1}".format(backupurl, backup_urlcode_value)
        elif backup_spliturlcode_value == 200: 
            # urllib.urlretrieve(backup_spliturl, filepath.replace('.jpg', '_HH.jpg'))
            urllib.urlretrieve(backup_spliturl, filepath)
            print "Failed Downloading URL {0} even on 3rd and Final Attempt with Error Code {1}".format(backup_spliturl, backup_spliturlcode_value)      
        else:
            print "AWFUL Totally Failed Downloading URL {0} on 2nd Attempt with Error Code {1}".format(url, urlcode_value)
            print "TERRIBLE Failed Downloading URL {0} even on 3rd and Final Attempt with Error Code {1}".format(backupurl, backup_urlcode_value)    
        

    else:
        print "{0} Error:\v {1} is not a valid URL".format(urlcode_value,url)


def get_postyles_dict(polist=None):
    import os,sys

    print polist
    stylesDictsDict = []
    if polist:
        for ponum in polist:
            try:
                stylesDict = sqlQuery_GetStyleVendor_ByPO(ponum)
                stylesDictsDict.append(stylesDict)
            except:
                pass
    else:
        stylesDictsDict = sqlQuery_GetStyleVendor_ByPO(ponum=None)
    return stylesDictsDict


def download_urls_bypo(stylesDictsDict):
    destdir = ''
    
    if not destdir:
        destdir = define_variables_mkdirs()
    
    originaldest = destdir

    for stylesDict in stylesDictsDict:
        if type(stylesDictsDict) == dict:
            stylesDict = stylesDictsDict
        else:
            pass
        for k,v in stylesDict.iteritems():
                
            vendor_url = "http://admin.swisswatchintl.com/Z/{0}.jpg".format(k)
            vendor_url_side = vendor_url.replace('.jpg', '-side.jpg')
            vendor_url_back = vendor_url.replace('.jpg', '-back.jpg')
            vendor_url_boxset = vendor_url.replace('.jpg', '-boxset.jpg')
            vendor_url_straps = vendor_url.replace('.jpg', '-straps.jpg')
            vendor_url_main = vendor_url.replace('.jpg', '-main.jpg')

            
            style = str(v['colorstyle'])
            ponumber = str(v['ponumber'])
            colorstyle = ''
            colorstyle =  style          +   "_1.jpg"
            colorstyle_side = style      +   "_2.jpg"
            colorstyle_back = style      +   "_3.jpg"
            colorstyle_boxset = style    +   "_4.jpg"
            colorstyle_straps = style    +   "_5.jpg"
            colorstyle_main = style      +   "_6.jpg"
            
            # Make the subdir by POnum
            # destdir = os.path.join(os.path.abspath(originaldest),ponumber)
            # try:
            #     os.makedirs(destdir, 16877)
            # except OSError:
            #     pass
            
            colorstyle_file = os.path.join(os.path.abspath(destdir), colorstyle)
            colorstyle_side_file = os.path.join(os.path.abspath(destdir),colorstyle_side)
            colorstyle_back_file = os.path.join(os.path.abspath(destdir), colorstyle_back)
            colorstyle_boxset_file = os.path.join(os.path.abspath(destdir), colorstyle_boxset)
            colorstyle_straps_file = os.path.join(os.path.abspath(destdir), colorstyle_straps)
            colorstyle_main_file = os.path.join(os.path.abspath(destdir), colorstyle_main)


            #imagefalse = sqlQuery_GetStyleVendor_ByPO()
            #if imagefalse:
            
            ##_1
            try:            
                url_download_file(vendor_url,colorstyle_file)
            except:
                print "Failed {}{}".format(vendor_url,colorstyle_file)

            ##_2
            try:            
                url_download_file(vendor_url_side,colorstyle_side_file)
                print "Downloaded {}".format(colorstyle_side_file)
            except:
                print "Failed {}{}".format(vendor_url,colorstyle_side_file)

            ## _3
            try:            
                url_download_file(vendor_url_back,colorstyle_back_file)
                print "Downloaded {}".format(colorstyle_back_file)
            except:
                try:
                    url_download_file(vendor_url_back,colorstyle_back_file.replace('-back','-clasp'))
                    print "Downloaded {}".format(colorstyle_back_file.replace('-back','-clasp'))
                except:
                    try:
                       url_download_file(vendor_url_back,colorstyle_back_file.replace('-back','-Clasp'))
                    except:
                        print "Failed {}{}".format(vendor_url,colorstyle_back_file.replace('-back','-Clasp'))


## Run MAin as a multiprocessor by PO
def run_multiproccesses_download(cmd_process=None,args=None):
    import multiprocessing
    import glob,os
    
    pool = multiprocessing.Pool(4)
    
    if not args:
        args = get_postyles_dict()
    #cmd_process = getattr(.,"{}".format(cmd_process)) #locals()["{}".format(cmd_process)]()
    #func = getattr(sys.modules[__name__], 'download_urls_bypo')
    print type(args)
    print type(dir(sys.modules[__name__]['download_urls_bypo']))
    results = pool.map(download_urls_bypo,args)
    print type(results)
    
    # close the pool and wait for the work to finish
    pool.close()
    print 'PoolClose'
    pool.join()
    print 'PoolJoin'


if __name__ == '__main__':
    import sys, importlib
    
    try:
        polist = set(list(sys.argv[1:]))
        stylesDictsDict = get_postyles_dict(polist)

        #mod  = importlib.import_module(swi_multi_dload)
        mod =  dir(sys.modules[__name__])
        mod3 = dir(__name__)
        print mod,mod3
        func =  'download_urls_bypo'
        run_multiproccesses_download(cmd_process=func,args=stylesDictsDict)
    
    except IndexError:

        try:
            popre= get_postyles_dict()
            polist = []
            for k,v in propre.iteritems():
                po = v['ponumber']
                polist.append(po)
            
            stylesDictsDict = get_postyles_dict(polist)

            #mod  = importlib.import_module(swi_multi_dload)
            mod =  dir(sys.modules[__name__])
            print mod,mod3
            
            func =  'download_urls_bypo'
            run_multiproccesses_download(cmd_process=func,args=stylesDictsDict)
        except:
            print 'EXCEPT MAIN only'
            
