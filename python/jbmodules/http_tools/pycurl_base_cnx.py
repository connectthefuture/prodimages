#!/usr/bin/env python
# -*- coding: utf-8 -*-

def pycurl_upload_imagedrop(localFilePath=None, 
                            url=None, 
                            port=None, 
                            auth=None, 
                            apiroot=None, 
                            redirect=False,
                            getdata=False,
                            senddata=False,
                            redirect=None):
    import pycurl, os

    mediaType = "8"
    if not url:
        url = "ftp://file3.bluefly.corp/ImageDrop/"
        auth = "imagedrop:imagedrop0"
        port = 21
    if not localFilePath:
        if not apiroot:
            apiroot     = 'looklet-shot-list'
        remoteFilePath  = os.path.join(url, apiroot)
    else:
        localFileName   = localFilePath.split('/')[-1]
        remoteFilePath  = os.path.join(url, localFileName)
        getdata = True

    ## Instantiate cURL connection obj   
    c = pycurl.Curl()

    if localFilePath    != "" and remoteFilePath != "":
        #########################
        ## Create and send data/binary file
        #########################
        ### Send the request and Set Primary cURL Options

        c.setopt(pycurl.URL, remoteFilePath)        
        c.setopt(pycurl.PORT , port)
        c.setopt(pycurl.USERPWD, auth)
        #c.setopt(pycurl.VERBOSE, 1)

        #########################        
        ### Connection Handling Options
        if redirect:
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(pycurl.MAXREDIRS, 5)
            c.setopt(pycurl.CONNECTTIMEOUT, 30)
            c.setopt(pycurl.TIMEOUT, 300)
            c.setopt(pycurl.NOSIGNAL, 1)
        else:
            c.setopt(pycurl.CONNECTTIMEOUT, 5)
            c.setopt(pycurl.TIMEOUT, 8)
        
        c.setopt(c.FAILONERROR, True)
        #c.setopt(pycurl.FORBID_REUSE, 1)
        #c.setopt(pycurl.FRESH_CONNECT, 1)
        
        #########################
        ### File Handling Options
        #########################
        ###
        ### Download Read/Write File/Data Options
        if getdata and localFilePath:
            c.f = open(localFilePath, 'wb')
            c.setopt(pycurl.WRITEDATA, c.f)
        
        # store some info
        #c.filename = localFilePath
        #c.url = remoteFilePath

        #######################
        ### Uploading Options #
        #######################
        if senddata and localFilePath:
            f = open(localFilePath, 'rb')
            #c.setopt(pycurl.READFUNCTION, f.read());
            #c.setopt(pycurl.READDATA, f.read()); 
            c.setopt(pycurl.INFILE, f)
            c.setopt(pycurl.INFILESIZE, os.path.getsize(localFilePath))
            c.setopt(pycurl.INFILESIZE_LARGE, os.path.getsize(localFilePath))
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


############# RUN ####
def main(localFilePath=None):
    import sys,os
    if not localFilePath:
        try:
            localFilePath = sys.argv[1]
        except:
            localFilePath = ''
            pass    
    try:
        pycurl_upload_imagedrop(localFilePath)
        print "Successfully Loaded {}".format(localFilePath.split('/'[-1]))
    except:
        print "FAILED UPLOAD {}".format(localFilePath)
            


if __name__ == '__main__':
    main()