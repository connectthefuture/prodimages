#!/usr/bin/env python
# -*- coding: utf-8 -*-

def multidownloader(styles_list=None, root_dir=None):
    import Queue
    import threading
    import multiprocessing
    import subprocess, datetime, download_server_imgs_styleslist
    import os
    os.chdir('/usr/local/batchRunScripts/python')
    if not root_dir and os.path.isdir('/Users/johnb'):
        root_dir = '/Volumes/Post_Complete/ImageDrop'
    elif not root_dir:
        root_dir = '/mnt/Post_Complete/ImageDrop'
    root_dir = os.path.abspath(root_dir)

    q = Queue.Queue()
    print len(styles_list), " len list"
    for s in styles_list: #put 30 tasks in the queue
        q.put(s)
        print s, " putted"


    def worker():
        import get_live_swatches, datetime, download_server_imgs_styleslist
        count = len(styles_list)
        while True:
            style = q.get()
            print style, count
            #execute a task: call a shell program and wait until it completes
            subprocess.call("/usr/local/batchRunScripts/python/download_marketplace_style.py " + str(style), shell=True)
            #download_swatch_urls(style)
            count -= 1
            print "LiveSwatch Remaining ", count
            q.task_done()

    cpus=multiprocessing.cpu_count() #detect number of cores
    qsized = q.qsize()
    print qsized, " Queue size"
    print("Creating %d threads" % cpus)
    for i in xrange(cpus):
        t = threading.Thread(target=worker)
        t.daemon = True
        print 'Starting Thread Name ', t.name
        t.start()
    q.join() #block until all tasks are done
    print 'Threads Complete'


if __name__ == '__main__':
    multidownloader(styles_list=None, root_dir=None)
