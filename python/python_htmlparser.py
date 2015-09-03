#!/usr/bin/env python

import sys,os,re
import urllib2
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import NavigableString

urltarget = sys.argv[1]

def printText(tags):
    for tag in tags:
        if tag.__class__ == NavigableString:
            print tag
        else:
            printText(tag)
        print ""

# def print_html_tags(tags):
#     for tag in tags:
#         if tag.__class__ == NavigableString:
#             print tag
#         else:
#             printText(tag)
# urltarget = sys.argv[1]

html = urllib2.urlopen(urltarget).read()
soup = BeautifulSoup(html)

printText(soup.findAll("p"))
print "".join(soup.findAll("p", text=re.compile(".")))

