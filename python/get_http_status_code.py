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
#
#import requests
#try:
#    r = requests.head("http://stackoverflow.com")
#    print r.status_code
#    #prints the int of the status code. Find more at httpstatusrappers.com :)
#except requests.ConnectionError:
#    print "failed to connect"
#    
#    

import httplib
def get_status_code(host=None, path="/"):
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        return conn.getresponse().status
    except StandardError:
        return None
        

def main(url_path=None):
    host = url_path.split('.com/')[0] + '.com'
    path = url_path.split('.com/')[-1] + '/'
    status_code = get_status_code(host=host, path=path)
    return status_code


if __name__ == '__main__':
    import sys
    try:
        host = sys.argv[1].split('.com/')[0] + '.com'
        path = sys.argv[1].split('.com/')[-1] + '/'
        status_code = get_status_code(host=host, path=path)
    except:
        print 'Error occurred. Unable to get Http Code'