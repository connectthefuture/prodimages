#!/usr/bin/env python
# -*- coding: utf-8 -*-
def styles_list():
    import sqlalchemy
    mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@localhost:3301/data_imagepaths')
    connection = mysql_engine.connect()
    query = """select distinct data.`file_path`, data.`photo_date`, data.`colorstyle`, CONCAT('/mnt/Post_Ready', t3.`file_path`),t3.`photo_date`
                FROM 
                    (SELECT t3.`available_ct`, t1.`file_path`, t1.`colorstyle`, t2.`image_ready_dt` , t1.`photo_date`,t1.`alt`
                    FROM `data_imagepaths`.`push_photoselects` t1 
                    join `data_imagepaths`.`product_snapshot_live` t2 on t1.`colorstyle` = t2.`colorstyle`
                    right outer join `www_django`.`offshore_status` t3 on t2.`colorstyle` = t3.`colorstyle`
                    where t1.photo_date BETWEEN SYSDATE( ) - INTERVAL 10 DAY AND SYSDATE( ) - INTERVAL 1 DAY
                    having (t2.`image_ready_dt` != '0000-00-00' or t2.`image_ready_dt` is not null)
                    and t3.`available_ct` > 0)
                     
                AS data
                join `data_imagepaths`.`post_ready_original` t3 on data.`colorstyle` = t3.`colorstyle`
                where data.`image_ready_dt` != t3.`photo_date`
                and data.`alt` = t3.`alt`"""
    #
    result = connection.execute(query)
    results = []
    for r in result:
        results.append(r['colorstyle'])
    return list(sorted(results))

import sys
def url_get_links(targeturl):
    import re,sys,requests
    from bs4 import BeautifulSoup
    try:
        r = requests.get(targeturl, timeout=(2.2))
        #print r
        soup = BeautifulSoup(r.text,"html.parser")
        ###  soup is now Full HTML of target -- Below creates/returns list of unique links
        linklist = []
        for link in soup.find_all('img'):
            #print link
            linklist.append(link.get('src'))
            sorted(linklist)
        ## Return list of unique links
        return list(set(linklist))
    except requests.exceptions.Timeout:
        print "Connect Timed Out ",  targeturl
    except requests.exceptions.MissingSchema:
        print "MissingSchema Error ",  targeturl

def download_swatch_urls(styles_list):
    import sys, requests, re
    regex_swatch    = re.compile(r'^http.*mgen/Bluefly/swatch.ms\?productCode=([0-9]{9})&width=49&height=59&orig(X=\d{1,4})&orig(Y=\d{1,4})$')
    pdpg            =   re.compile(r'^http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms\?img=(\d{9})\.jpg&w=75&h=89&(ver=\d{1,6})$')
    regex_pdplg     = re.compile(r'^http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms\?img=(\d{9})\.pct&outputx=583&outputy=700&level=1&(ver=\d{1,6})$')
    found_links = []
    for colorstyle in styles_list:
        pdp_url="http://www.bluefly.com/insert-favorite-phrase/p/{0}/detail.fly".format(colorstyle)
        found_links.append(url_get_links(pdp_url))
    filesizes = []
    colorstyle = ''
    print len(found_links[0])
    for stylelinks in found_links:
        for url in stylelinks:
            
            matcheslg = regex_pdplg.match(url)
            if matcheslg:
                colorstyle,version = matcheslg.groups()[:2]
                #netsrv101_url = 'ftp://imagedrop:imagedrop0@netsrv101.l3.bluefly.com//mnt/images/images/'
                #ext_JPG       = '_l.jpg'
                #netsrv101_url_file = os.path.join(netsrv101_url, colorstyle[:4], colorstyle + ext_JPG)
                #print colorstyle,version
                pdpimgurl = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}.jpg&w=75&h=89&{1}'.format(colorstyle,version)
                pdplgurl  = "http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=583&outputy=700&level=1&ver={1}".format(colorstyle,version)
                res   = requests.get(pdpimgurl, stream=False, timeout=(9.05))
                reslg = requests.get(pdplgurl, stream=False, timeout=(9.05))

                try:
                    if res.status_code < 400:
                        urlsize = (pdplgurl, reslg.size,)
                        print res.size, urlsize
                        filesizes.append(urlsize)
                    else:
                        print "Status Failed with ",  res.status_code, url
                except requests.exceptions.Timeout:
                    print "Connect Timed Out ",  targeturl
                except requests.exceptions.Timeout:
                    print "Read Timed Out ",  targeturl
                except requests.exceptions.Timeout:
                    print "Read Timed Out",  targeturl
            else:
                print 'Nuthin', url
    return filesizes


def url_get_links(targeturl):
    import os,re,sys,requests
    from bs4 import BeautifulSoup
    r = requests.get(targeturl)
    soup = BeautifulSoup(r.text,"html.parser")
    ###  soup is now Full HTML of target -- Below creates/returns list of unique links
    linklist = []
    for link in soup.find_all('img'):
        linklist.append(link.get('src'))
        sorted(linklist)
    ## Return list of unique links
    return list(set(linklist))


def rmain(bfly_url=None):
    styles = []
    import sys, os
    if not bfly_url:
        try:
            bfly_url = sys.argv[1]
        except:
            print 'Please enter a url to scrape'
    #print 'Scraping --> {}'.format(bfly_url)
    found_links = url_get_links(bfly_url)
    for f in found_links:
        try:

            style=f.split('?productCode=')[-1][:9]
            if style.isdigit():
                print style
                styles.append(style)
        except AttributeError:
            pass
    return styles

