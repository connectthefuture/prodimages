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


def parse_pdp_html_get_mozuid_cdnkey(pdpurl):
    from bs4 import BeautifulSoup
    import urllib2
    import json
    if len(pdpurl) == 9 and pdpurl.isdigit():
        pdpurl = 'http://beta.bluefly.com/cache-clear/p/' + pdpurl
    else:
        pass
    page = urllib2.urlopen(pdpurl)
    soup = BeautifulSoup(page.read(), "lxml")
    sources=soup.findAll('script', {"id":"data-mz-preload-pagecontext"} )
    res = []
    for source in sources:
        res.append(source)
    try:
        context_data = json.loads(res[0].text)
        outdict = {}
        mz_image_data = {}
        print context_data
        mz_image_data['mz_imageid']      = context_data['cmsContext']['site']['id']
        mz_image_data['bf_imageid']      = context_data['productCode']
        mz_image_data['cdnCacheBustKey'] = context_data['cdnCacheBustKey']
        outdict[context_data['productCode']] = mz_image_data
        return outdict
    except IndexError:
        print 'IndexError: Key not found in json results at\n\turl {}'.format(pdpurl)


def parse_pdp_html_get_mozu_data_tags(pdpurl):
    from bs4 import BeautifulSoup
    import urllib2
    import json
    if len(pdpurl) == 9 and pdpurl.isdigit():
        pdpurl = 'http://beta.bluefly.com/cache-clear/p/' + pdpurl
    else:
        pass
    page = urllib2.urlopen(pdpurl)
    soup = BeautifulSoup(page.read(), "lxml")
    sources=soup.findAll('img', {"itemprop": "image"})
    res = []
    print sources #.children()
    for source in sources:
        res.append(source['data-mz-productimage-main'])
    return res


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


def main(bfly_url=None,check_status=None):
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
        try:
            parsedurl =  urlparse.urlparse(f)
            host    = parsedurl.netloc
            qstring = parsedurl.query
            path    = parsedurl.path
            bfstyle = path.split('/')[-1]
            if len(bfstyle) == 9 and bfstyle.isdigit():
                if f[:2] == '//':
                    url = 'https:' + f
            elif bfstyle[-3:] == '.ms':
                url = f
                bfstyle = f.split('?productCode=')[-1][:9]
                if not bfstyle:
                    bfstyle = f.split('?img=')[-1][:9]
            if bfstyle.isdigit():
                print bfstyle
                if check_status:
                    status_code = url_tester(url)
                    res_tuple = (bfstyle, status_code,)
                    styles.append(res_tuple)
                    print res_tuple
                else:
                    styles.append(bfstyle)
        except AttributeError:
            print 'AttributeError, url:{}'.format(f)
            pass
    return styles


if __name__ == '__main__':
    main()
