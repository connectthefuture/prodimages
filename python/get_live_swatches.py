#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        print "Missing Schema Timed Out ",  targeturl
    # except requests.exceptions.ReadTimeout:
    #     print "Read Timed Out",  targeturl


def return_versioned_urls(text):
    import sys,re
    regex = re.compile(r'http:.+?ver=[1-9][0-9]?[0-9]?')
    regex_swatch = re.compile(r'^http.*mgen/Bluefly/swatch.ms\?productCode=[0-9]{9}&width=49&height=59.*$')
    listurls = []
    for line in text:
        testfind =  regex.findall(line)
        testswatch = regex_swatch.findall(line)
        if testfind:
            listurls.append(testfind)
            ##print testfind
        if testswatch:
            listurls.append(testswatch)
    return listurls


def getbinary_ftp_netsrv101(remote_pathtofile, outfile=None):
    # fetch a binary file
    import ftplib
    session = ftplib.FTP("netsrv101.l3.bluefly.com", "imagedrop", "imagedrop0")
    if outfile is None:
        outfile = sys.stdout
    destfile = open(outfile, "wb")
    print remote_pathtofile
    session.retrbinary("RETR " + remote_pathtofile, destfile.write, 8*1024)
    destfile.close()
    session.quit()


def return_cleaned_bfly_urls(text):
    import sys,re
    import re
    regex_url  = re.compile(r'^(?:.+?\.ms\?\w+=)(?P<colorstyle>[1-9][0-9]{8})(?:.*?)?&(?:.*?)?(?:(?:w=)|(?:width=)|(?:outputx=))?(?P<width>\d+)?(?:(?:&h=)|(?:&height=)|(?:&outputy=))?(?P<height>\d+)?(?:.*?)?((?:&ver=)(?P<version>\d+))?(?:&level=\d)?$', re.U)
    regex = re.compile(r'http:.+?mgen/Bluefly/.+?')
    listurls = []
    for line in text:
        testfind =  regex.findall(line)
        if testfind:
            listurls.append(testfind)
    return listurls


def download_swatch_urls(styles_list):
    import sys, requests, re
    import os
    regex_swatch    = re.compile(r'^http.*mgen/Bluefly/swatch.ms\?productCode=([0-9]{9})&width=49&height=59&orig(X=\d{1,4})&orig(Y=\d{1,4})$')
    pdpg            =   re.compile(r'^http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms\?img=(\d{9})\.jpg&w=75&h=89&(ver=\d{1,6})$')
    regex_pdplg     = re.compile(r'^http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms\?img=(\d{9})\.pct&outputx=583&outputy=700&level=1&(ver=\d{1,6})$')
    found_links = []
    for colorstyle in styles_list:
        pdp_url="http://www.bluefly.com/insert-favorite-phrase/p/{0}/detail.fly".format(colorstyle)
        found_links.append(url_get_links(pdp_url))
    swatch_links = []
    colorstyle = ''
    print len(found_links[0])
    for stylelinks in found_links:
        for url in stylelinks:
            print url
            matches   = regex_swatch.match(url)
            matcheslg = regex_pdplg.match(url)
            if matches:
                colorstyle,xRun,yRise = matches.groups()[:3]
                #print colorstyle, xRun,yRise
                res = requests.get(url, timeout=(2.05))
                with open(colorstyle + "_" + xRun + yRise + '_swatch.jpg','wb') as f:
                    f.write(res.content)
                swatch_links.append(url)

            if matcheslg:
                colorstyle,version = matcheslg.groups()[:2]
                netsrv101_url = 'ftp://imagedrop:imagedrop0@netsrv101.l3.bluefly.com//mnt/images/images/'
                ext_JPG       = '_l.jpg'
                netsrv101_url_file = "{}{}{}".format(netsrv101_url, colorstyle[:4], colorstyle + ext_JPG)
                #print colorstyle,version
                pdpimgurl = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}.jpg&w=75&h=89&{1}'.format(colorstyle,version)
                pdplgurl  = "http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=583&outputy=700&level=1&ver={1}".format(colorstyle,version)
                res   = requests.get(pdpimgurl, stream=False, timeout=(9.05))
                reslg = requests.get(pdplgurl, stream=False, timeout=(9.05))

                try:
                    if res.status_code < 400:
                        with open(colorstyle + '_Pdp_Cdn_lg_' + str(version) + '.jpg','wb') as f:
                            f.write(reslg.content)

                        with open(colorstyle + '_PDPCached_'  + str(version) + '.jpg','wb') as f:
                            f.write(res.content)

                        try:
                            import subprocess
                            #res_l = requests.get(netsrv101_url_file, stream=False, timeout=(4.05))
                            fname = colorstyle + '_PDPSource_l_' + '.jpg'
                            getbinary_ftp_netsrv101(netsrv101_url_file, outfile=fname)
                        except:
                            pass
                    else:
                        print "Status Failed with ",  res.status_code, url
                except requests.exceptions.ConnectTimeout:
                    print "Connect Timed Out ",  targeturl
                except requests.exceptions.ReadTimeout:
                    print "Read Timed Out ",  targeturl
                except requests.exceptions.ReadTimeout:
                    print "Read Timed Out",  targeturl
            else:
                print 'Nuthin', url
    return swatch_links


#def main(styles_list=None):



if __name__ == '__main__':
    import sys, os, datetime
    #root_dir = os.path.expanduser('~') + '/Pictures'
    root_dir = os.path.abspath('/mnt/Post_Ready/Retouchers/JohnBragato/swatchAndPDP')
    ################################################################
    ## ~Pictures for testing only will use sysargv 1 for root_dir ##
    ################################################################
    if os.path.isdir(root_dir):
        os.chdir(root_dir)
    elif os.path.isdir('/Users/johnb/Pictures'):
        root_dir = os.path.isdir(root_dir)
        os.chdir(root_dir)

    todaysdate = str(datetime.date.today())
    todaysdir = "{0}{1}{2}_swatchPDP".format(todaysdate[5:7],todaysdate[8:10],todaysdate[2:4])
    if os.path.isdir(todaysdir):
        os.chdir(todaysdir)
    else:
        os.makedirs(todaysdir)
        os.chdir(todaysdir)
    styles_list = sys.argv[1:]
    swatches_found = download_swatch_urls(styles_list)
    #print swatches_found, len(swatches_found)
