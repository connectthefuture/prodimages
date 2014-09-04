#!/usr/bin/env python
# -*- coding: utf-8 -*-

def request_status_code(url):
    import requests
    try:
        r = requests.head(url)
        return r.status_code
    except requests.ConnectionError:
        print "failed to connect"


def parse_html_for_urls(url):
    import requests, re, codecs
    #  [^\\]*
    rehex = re.compile(r'^.+?[:xdigit:]*.+?$')
    renoequal = re.compile(r'^(.+)[=].*$')
    regex_hex = re.compile(r'(https://.+?\.googleusercontent\.com/[a-zA-Z0-9-_]+?)[^=]\\?(?![:xdigit:].*?)',re.U)

    raw_response = unicode((requests.get(url, stream=True, timeout=1).content), 'utf8')
    response_list = [ r.strip('"') for r in codecs.unicode_escape_decode(raw_response)[0].split(',') if r ]

    res = [ r for r in response_list if regex_hex.findall(r) ]
    ret = list(set(sorted(res)))
    if len(ret) == 1:
        return ret
    else:
        
        valid = [ r for r in ret if not renoequal.findall(r) ]
        imgurl = valid[0]
        if request_status_code(imgurl) == 200:
            return imgurl
        else:
            return '{} is not a valid URL'.format(imgurl)
            
def download_file(url, colorstyle=None, alt=None, ext='.jpg', destdir=None):
    import os, sys, requests
    if not destdir:
        destir = os.path.abspath('.')
    if not ext:
        ext = url.split('.')[-1]
    destpath = os.path.join(destdir, colorstyle + '_' + alt + ext)
    if request_status_code(url) != 404:
        res = requests.get(url, stream=True, timeout=10)
        with open(destpath, 'ab+') as f:
            f.write(res.content)
            f.close()
        return destpath            

def main(url):
    result = parse_html_for_urls(url)
    return result

#    urlok='https://drive.google.com/file/d/0B4p-sxy24gtqOGlERmRkQmpoRkU/edit?usp=sharing'
#    urlbad='https://drive.google.com/file/d/0B4p-sxy24gtqb3dLQjZzZUJqSmc/edit?usp=sharing'
#    urlbad2='https://drive.google.com/file/d/0B4p-sxy24gtqWng3LTd4RXlxSXM/edit?usp=sharing'
#    print parse_html_for_urls(urlok)
#    print parse_html_for_urls(urlbad)
#    print parse_html_for_urls(urlbad2)



if __name__ == '__main__':
    import sys
    try:
        url = sys.argv[1]
        status_code = request_status_code(url)
        print status_code
    except IndexError:
        main()
        #print 'You need to provide a URL as your first and only argument'