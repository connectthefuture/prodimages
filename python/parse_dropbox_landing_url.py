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



def download_file(url, destdir=None):
    import os, sys, requests
    if not destdir:
        destir = os.path.abspath('.')
    destpath = os.path.join(destdir, url.split('/')[-1])
    if request_status_code(url) != 404:
        res = requests.get(url, stream=True, timeout=10)
        with open(destpath, 'ab+') as f:
            f.write(res.content)
            f.close()
        return destpath


def parse_dropbox_landing_page(url):
    import re, requests
    regex_dbx = re.compile(r'"(https://.+?[?]dl=1)"')
    if regex_dbx.findall(url): 
        r = requests.get(url).text.splitlines()
    else:
        r = url
    filesmash = [x for x in r if regex_dbx.findall(x)][1]
    all = [ line for line in filesmash.splitlines() if regex_dbx.findall(line) ][0].split(',')
    files = [ a for a in all if regex_dbx.findall(a) ]
    urls = []
    for f in files:
        u = f.splitlines()[0]
        if regex_dbx.findall(u):
            urls.append(u.split()[-1].strip('"'))
    return urls

if __name__ == '__main__':
    url='https://www.dropbox.com/sh/vw8t77pwdvbxo45/AACJrvjYaJuu26aO5T3lZ04Fa?dl=0'
    res = parse_dropbox_landing_page(url)
    destdir='/Users/johnb/Pictures'    
    for url in res:
        download_file(url, destdir=destdir)
    #print res