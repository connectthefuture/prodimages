#!/usr/bin/env python
import os, sys, re, csv



def upload_to_indiaDrop(filepath):
    import ftplib
    session = ftplib.FTP('prepressoutsourcing.com', 'bf', 'B1002#@F')
    fileread = open(filepath, 'rb')
    filename = str(filepath.split('/')[-1])
    session.cwd("Drop/")
    session.storbinary('STOR ' + filename, fileread, 8*1024)
    fileread.close()
    session.quit() 
    
    

def pycurl_upload_indiadrop(localFilePath):
    import pycurl, os
    #import FileReader
    localFileName = localFilePath.split('/')[-1]

    mediaType = "8"
    
    ftpURL = r'ftp://prepressoutsourcing.com//Pick/'
    ftpUSERPWD = "bf:B1002#@F"

    ftpFilePath = os.path.join(ftpURL, localFileName)
    if localFilePath != "" and ftpFilePath != "":
        ## Create send data

        ### Send the request to Edgecast
        c = pycurl.Curl()
        c.setopt(pycurl.URL, ftpFilePath)
#        c.setopt(pycurl.PORT , 21)
        c.setopt(pycurl.USERPWD, ftpUSERPWD)
        #c.setopt(pycurl.VERBOSE, 1)
        c.setopt(c.CONNECTTIMEOUT, 5)
        c.setopt(c.TIMEOUT, 8)
        c.setopt(c.FAILONERROR, True)
#        c.setopt(pycurl.FORBID_REUSE, 1)
#        c.setopt(pycurl.FRESH_CONNECT, 1)
        f = open(localFilePath, 'rb')
        c.setopt(pycurl.INFILE, f)
        c.setopt(pycurl.INFILESIZE, os.path.getsize(localFilePath))
        c.setopt(pycurl.INFILESIZE_LARGE, os.path.getsize(localFilePath))
#        c.setopt(pycurl.READFUNCTION, f.read());        
#        c.setopt(pycurl.READDATA, f.read()); 
        c.setopt(pycurl.UPLOAD, 1L)

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


    
def pycurl_download_indiaComplete(zipfilename, saveDir=None):
    import pycurl, os
    #import FileReader
    if not saveDir:
        saveDir = os.path.abspath('/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/2_Returned')
    
    localFileName = "{0}".format(zipfilename)
    localFilePath = os.path.join(saveDir, localFileName)
    
    mediaType = "8"
    ftpURL = r'ftp://prepressoutsourcing.com//Pick/'
    
    ftpFilePath = os.path.join(ftpURL, colorstyle[:4], localFileName)
    ftpUSERPWD = "bf:B1002#@F"

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