#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Download an HTTPS file from Google Drive using 

def download_googledrive_shared_image(targeturl, destdir=None):
    import os,re,sys,requests
    from bs4 import BeautifulSoup
    if not destdir:
        destdir = os.path.abspath('.')
    #regex_sourcefile = re.compile(r'https://.*?/googleusercontent\.com.*?')
    regex_sourcefile = re.compile(r'^"(https://lh3.googleusercontent.com/.+?)\\u003.*?"$')
    
    r = requests.get(targeturl)
    #soup = BeautifulSoup(r.text,"html.parser")
    ###  soup is now Full HTML of target -- Below creates/returns list of unique links
    #souplist = soup.renderContents().split(',')
    souplist = r.content.split('","')
    imglinks = []
    
    [ imglinks.append(imgurl) for imgurl in souplist if imgurl and regex_sourcefile.findall(imgurl) ]
    #print f
    imglinks = sorted(list(set(imglinks)))
    #print imglinks #, souplist
    # download found img urls content
    link = regex_sourcefile.findall(imglinks[0])
    print link
    localpath = os.path.join(destdir, link.split('/')[-1])
    res = requests.get(link, stream=True, timeout=10)
    with open(localpath, 'ab+') as f:
        f.write(res.content)
        f.close()


def main(targeturl=None, destdir=None):
    import sys
    if not targeturl:
        try:
            targeturl = 'https://drive.google.com/open?id=0B6gg_FhatSi8cWF4RVFhMEtiRm8&authuser=0'
            #image_url = sys.argv[1]
            destdir  = '/Users/johnb/Desktop/pix/testfile.jpg' 
            #targeturl = sys.argv[1]
            #destdir   = sys.argv[2]        
        except:
            pass

    file_content = download_googledrive_shared_image(targeturl)
    return file_content

if __name__ == "__main__":
    main()