# if __name__ == '__main__':
#     import sys, os, datetime
#     #root_dir = os.path.expanduser('~') + '/Pictures'
#     root_dir = os.path.abspath('/mnt/Post_Ready/Retouchers/JohnBragato/swatchAndPDP')
#     ################################################################
#     ## ~Pictures for testing only will use sysargv 1 for root_dir ##
#     ################################################################
#     os.chdir(root_dir)
#     todaysdate = str(datetime.date.today())
#     todaysdir = "{0}{1}{2}_swatchPDP".format(todaysdate[5:7],todaysdate[8:10],todaysdate[2:4])
#     if os.path.isdir(todaysdir):
#         os.chdir(todaysdir)
#     else:
#         os.makedirs(todaysdir)
#         os.chdir(todaysdir)
#     styles_list = styles_list() #sys.argv[1:]
#     filesizes = download_swatch_urls(styles_list)
#     print filesizes, len(filesizes) #swatches_found, len(swatches_found)


def download_swatch_urls(styles_list):
    import sys, requests, re
    regex_swatch    = re.compile(r'^http.*mgen/Bluefly/swatch.ms\?productCode=([0-9]{9})&width=49&height=59&orig(X=\d{1,4})&orig(Y=\d{1,4})$')
    pdpg            =   re.compile(r'^http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms\?img=(\d{9})\.jpg&w=75&h=89&(ver=\d{1,6})$')
    regex_pdplg     = re.compile(r'^http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms\?img=(\d{9})\.pct&outputx=583&outputy=700&level=1&(ver=\d{1,6})$')
    found_links = []
    for colorstyle in styles_list:
        pdp_url="http://www.bluefly.com/insert-favorite-phrase/p/{0}/detail.fly".format(colorstyle)
        found_links.append(url_get_links(pdp_url))
    filesizes = []
    colorstyle = ''
    print len(found_links[0])
    for stylelinks in found_links:
        for url in stylelinks:
            
            matcheslg = regex_pdplg.match(url)
            if matcheslg:
                colorstyle,version = matcheslg.groups()[:2]
                #netsrv101_url = 'ftp://imagedrop:imagedrop0@netsrv101.l3.bluefly.com//mnt/images/images/'
                #ext_JPG       = '_l.jpg'
                #netsrv101_url_file = os.path.join(netsrv101_url, colorstyle[:4], colorstyle + ext_JPG)
                #print colorstyle,version
                pdpimgurl = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}.jpg&w=75&h=89&{1}'.format(colorstyle,version)
                pdplgurl  = "http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=583&outputy=700&level=1&ver={1}".format(colorstyle,version)
                res   = requests.get(pdpimgurl, stream=False, timeout=(9.05))
                reslg = requests.get(pdplgurl, stream=False, timeout=(9.05))

                try:
                    if res.status_code < 400:
                        urlsize = (pdplgurl, reslg.size,)
                        print res.size, urlsize
                        filesizes.append(urlsize)
                    else:
                        print "Status Failed with ",  res.status_code, url
                except requests.exceptions.Timeout:
                    print "Connect Timed Out ",  targeturl
                except requests.exceptions.Timeout:
                    print "Read Timed Out ",  targeturl
                except requests.exceptions.Timeout:
                    print "Read Timed Out",  targeturl
            else:
                print 'Nuthin', url
    return filesizes


def multidownloader(arglist=None):
    import Queue
    import threading
    import multiprocessing
    import subprocess, datetime, download_server_imgs_styleslist
    import os
    os.chdir('/usr/local/batchRunScripts/python')
    root_dir = os.path.abspath('/mnt/Post_Ready/Retouchers/JohnBragato/swatchAndPDP')    
    todaysdate = str(datetime.date.today())
    todaysdir = "{0}{1}{2}_swatchPDP".format(todaysdate[5:7],todaysdate[8:10],todaysdate[2:4])
    todaysdir = os.path.join(root_dir, todaysdir)
    if os.path.isdir(todaysdir):
        os.chdir(todaysdir)
    else:
        os.makedirs(todaysdir)
        os.chdir(todaysdir)
    
    q = Queue.Queue()
    print len(arglist), " len list"
    for i in arglist: #put 30 tasks in the queue
#             lls = url_get_links(i)
#             for linx in lls:
#                 print linx
#                 ll= rmain(bfly_url=linx)
        q.put(i)
        print i, " putted"

    
    def worker():
        import get_live_swatches, datetime, download_server_imgs_styleslist
        count = len(arglist)
        while True:
            item = q.get()
            print item, count
            #execute a task: call a shell program and wait until it completes
            subprocess.call("/usr/local/batchRunScripts/python/get_live_swatches.py "+str(item), shell=True)
            #download_swatch_urls(item)
            count -= 1
            print "LiveSwatch Remaining ", count
            q.task_done()
    
    cpus=multiprocessing.cpu_count() #detect number of cores
    qsized = q.qsize()
    print qsized, " Queue size"
    print("Creating %d threads" % cpus)
    for i in xrange(cpus):
        t = threading.Thread(target=worker)
        t.daemon = True        
        print 'Starting Thread Name ', t.name
        t.start()
    q.join() #block until all tasks are done
    print 'Threads Complete'


if __name__ == '__main__':
    import sys
    try:
        arglist = sys.argv[1:]
    except KeyError:
        arglist = styles_list() #designers_list()[46:48]
    multidownloader(arglist=arglist)
