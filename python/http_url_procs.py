#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def get_image_urls_query(query):
    result = connection.execute(query)
    styles = {}
    for row in result:
        style_info = {}
        style_info['colorstyle'] = row['bluefly_product_color']
        style_info['alt'] = row['image_number']
        style_info['url'] = row['url']
        # Convert Colorstyle to string then set as KEY
        styles[str(row['url'])] = style_info

    connection.close()
    return styles


def request_status_code(url):
    import requests
    try:
        r = requests.head(url)
        return r.status_code
        #prints the int of the status code. Find more at httpstatusrappers.com :)
    except requests.ConnectionError:
        print "failed to connect"


def parse_html_for_urls(url):
    import requests, re
    regex_hex = re.compile(r'(https://.+?\.googleusercontent\.com/\w+)(?![:xdigit:])',re.U)
    res = str(requests.get(url, stream=True, timeout=1).content)
    ret = list(set(sorted(regex_hex.findall(res))))
    if len(ret) == 1:
        return ret[0]
    

def download_file(url, colorstyle=None, alt=None, ext='.jpg', destdir=None):
    import os, sys, requests
    if not destdir:
        destir = os.path.abspath('.')
    if not ext:
        ext = url.split('.')[-1]
    destpath = os.path.join(destdir, colorstyle + '_' + alt + ext)
    res = requests.get(url, stream=True, timeout=1)
    with open(destpath, 'ab+') as f:
        f.write(res.content)
        f.close()
    return destpath


#for style in styless:
#    url = style['image_url']
#    alt = str(style['alt'])
#    colorstyle = str(style['colorstyle'])
#    res = download_file(url.strip('/edit?usp=sharing'), colorstyle=colorstyle, alt=alt, destdir=destdir)


#import httplib
#def get_status_code(host=None, path="/"):
#    try:
#        conn = httplib.HTTPConnection(host)
#        conn.request("HEAD", path)
#        return conn.getresponse().status
#    except StandardError:
#        return None
#        
#
#def main(url_path=None):
#    host = url_path.split('.com/')[0] + '.com'
#    path = url_path.split('.com/')[-1] + '/'
#    status_code = get_status_code(host=host, path=path)
#    return status_code


if __name__ == '__main__':
    import sys
    try:
        url = sys.argv[1]
        status_code = request_status_code(url)
        print status_code
    except IndexError:
        print 'You need to provide a URL as your first and only argument'
    #except:
    #    print 'Error occurred. Unable to get Http Code'