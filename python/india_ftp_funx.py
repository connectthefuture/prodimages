#!/usr/bin/env python
import os, sys, re, csv



def upload_to_indiaDrop(localfilepath):
    import ftplib
    session = ftplib.FTP('prepressoutsourcing.com', 'bf', 'B1002#@F')
    fileread = open(localfilepath, 'rb')
    filename = str(localfilepath.split('/')[-1])
    session.cwd("Drop/")
    session.storbinary('STOR ' + filename, fileread, 8*1024)
    fileread.close()
    session.quit() 
    
    
def listcontents_indiaDrop(remotedir):
    import ftplib
    session = ftplib.FTP('prepressoutsourcing.com', 'bf', 'B1002#@F')
    session.cwd(remotedir)
    dirlist = session.dir()
    #session.storbinary('STOR ' + filename, fileread, 8*1024)
    fileread.close()
    session.quit() 
    return dirlist


def pycurl_upload_indiadrop(localfilepath):
    import pycurl, os
    #import FileReader
    localfilename = localfilepath.split('/')[-1]

    mediaType = "8"
    
    ftpURL = r'ftp://prepressoutsourcing.com//Drop/'
    ftpUSERPWD = "bf:B1002#@F"

    ftpfilepath = os.path.join(ftpURL, localfilename)
    if localfilepath != "" and ftpfilepath != "":
        ## Create send data

        ### Send the request to Edgecast
        c = pycurl.Curl()
        c.setopt(pycurl.URL, ftpfilepath)
#        c.setopt(pycurl.PORT , 21)
        c.setopt(pycurl.USERPWD, ftpUSERPWD)
        #c.setopt(pycurl.VERBOSE, 1)
        c.setopt(c.CONNECTTIMEOUT, 5)
        c.setopt(c.TIMEOUT, 8)
        c.setopt(c.FAILONERROR, True)
#        c.setopt(pycurl.FORBID_REUSE, 1)
#        c.setopt(pycurl.FRESH_CONNECT, 1)
        f = open(localfilepath, 'rb')
        c.setopt(pycurl.INFILE, f)
        c.setopt(pycurl.INFILESIZE, os.path.getsize(localfilepath))
        c.setopt(pycurl.INFILESIZE_LARGE, os.path.getsize(localfilepath))
#        c.setopt(pycurl.READFUNCTION, f.read());        
#        c.setopt(pycurl.READDATA, f.read()); 
        c.setopt(pycurl.UPLOAD, 1L)

        try:
            c.perform()
            c.close()
            print "Successfully Uploaded --> {0}".format(localfilename)
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



def pycurl_download_indiaComplete(zipfilename, savedir=None):
    import pycurl, os
    #import FileReader
    if not savedir:
        savedir = os.path.abspath('/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/2_Returned')
    
    localfilename = "{0}".format(zipfilename)
    localfilepath = os.path.join(savedir, localfilename)
    
    mediaType = "8"
    ftpURL = 'prepressoutsourcing.com/Pick/'
    
    ftpfilepath = os.path.join(ftpURL, localfilename)
    ftpUSERPWD = "bf:B1002#@F"

    if localfilepath != "" and ftpfilepath != "":
        ## Create send data

        ### Send the request to Edgecast
        c = pycurl.Curl()
        c.f = open(localfilepath, 'wb')
        c.setopt(pycurl.URL, ftpfilepath)
        c.setopt(pycurl.USERPWD, ftpUSERPWD)
        c.setopt(pycurl.WRITEDATA, c.f)
        #m.add_handle(c)
        # store some info
        c.filename = localfilepath
        c.url = ftpfilepath

#        c.setopt(pycurl.PORT , 21)

        c.setopt(pycurl.VERBOSE, 1)
        c.setopt(c.CONNECTTIMEOUT, 5)
        c.setopt(c.TIMEOUT, 8)
        c.setopt(c.FAILONERROR, True)
#        c.setopt(pycurl.FORBID_REUSE, 1)
#        c.setopt(pycurl.FRESH_CONNECT, 1)
        
        #c.setopt(pycurl.INFILE, f)
        #c.setopt(pycurl.INFILESIZE, os.path.getsize(localfilepath))
        #c.setopt(pycurl.INFILESIZE_LARGE, os.path.getsize(localfilepath))
#        c.setopt(pycurl.READFUNCTION, f.read());        
#        c.setopt(pycurl.READDATA, f.read()); 
        #c.setopt(pycurl.UPLOAD, 1L)

        try:
            c.perform()
            c.close()
            print "Successfully Uploaded --> {0}".format(localfilename)
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