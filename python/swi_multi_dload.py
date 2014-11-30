#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, datetime

def sqlQuery_GetStyleVendor_ByPO(ponum=None):
    import sqlalchemy, sys, re
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()

    if ponum:
        querymake_StylesByPO="SELECT POMGR.PRODUCT_COLOR.ID AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR.PO_LINE.PO_HDR_ID AS ponumber FROM POMGR.PRODUCT_COLOR INNER JOIN POMGR.PO_LINE ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.PO_LINE.PO_HDR_ID = '" + ponum + "' AND PRODUCT_COLOR.IMAGE_READY_DT is null"
    else:
        ## Get all missing SWISS WATCH Styles vs above which takes a PO list
        querymake_StylesByPO="""SELECT POMGR.PRODUCT_COLOR.ID      AS colorstyle,
                                POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style,
                                POMGR.PO_LINE.PO_HDR_ID          AS ponumber
                                FROM POMGR.PRODUCT_COLOR
                                RIGHT JOIN POMGR.PO_LINE
                                ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID
                                RIGHT JOIN POMGR.PO_HDR
                                ON POMGR.PO_LINE.PO_HDR_ID = POMGR.PO_HDR.ID
                                RIGHT JOIN POMGR.VENDOR
                                ON POMGR.VENDOR.ID                        = POMGR.PO_HDR.VENDOR_ID
                                WHERE POMGR.VENDOR.NAME like '%SWI%'
                                and POMGR.PRODUCT_COLOR.IMAGE_READY_DT IS NULL
                                ORDER BY POMGR.PRODUCT_COLOR.IMAGE_READY_DT DESC nulls Last"""

    result = connection.execute(querymake_StylesByPO)
    styles = {}
    regex = re.compile(r'^\d{8}[^0]{1}$')
    for row in result:
        if regex.findall(str(row['colorstyle'])):
            style = {}
            style['colorstyle'] = str(row['colorstyle'])
            style['ponumber'] = str(row['ponumber'])
            styles[row['vendor_style']] = style
            #print style
        else:
            pass
    connection.close()
    return styles


def define_variables_mkdirs():
    import os,sys
    maclinux_prefix=os.path.abspath(os.path.expanduser('~')).split('/')[1]
    if maclinux_prefix == 'Users':
        destdir=os.path.join('/Volumes','Post_Complete/Complete_Archive/MARKETPLACE/SWI')
    elif maclinux_prefix == 'home' or maclinux_prefix == 'root':
        destdir=os.path.join('/mnt','Post_Complete/Complete_Archive/MARKETPLACE/SWI')
    else:
        destdir=os.path.join(os.path.abspath(os.path.expanduser('~')),'MARKETPLACE/SWI')
    try:
        os.makedirs(destdir, 16877)
    except OSError:
        pass
    except:
        destdir=os.path.join(os.path.abspath(os.path.expanduser('~')),'MARKETPLACE/SWI')
        try:
            os.makedirs(destdir, 16877)
        except OSError:
            pass

    #setattr(globals,'destdir',destdir)
    globals()['destdir'] = destdir
    return destdir


