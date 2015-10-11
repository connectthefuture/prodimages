#!/usr/bin/env python
import os, sys, re, csv

def allocate_curl_multi_objects(arg1=None, numcnx=None):
    import sys, pycurl
    arg1 = sys.argv[1]
    
    try:
        numcnx = sys.argv[2]
    except:
        pass
    ########
    try:
        import signal
        from signal import SIGPIPE, SIG_IGN
        signal.signal(signal.SIGPIPE, signal.SIG_IGN)
    except ImportError:
        pass

    ###### Get args
    num_conn = 10
    try:
        if arg1 == "-":
            urls = sys.stdin.readlines()
        else:
            urls = open(arg1).readlines()
        if len(sys.argv) >= 3:
            num_conn = int(numcnx)
    except:
        print("Usage: %s <file with URLs to fetch> [<# of concurrent connections>]" % sys.argv[0])
        raise SystemExit

    ###### Make a queue with (url, filename) tuples
    queue = []
    for url in urls:
        url = url.strip()
        if not url or url[0] == "#":
            continue
        filename = "doc_%03d.dat" % (len(queue) + 1)
        queue.append((url, filename))

    ###### Check args
    assert queue, "no URLs given"
    num_urls = len(queue)
    num_conn = min(num_conn, num_urls)
    assert 1 <= num_conn <= 10000, "invalid number of concurrent connections"
    print("PycURL %s (compiled against 0x%x)" % (pycurl.version, pycurl.COMPILE_LIBCURL_VERSION_NUM))
    print("----- Getting", num_urls, "URLs using", num_conn, "connections -----")

    ###### Pre-allocate a list of curl objects
    m = pycurl.CurlMulti()
    m.handles = []
    for i in range(num_conn):
        c = pycurl.Curl()
        c.fp = None
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)
        c.setopt(pycurl.CONNECTTIMEOUT, 30)
        c.setopt(pycurl.TIMEOUT, 300)
        c.setopt(pycurl.NOSIGNAL, 1)
        m.handles.append(c)
        
    return m


class Test:
    def __init__(self):
        self.contents = ''

    def body_callback(self, buf):
        self.contents = self.contents + buf


def pycurl_download_netsrv101(colorstyle, alt=None, saveDir=None):
    import pycurl, os
    #import FileReader
    if alt:
        colorstyle = "{0}_{1}".format(colorstyle, alt)

    if not saveDir:
        saveDir = os.path.abspath(os.path.join(os.path.expanduser('~'), 'Share'))
    if os.path.isdir(saveDir):
        pass #saveDir = os.path.abspath(os.path.abspath(os.path.expanduser('~'), 'Share'))
    else:
        saveDir = os.path.abspath(os.path.expanduser('~'))
    
    localFileName = "{0}.png".format(colorstyle)
    localFilePath = os.path.join(saveDir, localFileName)
    
    mediaType = "8"
    ftpURL = r'ftp://netsrv101.l3.bluefly.com//mnt/images/images/'
    
    ftpFilePath = os.path.join(ftpURL, colorstyle[:4], localFileName)
    ftpUSERPWD = "imagedrop:imagedrop0"

    if localFilePath != "" and ftpFilePath != "":
        ## Create send data

        ### Send the request to Edgecast
        c = pycurl.Curl()
        c.f = open(localFilePath, 'wb')
        c.setopt(pycurl.URL, ftpFilePath)
        c.setopt(pycurl.USERPWD, ftpUSERPWD)
        c.setopt(pycurl.WRITEDATA, c.f)
        #m.add_handle(c)
        # store some info
        c.filename = localFilePath
        c.url = ftpFilePath

#        c.setopt(pycurl.PORT , 21)

        c.setopt(pycurl.VERBOSE, 1)
        c.setopt(c.CONNECTTIMEOUT, 5)
        c.setopt(c.TIMEOUT, 8)
        c.setopt(c.FAILONERROR, True)
#        c.setopt(pycurl.FORBID_REUSE, 1)
#        c.setopt(pycurl.FRESH_CONNECT, 1)
        
        #c.setopt(pycurl.INFILE, f)
        #c.setopt(pycurl.INFILESIZE, os.path.getsize(localFilePath))
        #c.setopt(pycurl.INFILESIZE_LARGE, os.path.getsize(localFilePath))
#        c.setopt(pycurl.READFUNCTION, f.read());        
#        c.setopt(pycurl.READDATA, f.read()); 
        #c.setopt(pycurl.UPLOAD, 1L)

        try:
            c.perform()
            c.close()
            print "Successfully Uploaded --> {0}".format(localFileName)
            ## return 200
        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr
            try:
                c.close()
            except:
                print "Couldnt Close Cnx"
                pass
            return errno
            
            
            
            
# Main loop
freelist = allocate_curl_multi_objects(arg1=None, numcnx=None)
num_processed = 0
while num_processed < num_urls:
    # If there is an url to process and a free curl object, add to multi stack
    while queue and freelist:
        url, filename = queue.pop(0)
        c = freelist.pop()
        c.fp = open(filename, "wb")
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.WRITEDATA, c.fp)
        m.add_handle(c)
        # store some info
        c.filename = filename
        c.url = url
    # Run the internal curl state machine for the multi stack
    while 1:
        ret, num_handles = m.perform()
        if ret != pycurl.E_CALL_MULTI_PERFORM:
            break
    # Check for curl objects which have terminated, and add them to the freelist
    while 1:
        num_q, ok_list, err_list = m.info_read()
        for c in ok_list:
            c.fp.close()
            c.fp = None
            m.remove_handle(c)
            print("Success:", c.filename, c.url, c.getinfo(pycurl.EFFECTIVE_URL))
            freelist.append(c)
        for c, errno, errmsg in err_list:
            c.fp.close()
            c.fp = None
            m.remove_handle(c)
            print("Failed: ", c.filename, c.url, errno, errmsg)
            freelist.append(c)
        num_processed = num_processed + len(ok_list) + len(err_list)
        if num_q == 0:
            break
    # Currently no more I/O is pending, could do something in the meantime
    # (display a progress bar, etc.).
    # We just call select() to sleep until some more data is available.
    m.select(1.0)


# Cleanup
for c in m.handles:
    if c.fp is not None:
        c.fp.close()
        c.fp = None
    c.close()
m.close()
