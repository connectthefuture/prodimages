#!/usr/bin/env python
import sys,re,os


htmlfile = sys.argv[1]

def bandc_return_versioned_url_listpage(htmlfile):
    regex = re.compile(r'http:.+ver=[1-9][0-9]?[0-9]?')
    listurls = []
    with open(htmlfile, 'rb') as f:
        for line in f:
            testfind =  regex.findall(line)
            if testfind:
                listurls.append(testfind)
            else:
                pass
    return listurls                



urls = bandc_return_versioned_url_listpage(htmlfile)


print len(urls)      