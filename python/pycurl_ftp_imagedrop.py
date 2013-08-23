#!/usr/bin/env python

def pycurl_upload_imagedrop(localFilePath):
    import pycurl, os
    #import FileReader
    localFileName = localFilePath.split('/')[-1]

    mediaType = "8"
    ftpURL = "ftp://file3.bluefly.corp/ImageDrop/"
    ftpFilePath = os.path.join(ftpURL, localFileName)
    ftpUSERPWD = "imagedrop:imagedrop0"

    if localFilePath != "" and ftpFilePath != "":
        ## Create send data

        ### Send the request to Edgecast
        c = pycurl.Curl()
        c.setopt(pycurl.URL, ftpFilePath)
        c.setopt(pycurl.PORT , 21)
        c.setopt(pycurl.USERPWD, ftpUSERPWD)
        c.setopt(pycurl.VERBOSE, 1)
        f = open(localFilePath, 'rb')
        c.setopt(pycurl.INFILE, f)
        c.setopt(pycurl.INFILESIZE, os.path.getsize(localFilePath))
        c.setopt(pycurl.UPLOAD, 1)

        try:
            c.perform()
            c.close()
            print "Successfully Sent Purge Request for --> {0}".format(localFileName)
        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr
            
            
############# RUN ####
import sys,os
    
if sys.argv[1]:
    localFilePath = sys.argv[1]
    try:
        pycurl_upload_imagedrop(localFilePath)
        print "Successfully Loaded {}".format(localFilePath.split('/'[-1]))
    except:
        print "FAILED UPLOAD {}".format(localFilePath)
        