def url_download_file(image_url,filepath,errdir=None):
    import urllib, os, io, cStringIO, requests

    ## Split Vendor # to try again on fail of full VENDOR_STYLE_NO
    url_split = image_url.split('/')[-1]
    url_split = url_split.split('-')[1:]
    url_split = '-'.join(url_split)
    url_parent = image_url.split('/')[:-1]
    url_parent = '/'.join(url_parent)
    backupurl = image_url.replace('admin.swisswatchintl.com/Z/', 'admin.swisswatchintl.com/H/')
    backup_spliturl = os.path.join(url_parent, url_split).replace('admin.swisswatchintl.com/Z/', 'admin.swisswatchintl.com/H/')
    headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:33.0) Gecko/20100101 Firefox/33.0'}

    error_check = requests.get(image_url, stream=True, timeout=1, headers=headers)
    urlcode_value = error_check.status_code()
    print urlcode_value

    ### PRIMARY URL, AKA /Z/
    import httplib2
    image_url = httplib2.urlnorm(httplib2.urllib.unquote(image_url))[-1]
    print 'RRR'
    print image_url, filepath #.split('/' )[-1].replace('.jpg','_1200.jpg')
    res = requests.get(image_url, stream=True, timeout=1, headers=headers)
    print 'ALMOST'
    urlcode_value = res.status_code
    print urlcode_value
    if urlcode_value == 200:
        res = requests.get(url_split, stream=True, timeout=1, headers=headers)
        with open(filepath, 'ab+') as f:
            f.write(res.content)
            f.close()
    elif urlcode_value == 404:

        ### Split URL, /Z/
        urlsplit = os.path.join(url_parent, url_split)
        error_check = requests.get(url_split, stream=True, timeout=1, headers=headers)
        split_urlcode_value = error_check.status_code()

        ### Backup URL, AKA /H/
        error_check = requests.get(backupurl, stream=True, timeout=1, headers=headers)
        backup_urlcode_value = error_check.status_code()

        ### BackupSplit
        error_check = urllib.urlopen(backup_spliturl)
        error_check = requests.get(backup_spliturl, stream=True, timeout=1, headers=headers)
        backup_spliturlcode_value = error_check.status_code()


        if split_urlcode_value == 200:
            res = requests.get(url_split, stream=True, timeout=1, headers=headers)
            with open(filepath, 'ab+') as f:
                f.write(res.content)
                f.close()
            # print "On 2nd Attempt, Retrieved: " + urlsplit + " ---> " + filepath

        elif backup_urlcode_value == 200:
            # urllib.urlretrieve(backupurl, filepath.replace('.jpg', '_H.jpg'))
            res = requests.get(backupurl, stream=True, timeout=1, headers=headers)
            with open(filepath, 'ab+') as f:
                f.write(res.content)
                f.close()
            #print "Downloaded URL {0} Finally on 3rd and Final Attempt with Error Code {1}".format(backupurl, backup_urlcode_value)
        elif backup_spliturlcode_value == 200:
            # urllib.urlretrieve(backup_spliturl, filepath.replace('.jpg', '_HH.jpg'))
            res = requests.get(backup_spliturl, stream=True, timeout=1, headers=headers)
            with open(filepath, 'ab+') as f:
                f.write(res.content)
                f.close()
            #print "Didnt Fail Downloading URL {0} even on 3rd and Final Attempt with Error Code {1}".format(backup_spliturl, backup_spliturlcode_value)
        else:
            #print "AWFUL Totally Failed Downloading URL {0} on 2nd Attempt with Error Code {1}".format(image_url, urlcode_value)
            # print "TERRIBLE Failed Downloading URL {0} even on 3rd and Final Attempt with Error Code {1}".format(backupurl, backup_urlcode_value)
            try:
                errdir=os.path.join('/mnt','Post_Complete/Complete_Archive/MARKETPLACE/SWI/ERRORS')
                try:
                    os.makedirs(errdir, 16877)
                except OSError:
                    pass
                colorstyle = filepath.split('/')[-1][:9]
                alt        = filepath.split('/')[-1].split('_')[-1][0]
                if alt.isdigit():
                    alt = str(alt)
                elif alt == 'a':
                    alt = str(alt)
                else:
                    alt = '1'
                try:
                    #info = cStringIO.StringIO()
                    with io.open(os.path.join(os.path.abspath(errdir), colorstyle + '_' + alt + '_error404.txt'), mode='wt+') as f:

                        info = "{0},{1},{2},{3}".format(str(colorstyle), str(alt), str(urlcode_value), str(image_url))
                        outtext = unicode(info, 'utf-8')
                        print outtext
                        print >>f, outtext
                        #info.flush()
                        #f.write(info.getvalue())
                        #f.write()
                        #info.close()
                        f.flush()
                        f.close()
                except AttributeError:
                    pass

            except OSError:
                pass

    else:
        print "{0} Error:\v {1} is not a valid URL".format(urlcode_value,image_url)


