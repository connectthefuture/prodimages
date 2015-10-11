#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
def url_get_links(targeturl):
    import re,sys,requests
    from bs4 import BeautifulSoup
    try:
        r = requests.get(targeturl, timeout=(2.2))
        #print r
        soup = BeautifulSoup(r.text,"html.parser")
        ###  soup is now Full HTML of target -- Below creates/returns list of unique links
        linklist = []
        for link in soup.find_all('img'):
            #print link
            linklist.append(link.get('src'))
            sorted(linklist)
        ## Return list of unique links
        return list(set(linklist))
    except: ##requests.exceptions.Timeout:
        print "Connect Timed Out ",  targeturl
        return '1'

def get_html_attribs(html, *args):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html)
    ret = []
    for arg in args:
        if len(arg) <= 2:
            print len(args)
            #print args
        for link in soup.find_all(args[0]):
            if link['href']:
                ret.append(link['href'])
    return ret


def designers_list():
    import requests, re
    htmltext=requests.get('http://www.bluefly.com/designers.fly')
    results=get_html_attribs(htmltext.text, 'a','href')
    regex=re.compile(r'^/designer/.*?$')
    urlbase = 'bluefly.com'
    links=[]
    
    for r in results:
        if regex.match(r):
            #print results
            qstring = '?so=new&vl=l&ppp=96&cp=1'
            bflylink="http://{0}{1}{2}".format(urlbase,r,qstring)
            links.append(bflylink)
    return links


def multidownloader(arglist=None):
    import Queue
    import threading
    import multiprocessing
    import subprocess
    import get_live_swatches
    q = Queue.Queue()
    for i in arglist: #put 30 tasks in the queue
        if i:
            for l in url_get_links(i):
                q.put(l)
    
    def worker():
        count = 0
        while True:
            item = q.get()
            #execute a task: call a shell program and wait until it completes
            #subprocess.call("echo "+str(item), shell=True)
            get_live_swatches.download_swatch_urls(item)
            count += 1
            print count
            q.task_done()

    cpus=multiprocessing.cpu_count() #detect number of cores
    print("Creating %d threads" % cpus)
    for i in xrange(cpus):
         t = threading.Thread(target=worker)
         t.daemon = True
         t.start()

    q.join() #block until all tasks are done



if __name__ == '__main__':
    import sys
    arglist = designers_list()[:9]
    multidownloader(arglist=arglist)