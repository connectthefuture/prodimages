#!/usr/bin/env python
# -*- coding: utf-8 -*-

def url_get_links(targeturl):
    import requests
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


def main(bfly_url=None,check_status=None):
    import sys, urlparse
    styles = []
    if not bfly_url:
        try:
            bfly_url = sys.argv[1]
        except:
            print 'Please enter a url to scrape'
    print 'Scraping --> {} for Bluefly Styles\n'.format(bfly_url)
    found_links = url_get_links(bfly_url)

    for f in found_links:
        parsedurl =  urlparse.urlparse(f)
        host    = parsedurl.netloc
        qstring = parsedurl.query
        path    = parsedurl.path
        bfstyle = path.split('/')[-1]
        if len(bfstyle) == 9 and bfstyle.isdigit():
            pass
        elif bfstyle[-3:] == '.ms':
            bfstyle = f.split('?productCode=')[-1][:9]
            if not bfstyle:
                bfstyle = f.split('?img=')[-1][:9]
        try:
            if bfstyle.isdigit():
                print bfstyle
                styles.append(bfstyle)
        except AttributeError:
            print 'AttributeError'
            pass
    if check_status:
        import requests
        styles = [ (s, str(requests.get(s).status_code)) for s in styles ]
    else:
        pass
    return styles


if __name__ == '__main__':
    main()
