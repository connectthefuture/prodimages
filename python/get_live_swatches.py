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
        print link
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
    import sys, requests, re
    regex_swatch = re.compile(r'^http.*mgen/Bluefly/swatch.ms\?productCode=([0-9]{9})&width=49&height=59&orig(X=\d{1,4})&orig(Y=\d{1,4})$')
    pdpg          =   re.compile(r'^http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img=(\d{9})\.jpg&w=75&h=89&(ver=\d{1,6})$')
    
    found_links = []
    for colorstyle in styles_list:
        pdp_url="http://www.bluefly.com/insert-favorite-phrase/p/{0}/detail.fly".format(colorstyle)
        found_links
        found_links.append(url_get_links(pdp_url))
    swatch_links = []
    colorstyle = ''
    for url in found_links[0]:
        print url
        matches = regex_swatch.match(url)
        if matches:
            try:
                colorstyle,xRun,yRise = matches.groups()[:3]
                print xRun,yRise
                res = requests.get(url)
                with open(colorstyle + "_" + xRun + yRise + '_swatch.jpg','wb') as f:
                    f.write(res.content)
                swatch_links.append(url)
            except AttributeError:
                print 'AtrribErr'
                pass
        elif pdpg.findall(url):
            try:
                colorstyle,version = pdpg.match.groups()[:2]
                pdpimgurl     =   'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?productCode={0}.jpg&w=75&h=89&{1}'.format(colorstyle,version)
                res = requests.get(pdpimgurl)
                with open(colorstyle + '_PDP_Cached.jpg','wb') as f:
                    f.write(res.content)
            except AttributeError:
                print 'PDPAtrribErr'
                pass

        else:
            print 'Nuthin', url
    return swatch_links


#def main(styles_list=None):
    


if __name__ == '__main__':
    import sys, os
    os.chdir(os.path.expanduser('~') + '/Share') ##'/Pictures')
    styles_list = sys.argv[1:]
    swatches_found = download_swatch_urls(styles_list)
    print swatches_found, len(swatches_found)