#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


def main(bfly_url=None):
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


if __name__ == '__main__':
    main()