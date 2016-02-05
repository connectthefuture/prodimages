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


def url_tester(url):
    import requests
    res = requests.get(url)
    #res = requests.request('HEADERS', url)
    http_code = res.status_code
    return http_code


def url_tester_headers(url):
    import requests
    #res = requests.get(url)
    res = requests.request('HEADERS', url)
    headers = res.headers
    return headers


def main(bfly_url=None,check_status=True):
    import sys, urlparse
    styles = []
    if not bfly_url:
        try:
            bfly_url = sys.argv[1]
            try:
                check_status = sys.argv[2]
            except IndexError:
                pass
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
                if check_status:
                    status_code = url_tester('http:'+f)
                    res_tuple = (bfstyle, status_code,)
                    styles.append(res_tuple)
                    print res_tuple
                else:
                    styles.append(bfstyle)
        except AttributeError:
            print 'AttributeError'
            pass
    return styles


if __name__ == '__main__':
    main()