def get_postyles_dict(polist=None):
    import os,sys

    #print polist


    stylesDictsDict = []
    if polist:
        for ponum in polist:
            try:
                stylesDict = sqlQuery_GetStyleVendor_ByPO(ponum=ponum)
                stylesDictsDict.append(stylesDict)
            except:
                pass
    else:
        stylesDictsDict = sqlQuery_GetStyleVendor_ByPO(ponum=None)
    return stylesDictsDict


def download_urls_bypo(ponum):
    import os
    destdir = ''

    if not destdir:
        destdir = define_variables_mkdirs()
    originaldest = destdir

    stylesDict = sqlQuery_GetStyleVendor_ByPO(ponum=ponum)
    for k,v in stylesDict.iteritems():
        # print k,v
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
        destdir = os.path.join(os.path.abspath(originaldest),ponumber)
        try:
            os.makedirs(destdir, 16877)
        except OSError:
            pass

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
        except IOError:
            print "Failed {}{}".format(vendor_url,colorstyle_file)
            pass
        ##_2
        try:
            url_download_file(vendor_url_side,colorstyle_side_file)
            print "Downloaded {}".format(colorstyle_side_file)
        except IOError:
            print "Failed {}{}".format(vendor_url,colorstyle_side_file)
            pass
        ## _3
        try:
            url_download_file(vendor_url_back,colorstyle_back_file)
            print "Downloaded {}".format(colorstyle_back_file)
        except IOError:
            try:
                url_download_file(vendor_url_back,colorstyle_back_file.replace('-back','-clasp'))
                print "Downloaded {}".format(colorstyle_back_file.replace('-back','-clasp'))
            except IOError:
                try:
                    url_download_file(vendor_url_back,colorstyle_back_file.replace('-back','-Clasp'))
                except IOError:
                    print "Failed {}{}".format(vendor_url,colorstyle_back_file.replace('-back','-Clasp'))
        # # Try to remove empty dirs
        # try:
        #     os.rmdir(destdir)
        # except:
        #     pass

##
## Run MAin as a multiprocessor by PO
def run_multiproccesses_download(cmd_process=None,args=None):
    import multiprocessing

    pool = multiprocessing.Pool(8)

    if not args:
        # args = get_postyles_dict()
        popre= get_postyles_dict()
        polist = []
        for v in popre.itervalues():
            po = v['ponumber']
            polist.append(po)

        args = sorted(list(set(sorted(polist))),reverse=True)
    try:
        funx = getattr(sys.modules[__name__], unicode(cmd_process))
        results = pool.map(funx,args)
        #print type(results)

        # close the pool and wait for the work to finish
        pool.close()
        print 'PoolClose'
        pool.join()
        print 'PoolJoin'
    except TypeError:
        print 'Failed with args {}'.format(args)
        pass # raise TypeError

if __name__ == '__main__':
    import sys,time
    start_time = time.strftime('%X')
    try:

        #mod  = importlib.import_module(swi_multi_dload)
        mod =  dir(sys.modules[__name__])

        ## Multiproc download incomlpete files by po
        func =  'download_urls_bypo'
        run_multiproccesses_download(cmd_process=func,args=None)
        ## Now Process and Load Em
        dload_end = time.strftime('%X')
        #print "Time to Complete Download Stage {0}".format(int(dload_end.strip(':')) - int(start_time.strip(':')))

        import multiprocmagick
        try:
            searchdir = globals()['destdir']
        except KeyError:
            searchdir = define_variables_mkdirs()
        multiprocmagick.run_multiproccesses_magick(searchdir=searchdir)
        #print "Time to Complete MagickProcessor Stage {0}".format(int(time.strftime('%X').strip(':')) - int(dload_end.strip(':')))
        # (int(time.strftime('%X').strip(':')) - int(start_time.strip(':')))
        print "Times for All Stages {0}".format(str(start_time) + '_' + str(dload_end)+'_' + str(time.strftime('%X')))


    except IndexError:
        print 'EXCEPT MAIN only'
