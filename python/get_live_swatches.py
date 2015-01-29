#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
def url_get_links(targeturl):
    import re,sys,requests
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
            #print testfind
        if testswatch:
            listurls.append(testswatch)
    return listurls
    

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
    import sys
    links = []
    for colorstyle in styles_list:
        swatch_url="http://cdn.is.bluefly.com/mgen/Bluefly/swatch.ms?productCode={0}&width=49&height=59&origX={1}&origY={2}".format(colorstyle,xRun,yRise)    
        pdp_url="http://www.bluefly.com/insert-favorite-phrase/p/{0}/detail.fly".format(colorstyle)
        found_links = url_get_links(pdp_url)
        links.append(found_links)
    swatch_links = []
    for url in found_links:
        try:
            res = requests.get(url)
            with open(colorstyle + '_swatch.jpg','wb') as f:
                f.write(res.content)
            swatch_links.append(colorstyle)
        except AttributeError:
            print 'AtrribErr'
            pass
    return swatch_links


#def main(styles_list=None):
    


if __name__ == '__main__':
    import sys, os
    os.chdir('~/Pictures')
    styles_list = sys.argv[1:]
    download_swatch_urls(styles_list)

